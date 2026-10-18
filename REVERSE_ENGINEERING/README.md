# APK reverse-engineering workspace

This directory documents an **authorized static-analysis workflow** for the APK supplied for this task. The APK itself and any extracted binary archive are not stored in this repository by this commit.

## Status

- APK ZIP inventory and DEX count were inspected in the analysis session.
- The APK contains 8 DEX files and 8,861 ZIP entries.
- The original Android manifest is binary XML until decoded.
- A complete JADX Java-like reconstruction and Apktool resource/Smali decode have **not** been verified yet.
- Raw ZIP extraction is not the same as complete decompilation.

## Run locally

Prerequisites: Java, JADX, Apktool, Python 3.

Place the APK at `input/app.apk`, then run:

```bash
bash REVERSE_ENGINEERING/run_local_analysis.sh input/app.apk
```

Outputs are created under `build/reverse-engineering/`:
- `apktool/` — decoded resources, manifest and Smali
- `jadx/` — reconstructed Java-like sources and resources
- `inventory.txt` — APK entry list, DEX sizes and hashes
- `SHA256SUMS.txt` — original APK checksum

## Repository hygiene and legal scope

Do not commit third-party proprietary app code, signing keys, session tokens, personal data, or a full commercial APK unless you have the rights and authorization to distribute them. Keep generated decompilation output local/private for authorized analysis. For a compatible replacement, implement desired features independently using original code and assets.

## Prior analysis artifact

The uploaded file was named `DOC-20261018-WA0008.apk`. The prior session reported size 86,303,468 bytes and SHA-256 `de97d945728d8ad55aa4dd3314d79e4e6cc8afae64e2c522e43baabbd0c40b6d`. Verify these values against your local copy before relying on them.
