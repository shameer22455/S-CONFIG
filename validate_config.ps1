$jsonPath = Join-Path $PSScriptRoot "providers_config.json"

if (-not (Test-Path $jsonPath)) {
    Write-Error "providers_config.json not found at $jsonPath"
    exit 1
}

try {
    $raw = Get-Content -Path $jsonPath -Raw -Encoding UTF8
    $config = ConvertFrom-Json -InputObject $raw

    Write-Host "Validating providers_config.json..." -ForegroundColor Cyan
    Write-Host "  - Version: $($config.version)"
    Write-Host "  - Updated At: $($config.updatedAt)"
    Write-Host "  - Sync Interval (Days): $($config.syncIntervalDays)"
    Write-Host "  - Default Repositories: $($config.defaultRepositories.Count)"
    Write-Host "  - Default Addons: $($config.defaultAddons.Count)"
    Write-Host "  - Tier 1 Priority Scrapers: $($config.scraperRankings.tier1_priority.Count)"
    Write-Host "  - Tier 2 Fallback Scrapers: $($config.scraperRankings.tier2_fallback.Count)"
    Write-Host "  - Disabled Scrapers: $($config.scraperRankings.disabled.Count)"
    Write-Host "  - Priority Addons: $($config.addonRankings.priorityAddons.Count)"

    if ($config.version -lt 1) { throw "Invalid version: $($config.version)" }
    if ($config.scraperRankings.tier1_priority.Count -eq 0) { throw "tier1_priority cannot be empty" }
    if ($config.addonRankings.priorityAddons.Count -eq 0) { throw "priorityAddons cannot be empty" }

    Write-Host "`n[SUCCESS] providers_config.json is valid and ready to push to GitHub!" -ForegroundColor Green
    exit 0
} catch {
    Write-Error "Validation failed: $_"
    exit 1
}
