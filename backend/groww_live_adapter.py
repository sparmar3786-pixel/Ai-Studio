"""Groww live quote/depth adapter for the Ai-Studio chart prototype.

Credentials are read from GROWW_ACCESS_TOKEN on the server only. This module
never places orders. It deliberately labels quote/depth data separately from
trade prints: quote snapshots cannot produce an exact executed-volume footprint.
"""
from __future__ import annotations

import asyncio
import os
import time
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from growwapi import GrowwAPI

app = FastAPI(title="Ai-Studio Groww Read-only Market Data", version="0.1.0")
# Restrict this list to the actual hosted chart origin before public deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CHART_ALLOWED_ORIGINS", "http://localhost:8000").split(","),
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_client() -> GrowwAPI:
    token = os.getenv("GROWW_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError("GROWW_ACCESS_TOKEN is not configured on the server")
    return GrowwAPI(token)

def _quote_payload(client: GrowwAPI, exchange: str, segment: str, symbol: str) -> dict[str, Any]:
    quote = client.get_quote(exchange=exchange, segment=segment, trading_symbol=symbol)
    if not isinstance(quote, dict) or not quote:
        raise RuntimeError("Groww returned an empty or unexpected quote payload")
    now_ms = int(time.time() * 1000)
    last_trade_time = quote.get("last_trade_time")
    try:
        source_ts_ms = int(last_trade_time) if last_trade_time is not None else None
    except (TypeError, ValueError):
        source_ts_ms = None
    last_price = quote.get("last_price")
    if not isinstance(last_price, (int, float)) or last_price <= 0:
        raise RuntimeError("Quote has no valid last_price; fail closed")
    depth = quote.get("depth") if isinstance(quote.get("depth"), dict) else {}
    return {
        "provider": "Groww",
        "mode": "LIVE",
        "received_at": datetime.now(timezone.utc).isoformat(),
        "received_at_ms": now_ms,
        "source_trade_at_ms": source_ts_ms,
        "source_age_ms": max(0, now_ms - source_ts_ms) if source_ts_ms else None,
        "exchange": exchange,
        "segment": segment,
        "symbol": symbol,
        "last_price": float(last_price),
        "volume": quote.get("volume"),
        "last_trade_quantity": quote.get("last_trade_quantity"),
        "total_buy_quantity": quote.get("total_buy_quantity"),
        "total_sell_quantity": quote.get("total_sell_quantity"),
        "open_interest": quote.get("open_interest"),
        "bid_quantity": quote.get("bid_quantity"),
        "offer_quantity": quote.get("offer_quantity"),
        "depth": depth,
        "data_kind": "quote_and_book_snapshot",
        "footprint_ready": False,
        "warning": "Quote/depth snapshots are not aggressor-side executed trade prints; exact footprint is unavailable from this payload alone.",
    }

@app.get("/health")
async def health() -> dict[str, str]:
    configured = bool(os.getenv("GROWW_ACCESS_TOKEN", "").strip())
    return {"status": "configured" if configured else "WAIT", "provider": "Groww", "credentials_present": str(configured).lower(), "orders_enabled": "false"}

@app.get("/quote")
async def quote(
    exchange: str = "NSE",
    segment: str = "FNO",
    symbol: str = "NIFTY",
) -> dict[str, Any]:
    # Deliberate allow-list to avoid arbitrary API calls via query parameters.
    if exchange not in {"NSE", "BSE"} or segment not in {"CASH", "FNO"}:
        return {"status": "WAIT", "reason": "Unsupported exchange/segment. Groww API docs list CASH/FNO; MCX is not supported."}
    if not symbol or len(symbol) > 80 or any(ch not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-& " for ch in symbol):
        return {"status": "WAIT", "reason": "Invalid trading symbol"}
    try:
        payload = await asyncio.to_thread(_quote_payload, get_client(), exchange, segment, symbol)
        return {"status": "LIVE", "data": payload}
    except Exception as exc:
        # Do not expose tokens or raw provider exceptions to clients.
        return {"status": "WAIT", "reason": type(exc).__name__, "message": "Live quote unavailable; verify server credentials, subscription, symbol and Groww API status."}

@app.websocket("/ws/market")
async def market_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    exchange = websocket.query_params.get("exchange", "NSE").upper()
    segment = websocket.query_params.get("segment", "FNO").upper()
    symbol = websocket.query_params.get("symbol", "NIFTY").upper()
    if exchange not in {"NSE", "BSE"} or segment not in {"CASH", "FNO"}:
        await websocket.send_json({"status": "WAIT", "reason": "Unsupported exchange/segment; MCX is not supported by this Groww API integration."})
        await websocket.close(code=1008)
        return
    if not symbol or len(symbol) > 80 or any(ch not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-& " for ch in symbol):
        await websocket.send_json({"status": "WAIT", "reason": "Invalid trading symbol"})
        await websocket.close(code=1008)
        return
    try:
        client = get_client()
    except Exception:
        await websocket.send_json({"status": "WAIT", "reason": "Server credential GROWW_ACCESS_TOKEN is not configured"})
        await websocket.close(code=1011)
        return
    try:
        while True:
            try:
                payload = await asyncio.to_thread(_quote_payload, client, exchange, segment, symbol)
                # Fail closed when source trade time is absent or too old.
                age = payload.get("source_age_ms")
                if age is None or age > 15_000:
                    await websocket.send_json({"status": "WAIT", "reason": "Missing or stale source trade timestamp", "data": payload})
                else:
                    await websocket.send_json({"status": "LIVE", "data": payload})
            except Exception as exc:
                await websocket.send_json({"status": "WAIT", "reason": type(exc).__name__, "message": "Groww quote unavailable; charts must not treat the feed as live."})
            await asyncio.sleep(2)
    except (WebSocketDisconnect, RuntimeError):
        return
