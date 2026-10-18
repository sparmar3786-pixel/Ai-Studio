# APK Static Analysis — Ai-Studio

## Scope
This repository was empty at inspection time. The supplied APK is a third-party Groww Android application (package/class strings include `com.nextbillion.groww` and `com.groww`). This note records basic artifact facts and a reproducible local analysis workflow. It does **not** include or reproduce Groww's proprietary source code, assets, UI, credentials, or backend endpoints.

## Supplied artifact facts
- File name: `DOC-20261018-WA0008.apk`
- Size: 86,303,468 bytes
- SHA-256: `de97d945728d8ad55aa4dd3314d79e4e6cc8afae64e2c522e43baabbd0c40b6d`
- APK entries: 8,861
- DEX files: `classes.dex` through `classes8.dex`
- `resources.arsc`: present
- `AndroidManifest.xml`: present (binary Android XML)
- Native `.so` libraries: none found in the APK root listing

## Reproducible local inspection
Install Android build tools, JADX, and Apktool on a trusted workstation. Keep the APK in a private analysis directory and do not commit the APK or extracted proprietary app code into this repository.

```bash
sha256sum DOC-20261018-WA0008.apk
apktool d -f DOC-20261018-WA0008.apk -o apktool-out
jadx -d jadx-out DOC-20261018-WA0008.apk
```

Useful review targets:
1. Manifest permissions, exported components, deep links, and network security configuration.
2. App-owned configuration and hard-coded secrets (report/redact findings; do not publish credentials).
3. Network domains and API contracts for compatibility/security review.
4. Third-party SDK inventory and outdated dependencies.
5. Decompiled code only for authorized security review or interoperability; implement any replacement independently with original code and design.

## Current limitation
This environment could inspect the APK ZIP structure and DEX string samples, but does not have JADX or Apktool installed, and direct Git cloning is unavailable. Therefore a full Java/Kotlin decompilation and decoded manifest are **not yet completed**.