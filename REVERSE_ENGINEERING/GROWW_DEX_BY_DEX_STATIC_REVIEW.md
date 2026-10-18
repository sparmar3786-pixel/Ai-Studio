# Groww APK — Per-DEX Reverse-Engineering Pass (Static Only)

Input artifact: `DOC-20261018-WA0008.apk`
APK SHA-256: `de97d945728d8ad55aa4dd3314d79e4e6cc8afae64e2c522e43baabbd0c40b6d`

## What was actually performed

The APK ZIP archive was opened locally. Each of the eight DEX files was read individually; byte size, SHA-256, and printable-string counts were calculated. Strings were sampled for package names and SDK/domain markers. This is **static triage**, not a Java/Kotlin decompilation or Smali disassembly.

## Per-file pass

| DEX | Bytes | SHA-256 | Printable strings (5+ chars) | Static observations |
|---|---:|---|---:|---|
| `classes.dex` | 6,583,036 | `a0dd3cbc42086bf40707782f446964a9b421d020886f80c8a3e637db1409c86c` | 63,216 | AndroidX Work, Android framework, Kotlin, Firebase/Crashlytics/Performance markers; Groww static-content URL strings |
| `classes2.dex` | 269,108 | `2034a854018d7a3cff3eae760a4559f2f0d39897160ad10f197f11eb77e1f98b` | 1,657 | Small DEX; string sample mostly generic/Java serialization markers; no strong Groww domain marker in the sampled set |
| `classes3.dex` | 9,373,764 | `201d8e19e3acbbeb28d6219e4b1a97dea71cbe7324c3151ae99c0ee6dc61eb3b` | 73,308 | Firebase SDK markers and Groww URL strings, including a CP-home route |
| `classes4.dex` | 7,888,692 | `5b0bf3a0a32ed52f31b414ab8d38bb327bdabfe5dd5c695469384e7fca12ec3c` | 53,318 | Google Play Integrity/Review/Install and Firebase/Sentry markers |
| `classes5.dex` | 12,269,212 | `20af155193005b38328881f1f40b38ea880d5112db32b85227b0837946470693` | 84,235 | Clear `com/nextbillion/groww/...` model/class-name strings; Groww routes for holdings, open interest, privacy/help and balance |
| `classes6.dex` | 12,020,208 | `38bb1458177aa07fa75816fd3955b94cdf23ba756edd7cd5b05dbe2c2c5762a6` | 89,954 | Groww model/package strings, mutual-fund/help routes, Firebase Auth marker |
| `classes7.dex` | 11,353,716 | `7b64eefa4f924f6e770291c908102f7813da96892ce28ff6b17d37874620c413` | 99,925 | Groww biller model strings, font asset marker, Razorpay and mutual-fund/pledge route strings |
| `classes8.dex` | 8,266,092 | `4844827a45913526e3aba4f4b2b736443bc2504f167bd7662ca61f16bc9bd933` | 70,069 | Android framework/WebView, Razorpay SDK class markers and banking/teleport asset URLs |

## Archive-level checks

- ZIP entries: 8,861
- `res/`: 8,487 entries
- `assets/`: 182 entries
- `META-INF/`: 58 entries
- Root-level entries: 93
- `resources.arsc` and binary `AndroidManifest.xml`: present
- No `.so` files were found in the prior APK-root inventory.

## Next technical step

Use JADX for DEX-to-Java-like source and resource decoding, and Apktool for decoded Android resources/manifest. Official JADX documentation: https://github.com/skylot/jadx and releases: https://github.com/skylot/jadx/releases.

The current runtime has Java 21, but neither `jadx` nor `apktool` is installed; DNS resolution for GitHub currently fails. Therefore, full decompilation could not be executed here. No decompiled Java/Kotlin or Smali source is claimed as produced.

## Scope / handling

This report is a metadata and string-level review for authorized analysis. It deliberately does not publish the third-party APK, extracted proprietary assets, credentials, or a wholesale source-code copy. For a replacement app, implement required behavior independently.
