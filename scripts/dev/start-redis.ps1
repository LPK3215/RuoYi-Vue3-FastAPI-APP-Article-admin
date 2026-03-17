param(
  [string]$TargetDir = ""
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
  return (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
}

$root = Get-RepoRoot
$runtimeRedis = if ($TargetDir) { $TargetDir } else { (Join-Path $root ".runtime\\redis") }
$redisServerExe = Join-Path $runtimeRedis "redis-server.exe"
$redisConf = Join-Path $runtimeRedis "redis.windows.conf"

if (-not (Test-Path $redisServerExe)) {
  throw "redis-server.exe not found. Run scripts/dev/setup-redis.ps1 first. Expected: $redisServerExe"
}
if (-not (Test-Path $redisConf)) {
  throw "redis.windows.conf not found. Expected: $redisConf"
}

$existing = Get-Process -Name "redis-server" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($existing) {
  Write-Host "OK: redis already running (pid=$($existing.Id))"
  exit 0
}

$p = Start-Process `
  -FilePath $redisServerExe `
  -WorkingDirectory $runtimeRedis `
  -ArgumentList @("redis.windows.conf") `
  -PassThru
Start-Sleep -Seconds 1
Write-Host "OK: redis started (pid=$($p.Id))"
