#!/usr/bin/env python3
import json
import os
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "providers_config.json")

    if not os.path.exists(config_path):
        print(f"Error: providers_config.json not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        print("Validating providers_config.json...")
        print(f"  - Version: {config.get('version')}")
        print(f"  - Updated At: {config.get('updatedAt')}")
        print(f"  - Sync Interval (Days): {config.get('syncIntervalDays')}")
        print(f"  - Default Repositories: {len(config.get('defaultRepositories', []))}")
        print(f"  - Default Addons: {len(config.get('defaultAddons', []))}")

        rankings = config.get("scraperRankings", {})
        print(f"  - Tier 1 Priority Scrapers: {len(rankings.get('tier1_priority', []))}")
        print(f"  - Tier 2 Fallback Scrapers: {len(rankings.get('tier2_fallback', []))}")
        print(f"  - Disabled Scrapers: {len(rankings.get('disabled', []))}")

        addon_rankings = config.get("addonRankings", {})
        print(f"  - Priority Addons: {len(addon_rankings.get('priorityAddons', []))}")

        if config.get("version", 0) < 1:
            raise ValueError(f"Invalid version: {config.get('version')}")
        if not rankings.get("tier1_priority"):
            raise ValueError("tier1_priority list cannot be empty")
        if not addon_rankings.get("priorityAddons"):
            raise ValueError("priorityAddons list cannot be empty")

        print("\n[SUCCESS] providers_config.json is valid and ready to push to GitHub!")
        sys.exit(0)
    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
