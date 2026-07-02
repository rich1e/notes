# Tag Taxonomy — Controlled Vocabulary

Canonical tag list for this vault. Max 5 tags per page (excluding `visibility/` system tags). All tags lowercase and hyphenated.

## Rules

- **Max 5 tags per page** — choose the most relevant; drop peripheral ones
- **Lowercase and hyphenated** — `core-data` not `CoreData` or `core data`
- **Prefer broad over narrow** — `networking` not `tcp-ip-layer-4`
- **Canonical over alias** — always use the canonical form listed here

---

## Domain Tags

### iOS / Apple Platform

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `ios` | `iOS`, `iPhone` | iOS development, apps, platform |
| `swift` | — | Swift programming language |
| `swiftui` | — | SwiftUI framework |
| `swiftdata` | — | SwiftData persistence framework |
| `core-data` | `coredata` | Core Data persistence |
| `cloudkit` | — | CloudKit sync and storage |
| `xcode` | `ide`, `simulator`, `playground` | Xcode IDE and toolchain |
| `xcode-cloud` | — | Xcode Cloud CI/CD |
| `app-store` | `publishing`, `testflight` | App Store / TestFlight |
| `architecture` | `mvvm`, `mvc`, `viper`, `mvp` | App architecture patterns |
| `networking` | `urlsession`, `alamofire`, `rest` | iOS networking |
| `concurrency` | `async-await`, `gcd`, `actor`, `dispatchqueue`, `operation`, `multithreading` | Concurrency and threading |
| `persistence` | `sqlite`, `userdefaults` | Local storage and persistence |
| `animation` | — | UI animation |
| `navigation` | — | App navigation patterns |
| `state-management` | `state-machine`, `observed-object` | State management patterns |
| `media` | `audio`, `music`, `camera`, `photography`, `media-asset` | Media handling |
| `security` | `permission`, `permissions`, `certificate`, `parental-control` | Security and privacy |
| `sideload` | `feather` | App sideloading tools |
| `weatherkit` | — | WeatherKit framework |

### Web / Frontend

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `react` | `react-hook`, `hooks` | React framework and ecosystem |
| `typescript` | — | TypeScript language |
| `javascript` | `event-loop`, `async`, `closures` | JavaScript language |
| `browser` | `chrome`, `webkit`, `WebKit`, `Chrome` | Browser internals and APIs |
| `chrome-extension` | `manifest-v3`, `content-script`, `service-worker`, `sidepanel` | Chrome extension development |
| `zustand` | — | Zustand state management |
| `antd` | — | Ant Design component library |
| `f2e` | `frontend` | Frontend development (general) |
| `vue` | `vue3` | Vue.js framework |
| `performance` | `http-cache`, `cookie`, `localstorage` | Web performance |
| `design-system` | `theming`, `ux`, `ui-pattern`, `declarative-ui` | Design systems and UX patterns |
| `webrtc` | `sip`, `jssip`, `phonebar` | Real-time communication |

### General Programming

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `programming` | `software` | General programming concepts |
| `architecture` | `design-patterns`, `pattern`, `anti-patterns` | Software architecture and patterns |
| `git` | — | Git version control |
| `debugging` | `bugfix`, `Bugfix` | Debugging and bug fixes |
| `type-system` | — | Type system concepts |
| `memory` | `reference-counting`, `arc` | Memory management |
| `networking` | — | Network protocols and concepts |
| `security` | `rbac` | Security concepts |

### AI / LLM

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `llm` | `AI`, `Deepseek` | Large language models |
| `claude-code` | `Claude` | Claude Code tool and features |
| `prompt-caching` | — | Prompt caching techniques |
| `token-optimization` | — | Token usage optimization |
| `automation` | `workflow` | Automation and workflows |

### DevOps / Tooling

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `macos` | `mac`, `macOS` | macOS system and tools |
| `cli` | `CLI`, `shell`, `terminal` | Command-line tools |
| `tools` | — | Development tools |
| `homebrew` | `Homebrew`, `Brew Update` | Homebrew package manager |
| `tmux` | — | tmux terminal multiplexer |
| `sublime` | — | Sublime Text editor |

### Retro Gaming / Hardware

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `game` | `gaming` | Games and gaming |
| `nintendo` | — | Nintendo platforms and games |
| `nds` | `NDS`, `dsi`, `DSi` | Nintendo DS family |
| `ique` | — | iQue Player (Chinese Nintendo) |
| `retro-gaming` | `emulator`, `neo-geo`, `neogeo`, `NEOGEO`, `MAME`, `download-play`, `pictochat` | Retro gaming and emulation |
| `fire-emblem` | `Fire-Emblem`, `fire-emblem` | Fire Emblem game series |
| `flashcard` | `R4`, `DSTWO` | DS flashcard hardware |
| `handheld` | `hardware`, `virtual-pet` | Portable gaming hardware |

### Business / Work

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `call-center` | `phonebar`, `sensorsdata`, `analytics` | Call center systems |
| `fintech` | — | Financial technology |
| `analytics` | — | Analytics and tracking |

### Personal / Life

| Canonical | Aliases | Usage |
|-----------|---------|-------|
| `travel` | `日本` | Travel notes |
| `book` | — | Books and reading |
| `personal` | `diary` | Personal notes |
| `photography` | — | Photography |

---

## Type Tags

| Tag | Usage |
|-----|-------|
| `daily` | Daily journal entries |
| `clippings` | Saved web clippings |
| `excalidraw` | Excalidraw diagrams |
| `undone` | Incomplete notes |
| `glossary` | Glossary / reference entries |
| `report` | Reports and summaries |

---

## System / Vault Tags

| Tag | Usage |
|-----|-------|
| `links` | Link collections |
| `maintenance` | Vault maintenance records |
| `vault-health` | Vault health reports |
| `linking` | Cross-linking operations |

---

## Tags Needing Cleanup

These tags were found in the vault but need normalization:

| Found | → Use Instead | Notes |
|-------|--------------|-------|
| `iOS` | `ios` | Lowercase |
| `NDS` | `nds` | Lowercase |
| `DSTWO` | `flashcard` | Use category tag |
| `R4` | `flashcard` | Use category tag |
| `Fire-Emblem` | `fire-emblem` | Normalize |
| `NEOGEO` | `retro-gaming` | Too specific |
| `MAME` | `retro-gaming` | Too specific |
| `mac` | `macos` | Use canonical |
| `macOS` | `macos` | Use canonical |
| `CLI` | `cli` | Lowercase |
| `Chrome` | `browser` | Use category tag |
| `WebKit` | `browser` | Use category tag |
| `AI` | `llm` | Use canonical |
| `Claude` | `claude-code` | Use canonical |
| `Deepseek` | `llm` | Use canonical |
| `Bugfix` | `debugging` | Use canonical |
| `Feather` | `sideload` | Use category tag |
| `Homebrew` | `homebrew` | Lowercase |
| `#vibe-coding` | — | Remove `#` prefix |
| `标签1`, `标签2` | — | Remove placeholder tags |
| `it` | — | Too generic, remove |
| `develop` | `programming` | Use canonical |
| `mobile` | `ios` | Use platform tag |

---

## Migration Guide

When normalizing tags, apply these renames:

```
iOS → ios
NDS → nds
DSTWO → flashcard
R4 → flashcard
Fire-Emblem → fire-emblem
NEOGEO → retro-gaming
MAME → retro-gaming
mac → macos
macOS → macos
CLI → cli
Chrome → browser
WebKit → browser
AI → llm
Claude → claude-code
Deepseek → llm
Bugfix → debugging
Feather → sideload
Homebrew → homebrew
#vibe-coding → (remove # prefix, keep as vibe-coding or drop)
标签1 → (remove)
标签2 → (remove)
it → (remove)
develop → programming
mobile → ios
ide → xcode
simulator → xcode
playground → xcode
publishing → app-store
testflight → app-store
```
