"""Fail-closed, rules-only signal evaluation for Ai-Studio.

This is an independently authored starter engine, not connected to a broker or app UI.
It emits WAIT unless data freshness and required fields are valid. Strategies are
transparent rule templates and must be calibrated/backtested before live use.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


STRATEGIES = (
    "ORB", "VWAP", "OI Price Action", "PDH/PDL",
    "EMA Crossover", "Hero Zero", "Failed-Move",
)


@dataclass
class MarketSnapshot:
    market: str
    symbol: str
    timestamp: str
    price: Optional[float] = None
    opening_range_high: Optional[float] = None
    opening_range_low: Optional[float] = None
    vwap: Optional[float] = None
    oi_bias: Optional[str] = None             # BULLISH / BEARISH / NEUTRAL
    pdh: Optional[float] = None
    pdl: Optional[float] = None
    reclaimed_level: Optional[str] = None    # PDH / PDL / NONE
    ema_fast: Optional[float] = None
    ema_slow: Optional[float] = None
    ema_previous_fast: Optional[float] = None
    ema_previous_slow: Optional[float] = None
    expiry_day: Optional[bool] = None
    near_otm_contract: Optional[bool] = None
    failed_breakout: Optional[str] = None    # UP / DOWN / NONE
    confirmation: Optional[bool] = None
    stop_loss: Optional[float] = None
    target: Optional[float] = None


@dataclass
class StrategyResult:
    strategy: str
    side: str
    reason: str


def _valid_num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _fresh(snapshot: MarketSnapshot, now: datetime, max_age_seconds: int) -> bool:
    try:
        stamp = datetime.fromisoformat(snapshot.timestamp.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            return False
        age = (now.astimezone(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds()
        return 0 <= age <= max_age_seconds
    except (ValueError, AttributeError, TypeError):
        return False


def evaluate(snapshot: MarketSnapshot, now: Optional[datetime] = None,
             max_age_seconds: int = 60) -> Dict[str, Any]:
    """Return a signal-only result. Missing/stale/contradictory data means WAIT."""
    now = now or datetime.now(timezone.utc)
    errors: List[str] = []
    if snapshot.market not in ("NIFTY", "BANKNIFTY", "MCX"):
        errors.append("unsupported_market")
    if not snapshot.symbol.strip():
        errors.append("missing_symbol")
    if not _fresh(snapshot, now, max_age_seconds):
        errors.append("stale_or_invalid_timestamp")
    if not _valid_num(snapshot.price) or snapshot.price <= 0:
        errors.append("missing_or_invalid_price")
    if errors:
        return {
            "status": "WAIT", "side": "WAIT", "market": snapshot.market,
            "symbol": snapshot.symbol, "entry": None, "stop_loss": None,
            "target": None, "strategies": [], "reasons": errors,
            "order_placement": False,
        }

    p = float(snapshot.price)
    results: List[StrategyResult] = []

    # ORB: breakout must be confirmed; no assumptions when range is absent.
    if (_valid_num(snapshot.opening_range_high) and
        _valid_num(snapshot.opening_range_low) and snapshot.confirmation is True):
        if p > snapshot.opening_range_high:
            results.append(StrategyResult("ORB", "BUY", "confirmed_above_opening_range"))
        elif p < snapshot.opening_range_low:
            results.append(StrategyResult("ORB", "SELL", "confirmed_below_opening_range"))

    # VWAP direction is only a candidate, not sufficient alone to authorize entry.
    if _valid_num(snapshot.vwap):
        if p > snapshot.vwap and snapshot.confirmation is True:
            results.append(StrategyResult("VWAP", "BUY", "price_above_vwap_confirmed"))
        elif p < snapshot.vwap and snapshot.confirmation is True:
            results.append(StrategyResult("VWAP", "SELL", "price_below_vwap_confirmed"))

    if snapshot.oi_bias in ("BULLISH", "BEARISH") and snapshot.confirmation is True:
        results.append(StrategyResult("OI Price Action",
            "BUY" if snapshot.oi_bias == "BULLISH" else "SELL",
            "oi_bias_and_price_confirmation"))

    # Sweep/reclaim: reclaim field must explicitly identify the swept level.
    if snapshot.reclaimed_level == "PDH" and p < snapshot.pdh if _valid_num(snapshot.pdh) else False:
        results.append(StrategyResult("PDH/PDL", "SELL", "pdh_sweep_rejected"))
    if snapshot.reclaimed_level == "PDL" and p > snapshot.pdl if _valid_num(snapshot.pdl) else False:
        results.append(StrategyResult("PDH/PDL", "BUY", "pdl_sweep_reclaimed"))

    if all(_valid_num(v) for v in (snapshot.ema_fast, snapshot.ema_slow,
                                    snapshot.ema_previous_fast, snapshot.ema_previous_slow)):
        if snapshot.ema_previous_fast <= snapshot.ema_previous_slow and snapshot.ema_fast > snapshot.ema_slow:
            results.append(StrategyResult("EMA Crossover", "BUY", "bullish_crossover"))
        elif snapshot.ema_previous_fast >= snapshot.ema_previous_slow and snapshot.ema_fast < snapshot.ema_slow:
            results.append(StrategyResult("EMA Crossover", "SELL", "bearish_crossover"))

    # Hero Zero requires explicit expiry/contract/confirmation flags.
    if snapshot.expiry_day is True and snapshot.near_otm_contract is True and snapshot.confirmation is True:
        if snapshot.oi_bias == "BULLISH":
            results.append(StrategyResult("Hero Zero", "BUY", "expiry_near_otm_bullish_confirmed"))
        elif snapshot.oi_bias == "BEARISH":
            results.append(StrategyResult("Hero Zero", "SELL", "expiry_near_otm_bearish_confirmed"))

    if snapshot.failed_breakout == "UP" and snapshot.confirmation is True:
        results.append(StrategyResult("Failed-Move", "SELL", "upside_breakout_failed"))
    elif snapshot.failed_breakout == "DOWN" and snapshot.confirmation is True:
        results.append(StrategyResult("Failed-Move", "BUY", "downside_breakout_failed"))

    sides = {r.side for r in results}
    # Fail closed: conflicting candidates, no candidates, or absent risk values -> WAIT.
    if len(sides) != 1:
        return {
            "status": "WAIT", "side": "WAIT", "market": snapshot.market,
            "symbol": snapshot.symbol, "entry": None, "stop_loss": None,
            "target": None, "strategies": [asdict(r) for r in results],
            "reasons": ["no_strategy_agreement" if not sides else "strategy_conflict"],
            "order_placement": False,
        }

    side = next(iter(sides))
    if not (_valid_num(snapshot.stop_loss) and _valid_num(snapshot.target)):
        risk_reason = ["missing_stop_loss_or_target"]
        status = "WAIT"
        side_out = "WAIT"
        entry = sl = target = None
    else:
        sl, target = float(snapshot.stop_loss), float(snapshot.target)
        risk_valid = (sl < p < target) if side == "BUY" else (target < p < sl)
        if not risk_valid:
            risk_reason = ["invalid_risk_geometry"]
            status, side_out, entry, sl, target = "WAIT", "WAIT", None, None, None
        else:
            risk_reason = []
            status, side_out, entry = "CANDIDATE", side, p

    return {
        "status": status, "side": side_out, "market": snapshot.market,
        "symbol": snapshot.symbol, "entry": entry, "stop_loss": sl,
        "target": target, "strategies": [asdict(r) for r in results],
        "reasons": risk_reason, "order_placement": False,
    }
