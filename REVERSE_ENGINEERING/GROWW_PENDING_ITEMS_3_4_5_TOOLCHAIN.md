# Groww APK — Pending Items 3, 4, 5: Toolchain and Closure Plan

**Status date:** 2026-10-18  
**Target artifact recorded in existing reports:** `DOC-20261018-WA0008.apk`  
**Recorded size:** 86,303,468 bytes  
**Recorded SHA-256 (not independently re-verified in this run):** `de97d945728d8ad55aa4dd3314d79e4e6cc8afae64e2c522e43baabbd0c40b6d`

## Honest status

The existing inventory documents eight DEX files and an encoded Android manifest. This is not full decompilation. During this run the APK binary was not present in the current conversation attachments or the searched Library results, so the following outputs cannot honestly be marked complete:

- **Item 3:** readable AndroidManifest.xml and decoded resource table.
- **Item 4:** JADX Java-like decompilation and Apktool Smali/resource output.
- **Item 5:** findings report based on actual decoded permissions, components, SDKs, and configuration.

GitHub research was completed to identify suitable tools and documented commands. No proprietary Groww source/assets are copied into this repository.

## Tool research (official / upstream repositories)

1. **apkdec** — https://github.com/emrezdemir/apk-decompiler  
   CLI can inspect package metadata, permissions/components, decode the binary manifest, extract the APK, enumerate DEX classes, and run a basic static security scan. Its README says the initial info/scan/manifest/extract/DEX functions do not need Java; full decompilation invokes JADX or Apktool and may download them. Review its disclaimer and use only with appropriate authorization.

2. **JADX** — https://github.com/skylot/jadx  
   Decompiles DEX/APK bytecode into Java-like source and can decode AndroidManifest.xml/resources. Upstream explicitly warns that decompilation may be incomplete or imperfect.

3. **Apktool** — https://github.com/iBotPeaches/Apktool  
   Decodes Android resources and emits Smali for bytecode inspection. Rebuilding/signing a third-party application is outside the scope of this review.

## Reproducible workflow (run on a trusted workstation with the actual APK)

Set the input path and first verify the bytes against the recorded hash:

```bash
export APK="$PWD/DOC-20261018-WA0008.apk"
sha256sum "$APK"
```

Do not proceed under the assumption that the recorded hash matches unless the command output matches it exactly. If it differs, preserve the new hash and treat the artifact as a different version.

### Item 3 — Decode and review the Android Manifest

Install/use apkdec from its upstream repository, then run:

```bash
python -m apkdec info "$APK" --json > groww-apk-info.json
python -m apkdec manifest "$APK" -o AndroidManifest.xml
python -m apkdec scan "$APK" --json > groww-apk-security-scan.json
```

Review and record, with evidence:
- package name, version, min/target SDK and signing scheme;
- requested permissions and whether each appears justified;
- exported activities, services, receivers and providers, including required permissions;
- intent filters, deep links, backup/debug settings and cleartext/network-security policy;
- provider authorities and any risky task/launch configuration.

A scanner finding is a lead to validate, not proof of an exploitable vulnerability.

### Item 4 — Extract resources and decompile all DEX files

Use a private, access-controlled output directory. Keep outputs out of public Git:

```bash
mkdir -p private-analysis
jadx -j 4 -d private-analysis/jadx "$APK"
apktool d -f "$APK" -o private-analysis/apktool
```

If the JADX CLI is not installed, obtain it only from the upstream release page linked in the official repository. If Apktool is not installed, follow the official project installation instructions. Do not execute unknown scripts from third-party mirrors.

After each tool exits, capture exit status and logs. Check that the output contains a readable manifest, resource files, Java-like files, and Smali directories for the DEX payloads. Decompilers can fail on obfuscated or unsupported constructs; record warnings rather than claiming perfect source recovery.

### Item 5 — Evidence-based technical findings

Build the final report from the actual outputs above. Include:
- artifact SHA-256, tool versions, command lines, timestamps and exit codes;
- manifest permissions/components and risk rationale;
- SDK/dependency indicators and relevant version evidence where available;
- network host strings only as **static indicators** (not proof of runtime connections);
- secrets findings only as redacted indicators; never commit tokens, keys, personal data or session material;
- unresolved questions and confidence level for each finding.

Do not publish the full decompiled proprietary source, original assets, credentials, or private backend details. For a replacement app, document the observed public-facing behavior and implement it independently.

## Closure criteria

Mark items 3–5 complete only after the actual APK is available and all of these are true:

- [ ] Actual APK hash verified and recorded.
- [ ] Decoded manifest and resource table generated and inspected.
- [ ] JADX output generated; warnings/errors reviewed.
- [ ] Apktool output generated; resource/Smali directories inspected.
- [ ] Eight DEX payloads accounted for in outputs (or a documented tool limitation).
- [ ] Security/SDK findings cite actual output evidence, not guesses.
- [ ] Sensitive outputs remain private and are excluded from public Git.

**Current blocker:** the APK binary itself is not mounted in the current execution environment. The GitHub research and reproducible workflow are complete; the artifact-dependent extraction and final findings are not. No successful decompilation is claimed.
