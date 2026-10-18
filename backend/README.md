# Groww read-only live quote adapter

This is a server-side adapter for the Ai-Studio Order Flow / Footprint UI prototype. It does not place orders. It uses Groww's documented quote API and keeps the access token on the server.

## Run locally

1. Use Python 3.10+ and install `pip install -r backend/requirements.txt`.
2. Set `GROWW_ACCESS_TOKEN` in your shell or deployment secret manager. Never commit it, put it in the APK, or paste it into frontend JavaScript.
3. Set `CHART_ALLOWED_ORIGINS` to the exact origin hosting the chart.
4. From the repository root run `uvicorn backend.groww_live_adapter:app --host 127.0.0.1 --port 8000`.
5. Check `GET /health`, then `GET /quote?exchange=NSE&segment=FNO&symbol=NIFTY`. A missing token, rejected token, invalid symbol, or stale/missing source timestamp must be treated as WAIT.

WebSocket endpoint: `/ws/market?exchange=NSE&segment=FNO&symbol=NIFTY`. The adapter polls quote snapshots every 2 seconds. It is not a tick-by-tick trade tape.

## Important limits

- This is not yet connected to the HTML chart or deployed to a hosted backend. The token and Groww API subscription/permissions are needed to validate a real response.
- Groww's documented SDK provides quote fields and market depth; quote snapshots do not by themselves provide aggressor-side executed trades. Do not present this data as a true bid/ask volume footprint or calculate exact absorption/stacked imbalance from it.
- Groww's API docs list CASH/FNO segments and state MCX commodity API trading is unsupported; this adapter rejects other segments.
- Before public deployment, add user authentication, HTTPS/WSS, request throttling, symbol/instrument-token validation, structured monitoring, provider rate-limit handling and a deployment-specific CORS allow-list.
- No order placement endpoints are included. This module is market-data-only.
