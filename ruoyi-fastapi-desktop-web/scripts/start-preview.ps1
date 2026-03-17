$ErrorActionPreference = 'Stop'

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $projectRoot

Write-Host "== DeskOps: build + preview ==" -ForegroundColor Cyan

if (-not (Test-Path (Join-Path $projectRoot 'node_modules'))) {
  Write-Host "Installing deps..." -ForegroundColor Cyan
  npm install
}

Write-Host "Building..." -ForegroundColor Cyan
npm run build

$port = 5175
$url = "http://localhost:$port"

Write-Host "Opening $url" -ForegroundColor Cyan
Start-Process $url | Out-Null

Write-Host "Starting preview server on $url" -ForegroundColor Cyan
npm run preview -- --host 127.0.0.1 --port $port

