param(
  [string]$TargetDir = ""
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
  return (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
}

$root = Get-RepoRoot
$runtimeRedis = if ($TargetDir) { $TargetDir } else { (Join-Path $root ".runtime\\redis") }
New-Item -ItemType Directory -Force -Path $runtimeRedis | Out-Null

$redisServerExe = Join-Path $runtimeRedis "redis-server.exe"
if (Test-Path $redisServerExe) {
  Write-Host "OK: redis already exists at $redisServerExe"
  exit 0
}

Write-Host "Downloading portable Redis (Windows) to $runtimeRedis ..."

# 1) Get latest tag by following redirects
$latest = Invoke-WebRequest -Uri "https://github.com/tporadowski/redis/releases/latest" -MaximumRedirection 10
$finalUrl = $latest.BaseResponse.ResponseUri.AbsoluteUri
if ($finalUrl -notmatch "/releases/tag/(?<tag>[^/]+)$") {
  throw "Could not parse latest release tag from URL: $finalUrl"
}
$tag = $Matches["tag"]

# 2) Fetch expanded assets HTML (contains actual download links)
$expandedUrl = "https://github.com/tporadowski/redis/releases/expanded_assets/$tag"
$expanded = Invoke-WebRequest -Uri $expandedUrl -MaximumRedirection 10
$content = $expanded.Content

# 3) Find the zip download link
$zipHrefs = [regex]::Matches($content, 'href=\"([^\"]+\.zip)\"', 'IgnoreCase') | ForEach-Object { $_.Groups[1].Value }
$candidates = $zipHrefs | Where-Object { $_ -like "*/releases/download/*" -and $_ -like "*/tporadowski/redis/*" }
if (-not $candidates -or $candidates.Count -eq 0) {
  throw "Could not find a .zip asset link in expanded_assets page: $expandedUrl"
}
$chosen = ($candidates | Where-Object { $_ -match "x64" } | Select-Object -First 1)
if (-not $chosen) { $chosen = $candidates | Select-Object -First 1 }

$downloadUrl = "https://github.com$chosen"
$zipPath = Join-Path $runtimeRedis "redis.zip"

Write-Host "Downloading $downloadUrl"
Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -MaximumRedirection 10

Write-Host "Extracting $zipPath"
Expand-Archive -Path $zipPath -DestinationPath $runtimeRedis -Force
Remove-Item $zipPath -Force

if (-not (Test-Path $redisServerExe)) {
  throw "Download finished, but redis-server.exe not found in $runtimeRedis"
}

Write-Host "OK: Redis extracted to $runtimeRedis"

