param(
    [Parameter(Mandatory = $true)]
    [string]$GameRoot,

    [ValidateSet("Install", "Restore")]
    [string]$Action = "Install"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$pack = Join-Path $projectRoot "dist\Wargroove 2\1.2.x\20260926\config.dat"
$target = Join-Path $GameRoot "assets\config.dat"
$backup = Join-Path $GameRoot "assets\config.dat.wargroove-ko-original"
$expected = "746b17b14cb52dcbd3d9e94ca33d8400e2bae6555d564b66a40a6661a456bbc6"

if (-not (Test-Path -LiteralPath $target)) {
    throw "Target config.dat was not found: $target"
}

if ($Action -eq "Restore") {
    if (-not (Test-Path -LiteralPath $backup)) {
        throw "Backup was not found: $backup"
    }
    Copy-Item -LiteralPath $backup -Destination $target -Force
    Write-Host "Restored original config.dat."
    exit 0
}

if (-not (Test-Path -LiteralPath $pack)) {
    throw "Generated pack was not found: $pack"
}

$actual = (Get-FileHash -LiteralPath $pack -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) {
    throw "Final pack hash mismatch. Expected $expected, got $actual"
}

if (-not (Test-Path -LiteralPath $backup)) {
    Copy-Item -LiteralPath $target -Destination $backup
    Write-Host "Created original backup: $backup"
}

Copy-Item -LiteralPath $pack -Destination $target -Force
Write-Host "Installed final Korean config.dat for testing."
Write-Host "After testing, restore with:"
Write-Host "  .\Test-Wargroove2-KoreanPack.ps1 -GameRoot `"$GameRoot`" -Action Restore"
