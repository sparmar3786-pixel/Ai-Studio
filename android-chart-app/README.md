# Ai-Studio Charts Android app

This is an Android WebView wrapper for the repository's Order Flow and Footprint prototype. It is **not the Groww proprietary app or a clone of Groww's source**.

## Build
The GitHub Actions workflow builds a debug APK and uploads it as an artifact. The app has two separate chart tabs from the bundled HTML.

## Live-data configuration
On first launch, enter the URL of a deployed Ai-Studio backend, for example `https://your-service.example`. The app converts HTTP(S) to WS(S) and connects to `/ws/market`. Set `GROWW_ACCESS_TOKEN` only as a backend secret; never embed it in the APK or commit it to Git.

Until a real backend is deployed and verified, the UI must be treated as demo/WAIT. The Groww quote/depth snapshot adapter does not provide executed aggressor-side trade prints, so it cannot substantiate a true trade-by-trade footprint, CVD, absorption or stacked-imbalance calculation. MCX is unsupported by the current adapter.


Build workflow updated to use the runner-provided Android SDK tools.

Build note: workflow now locates sdkmanager dynamically and reports SDK path if unavailable.
