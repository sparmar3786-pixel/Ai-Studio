# Groww APK — Static Inventory Report

## Artifact verification

- Input: `DOC-20261018-WA0008.apk`
- File size: 86,303,468 bytes
- SHA-256: `de97d945728d8ad55aa4dd3314d79e4e6cc8afae64e2c522e43baabbd0c40b6d`
- ZIP entries: 8,861
- DEX files: 8

## DEX inventory

| File | Bytes |
|---|---:|
| `classes.dex` | 6,583,036 |
| `classes2.dex` | 269,108 |
| `classes3.dex` | 9,373,764 |
| `classes4.dex` | 7,888,692 |
| `classes5.dex` | 12,269,212 |
| `classes6.dex` | 12,020,208 |
| `classes7.dex` | 11,353,716 |
| `classes8.dex` | 8,266,092 |

## Archive entry counts

- `res/`: 8,487 entries
- `assets/`: 182 entries
- root-level entries: 93
- `META-INF/`: 58
- other package/resource prefixes: remaining entries

## Static string observations

Printable strings in DEX files include package markers `com.nextbillion.groww` and `com.groww`, and hostnames including `groww.in`, `mapi.groww.in`, `storage.googleapis.com`, `google.com`, and Firebase/Google SDK markers. These are string-level observations only; they do not prove a host is contacted at runtime. Full URLs, credentials, and sensitive strings are intentionally omitted.

## Limitations

- The APK ZIP structure and SHA-256 were checked locally.
- DEX string scanning is not Java/Kotlin decompilation and may include SDK strings or unused code.
- The binary `AndroidManifest.xml` has not been decoded into readable XML.
- Full JADX/Apktool decompilation is still pending: neither tool is installed in the current environment, and outbound DNS/network access is unavailable, preventing tool download.
- This report does not include the APK itself or extracted proprietary source/assets.

For authorized review, run JADX and Apktool on a trusted workstation. Use any findings to independently implement needed functionality rather than republishing a third-party app wholesale.
