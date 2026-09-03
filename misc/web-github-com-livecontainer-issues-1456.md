---
title: "LiveContainer Issue #1456: SideStore \"Unable to manage profiles on the device\""
category: misc
tags: [mobile, Feather, bug, troubleshooting]
sources:
  - "https://github.com/LiveContainer/LiveContainer/issues/1456"
source_url: "https://github.com/LiveContainer/LiveContainer/issues/1456"
created: "2026-07-26T03:00:00Z"
updated: "2026-07-26T03:00:00Z"
tier: peripheral
summary: "LiveContainer nightly 3.7.14 + iPadOS 26.3 下，SideStore 内置\"Refresh All\"触发 Unable to manage profiles；维护者结论是 iOS 26+ 须用 RPPairing 替代旧 Lockdown 配对文件。"
affinity:
  "[[skills/ios-sideloading-fundamentals]]": 3
promotion_status: misc
stub: false
provenance:
  extracted: 0.85
  inferred: 0.10
  ambiguous: 0.05
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: "2026-07-26"
---

# LiveContainer Issue #1456: SideStore "Unable to manage profiles on the device"

## Overview

This issue (filed by GaryYeah on 2026-07-17, closed by maintainer hugeBlack on 2026-07-19) is a real-world SideStore refresh failure reproduced inside LiveContainer 3.7.14 Nightly on iPadOS 26.3. The user could not refresh apps: tapping **Refresh All** in the built-in SideStore surfaced the error **"Unable to manage profiles on the device"** continuously, even after resetting the pairing file.

The maintainer's diagnosis pinpoints a known regression introduced when Apple deprecated the legacy Lockdown pairing format on iOS 26.x in favour of **RPPairing**. SideStore 续签 (and StikDebug's JIT flow) need an `rppairing` file rather than the older one; if your install path (e.g. iloader) does not generate one, use `idevice_pair` v0.1.14+ by jkcoxson to produce it.

## Key Points

- **Environment**: LiveContainer 3.7.14 Nightly, iPadOS 26.3 (iPad).
- **Reproduction**: Connect to LocalDevVPN → open the built-in SideStore → tap **Refresh All** → error appears.
- **Workaround attempted**: Resetting the pairing file did **not** resolve the issue — implying the user either reset the wrong file type or the file format itself was the cause.
- **Maintainer fix (hugeBlack, 2026-07-19)**:
  1. Use the **latest nightly** build, not a pinned older release.
  2. On **iOS 26+**, the pairing file **must be RPPairing**, not legacy Lockdown pairing.
  3. If iloader does not produce one, generate it with `idevice_pair` (v0.1.14 by jkcoxson).
- **Maintainer ask for triage**: exact error text, screenshot of SideStore's **Health Check** page (fully scrolled), and SideStore's console log from `Files → sidestore → Documents → ConsoleLogs → most recent file`.

## Concepts

- [[skills/ios-sideloading-fundamentals]] — Existing vault page documenting SideStore's minimuxer / Anisette / LocalDevVPN stack and the iOS 26.4 RPPairing format change. This issue is the canonical case study of what that format change breaks in practice.
- `RPPairing` ^[inferred] — Apple's replacement for legacy Lockdown pairing on iOS 26+, required by SideStore's local developer workflow. Not a separate wiki page yet; the existing skill page references it under "iOS 26.4 的影响".
- `idevice_pair` (jkcoxson, v0.1.14) ^[inferred] — Cross-platform pairing-file generator. Used as a fallback when iloader doesn't produce an RPPairing file.

## Entities

- `LiveContainer` ^[inferred] — Open-source iOS container that runs apps without installing them to the system. Issue tracker lives at github.com/LiveContainer/LiveContainer.
- `SideStore` ^[inferred] — AltStore-family sideloader that re-signs apps over Wi-Fi using an Anisette server and a local VPN tunnel.
- `hugeBlack` ^[inferred] — LiveContainer maintainer (the issue is pinned to their diagnostic comment).
- `jkcoxson` ^[inferred] — Author of `idevice_pair` (referenced for pairing-file generation on iOS 26+).

## Open Questions

- Whether `idevice_pair` v0.1.14+ is bundled with or separately installed from the LiveContainer nightly — not stated in the issue. ^[ambiguous]
- Whether **resetting the pairing file** that the user attempted was the legacy Lockdown file (which would explain why the fix failed) or an RPPairing file (in which case the bug is something else). The issue text does not specify. ^[ambiguous]
- SideStore console log contents are not public in the thread; root cause beyond "wrong pairing format" is not pinned down.

## Related

- [[skills/ios-sideloading-fundamentals]] — Foundational page on iOS sideloading; "iOS 26.4 的影响" section already explains the RPPairing format change that this issue makes concrete.
- [[entities/feather-ios-sideload]] — Alternate signing path; uses paid certificates and avoids the SideStore pairing-file chain entirely.