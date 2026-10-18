# Ai-Studio rules-only Bot AI starter

## Repository audit
The current `main` branch is a small reverse-engineering workspace (shell/docs), not an Android app source project. It has no Gradle/Flutter project, app screens, backend API, market-data adapter, broker adapter, or existing strategy integration. Therefore this engine is a new independent Python module; it is **not yet wired into an APK or live market feed**.

## Included
- `rules_engine.py`: transparent rule candidates for ORB, VWAP, OI Price Action, PDH/PDL, EMA Crossover, Hero Zero and Failed-Move.
- Fail-closed handling for stale timestamps, missing prices, strategy disagreement and missing/invalid stop-loss/target.
- Signal-only output (`order_placement: false`). `CANDIDATE` means rule checks passed, not a recommendation or a validated profitable trade.
- `../tests/test_rules_engine.py`: starter unit tests.

## Run tests locally
From repository root with Python 3.10+:

```bash
python -m unittest discover -s tests -v
```

## Before any live use
1. Connect a trusted market-data adapter and validate exchange timestamps, session/calendar, instrument identifiers, units and market-specific schemas.
2. Validate each strategy's actual definition and inputs. Hero Zero especially needs expiry/contract-selection rules; OI Price Action needs reliable option-chain snapshots; PDH/PDL needs session-aware levels and sweep/reclaim confirmation.
3. Add integration tests using recorded/redacted fixtures, backtests and paper-trading observation.
4. Add a risk policy, slippage/fees, position sizing and a stability gate before displaying live signals.
5. Wire the API into an actual Android app source project. Do not treat APK decompilation output as an editable original source project.

No real-time signal, accuracy, deployment, APK build, or market-data integration is claimed by this starter.