param(
  [switch]$SkipBuild = $false,
  [switch]$SkipSql = $false,
  [int]$WaitSeconds = 120
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
  return (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
}

function Wait-ForContainers {
  param(
    [int]$TimeoutSeconds = 120
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while ((Get-Date) -lt $deadline) {
    $ps = & docker compose -f (Join-Path (Get-RepoRoot) "docker-compose.my.yml") ps 2>$null
    if ($LASTEXITCODE -eq 0 -and ($ps -match "ruoyi-mysql") -and ($ps -match "healthy") -and ($ps -match "ruoyi-redis") -and ($ps -match "healthy")) {
      return
    }
    Start-Sleep -Seconds 2
  }

  throw "Timeout waiting for containers to be ready (mysql/redis healthy)."
}

$root = Get-RepoRoot
Set-Location $root

$composeFile = Join-Path $root "docker-compose.my.yml"
if (-not (Test-Path $composeFile)) {
  throw "docker-compose.my.yml not found: $composeFile"
}

Write-Host "1) Starting docker compose (dockermy)..."
$composeArgs = @("-f", $composeFile, "up", "-d")
if (-not $SkipBuild) {
  $composeArgs += "--build"
}
& docker compose @composeArgs

Write-Host "2) Waiting for mysql/redis to be healthy..."
Wait-ForContainers -TimeoutSeconds $WaitSeconds

if (-not $SkipSql) {
  Write-Host "3) Applying incremental SQL (software + kb)..."
  $softwareSql = Join-Path $root "ruoyi-fastapi-backend\\sql\\ruoyi-fastapi-software.sql"
  $kbSql = Join-Path $root "ruoyi-fastapi-backend\\sql\\ruoyi-fastapi-kb.sql"

  if (-not (Test-Path $softwareSql)) { throw "SQL not found: $softwareSql" }
  if (-not (Test-Path $kbSql)) { throw "SQL not found: $kbSql" }

  Get-Content $softwareSql -Raw | docker exec -i ruoyi-mysql mysql -uroot -proot -D ruoyi-fastapi | Out-Null
  Get-Content $kbSql -Raw | docker exec -i ruoyi-mysql mysql -uroot -proot -D ruoyi-fastapi | Out-Null
}

Write-Host "4) Verifying KB menus/tables..."
$menuCheck = & docker exec -i ruoyi-mysql mysql -uroot -proot -D ruoyi-fastapi -e "SELECT menu_id,parent_id,menu_name,path,component FROM sys_menu WHERE menu_id IN (120,124,130,131) ORDER BY menu_id;"
if ($LASTEXITCODE -ne 0) { throw "Menu check failed." }

$tablesCheck = & docker exec -i ruoyi-mysql mysql -uroot -proot -D ruoyi-fastapi -e "SHOW TABLES LIKE 'tool_kb_%';"
if ($LASTEXITCODE -ne 0) { throw "KB tables check failed." }

Write-Host "5) Verifying portal endpoints..."
$cats = & curl.exe --noproxy "*" -sS "http://127.0.0.1:19099/portal/article/categories" | ConvertFrom-Json
if ($cats.code -ne 200) { throw "Portal categories failed: $($cats.msg)" }

Write-Host ""
Write-Host "OK: dockermy is up and KB module looks healthy."
Write-Host "Admin:  http://127.0.0.1:12580/"
Write-Host "Backend: http://127.0.0.1:19099/"

