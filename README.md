# SDM Providers & Scrapers Remote Configuration

This repository hosts the official curated rankings and default sources configuration for the **SDM (Stream Discovery & Media)** Android application.

The app automatically checks this repository every **7 days** (or when the user taps "Check for Source Updates" in the app's settings) to update scraper tiers, seed default repositories/addons, and immediately hotfix broken scrapers without requiring an APK release.

---

## 📁 Repository Contents

- [`providers_config.json`](./providers_config.json): The production configuration file read by the SDM client.
- [`validate_config.ps1`](./validate_config.ps1): PowerShell validator script to verify JSON structure before pushing.
- [`validate_config.py`](./validate_config.py): Python validator script alternative.

---

## 🚀 GitHub Repository & Hosting

- **Repository**: `https://github.com/shameer22455/S-CONFIG.git`
- **Raw URL**: `https://raw.githubusercontent.com/shameer22455/S-CONFIG/main/providers_config.json`

This raw URL is fetched automatically by the SDM Android app on cold start and background sync.

### Pushing Updates to GitHub
```bash
git add providers_config.json README.md validate_config.ps1 validate_config.py
git commit -m "Update SDM providers configuration"
git push origin main
```

---

## ⚙️ How the App Uses This Config

| Config Field | Description | Client Impact |
|---|---|---|
| `syncIntervalDays` | Time between automatic background checks (default: `7`). | The app caches the config locally and checks once every 7 days (or immediately on manual check). |
| `defaultRepositories` | Curated Nuvio / JS plugin repositories. | **Dynamic Multi-Repo Sync**: Any repository added here with `enabledByDefault: true` is automatically downloaded and installed on all client devices without requiring an APK update! |
| `defaultAddons` | Curated media addons (e.g. Cinemeta, HDHub, WebStreamR, Torrentio Lite). | Auto-seeded into the app's Addon Store. |
| `addonRankings.priorityAddons` | Curated Tier 1 fast-track addons (`hdhub`, `webstream`, `baby-beamup`). | Launched **immediately** (0ms) in parallel; receive tier score bonuses in AutoPlay matching. |
| `scraperRankings.tier1_priority` | Elite Tier 1 scrapers (`4khdhub`, `hdhub4u`, `hdghartv`, `uhdmovies`, `vegamovies`). | Launched **immediately** (<0ms) with first semaphore permits. Powers fast AutoPlay. |
| `scraperRankings.tier2_fallback` | Secondary, deep-search, or specialized scrapers. | Launched after a 300ms stagger or if Tier 1 yields low results. |
| `scraperRankings.disabled` | Known broken or temporarily down scrapers. | **Hotfix**: Any scraper ID placed in this array is immediately silenced across all devices without needing an app update! |

---

## ⚡ Addon Tiers & Execution Architecture

In SDM, addons are evaluated and executed across three distinct execution tiers:

1. **Tier 0: User-Pinned Addons (Rank `-1`)**
   - **Trigger:** Toggling the Star icon on any addon in the Addons Manager (`UserSourcePriorityStore.toggleAddonPin`).
   - **Execution:** Launched immediately at 0ms.
   - **Score Bonus:** Awarded a **+35 tier bonus** in `StreamMetadataMatcher`. Overrides all remote config rankings.

2. **Tier 1: Curated Priority Addons (Rank `0..N`)**
   - **Trigger:** Configured in `addonRankings.priorityAddons` (strictly `hdhub`, `webstream`, `baby-beamup`).
   - **Execution:** Launched immediately in Phase 1 (parallel coroutines with zero delay).
   - **Score Bonus:** Awarded a **+25 to +10 tier bonus** (`25 - (priority * 3)`), ensuring fast, high-quality streams surface at the top.
   - **AutoPlay:** Eligible for sub-200ms golden fast-track auto-play dispatch.

3. **Tier 2: Community & Fallback Addons (Rank `999`)**
   - **Trigger:** Any installed custom or third-party addon URL not in the curated priority list.
   - **Execution:** Launched in Phase 2 in chunked batches of 5 with 200ms staggering to prevent socket exhaustion and bandwidth contention.
   - **Score Bonus:** Awarded a baseline **+5 bonus**.

### 🧩 Functional Addon Types
- **Direct Playable Web Streams** (e.g. `WebStreamR`): Direct HTTP/HLS sources that bypass Debrid caching and play instantly.
- **Debrid-Cached Video Streams** (e.g. `HDHub`, `Torrentio`): Multi-gigabit cached torrent streams requiring Real-Debrid / TorBox / AllDebrid / Premiumize resolution.
- **Catalog & Metadata Providers** (e.g. `Cinemeta`, `Cyberflix`): Provide catalog rails, genres, and metadata discovery.
- **Subtitle Providers** (e.g. `OpenSubtitles v3`): Queried dynamically for subtitle tracks.


---

## 🛡️ Validation

Before pushing any changes to GitHub, test your JSON:
- **Using PowerShell**:
  ```powershell
  .\validate_config.ps1
  ```
- **Using Python**:
  ```bash
  python validate_config.py
  ```
