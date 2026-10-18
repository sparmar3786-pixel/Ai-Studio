#!/usr/bin/env bash
set -euo pipefail

# Authorized local APK analysis only. Never commit the APK or generated
# proprietary decompilation output to a public repository without permission.
APK_PATH="${1:-}"
if [[ -z "$APK_PATH" || ! -f "$APK_PATH" ]]; then
  echo "Usage: $0 /path/to/authorized-app.apk" >&2
  exit 2
fi

command -v java >/dev/null || { echo "Java is required." >&2; exit 1; }
command -v jadx >/dev/null || { echo "Install JADX first: https://github.com/skylot/jadx" >&2; exit 1; }
command -v apktool >/dev/null || { echo "Install Apktool first: https://apktool.org/" >&2; exit 1; }

BASE="$(cd "$(dirname "$APK_PATH")" && pwd)"
NAME="$(basename "$APK_PATH" .apk)"
OUT="$BASE/${NAME}-analysis"
mkdir -p "$OUT"

sha256sum "$APK_PATH" | tee "$OUT/SHA256SUMS.txt"
unzip -l "$APK_PATH" > "$OUT/apk-file-inventory.txt"

# Java-like sources/resources and Android resource/Smali decoding.
jadx --threads-count 4 --export-gradle -d "$OUT/jadx" "$APK_PATH"
apktool d --force --all-src -j 4 -o "$OUT/apktool" "$APK_PATH"

echo "Analysis completed locally: $OUT"
echo "Review generated output before sharing. Do not publish third-party proprietary code/assets without authorization."
