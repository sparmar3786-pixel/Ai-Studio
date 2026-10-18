# Order Flow + Footprint chart prototype

File: [order_flow_footprint_prototype.html](./order_flow_footprint_prototype.html)

## Included
- Two independent tabs: Order Flow and Footprint.
- Order Flow panel: illustrative delta/CVD plot, buy/sell split, and diagnostics.
- Footprint panel: bid/ask volume ladder, synthetic intensity, POC and imbalance interpretation placeholders.
- Responsive dark terminal styling and mobile layout.
- Explicit WAIT/unverified status until a live feed adapter is validated.

## Important integration status
This is a standalone front-end prototype, not yet embedded in an Android APK and not connected to Groww. All chart numbers are synthetic demo data. The market and timeframe selectors are UI-only.

To make it genuinely live, integrate only through an authorized, documented Groww data interface and validate:
1. Instrument/token mapping and market session.
2. Feed timestamps, reconnect handling, staleness detection and missing-data behaviour.
3. Bid/ask aggressor-side volume or trade-level data for true footprint. OHLCV candles alone cannot reconstruct exact bid/ask footprint or absorption.
4. Rendering performance on target Android devices, bounded data buffers and throttled UI updates.
5. Unit/integration tests and fail-closed WAIT behaviour on stale or incomplete feed.

Do not display simulated values as live market data or treat this prototype as a trade signal.
