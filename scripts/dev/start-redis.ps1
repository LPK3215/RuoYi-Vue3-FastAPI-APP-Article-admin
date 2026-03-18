param(
  [string]$Image,
  [string]$ContainerName,
  [Nullable[int]]$Port
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
  return (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
}

function Get-RedisDefaults {
  $defaults = @{
    Image = "redis:7.4.8"
    ContainerName = "ruoyi-redis-local"
    Port = 6379
  }

  $configPath = Join-Path $PSScriptRoot "redis-version.json"
  if (-not (Test-Path $configPath)) {
    return $defaults
  }

  try {
    $config = Get-Content -Path $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($config.image) {
      $defaults.Image = [string]$config.image
    }
    if ($config.containerName) {
      $defaults.ContainerName = [string]$config.containerName
    }
    if ($config.port) {
      $defaults.Port = [int]$config.port
    }
  } catch {
    Write-Warning "读取 redis-version.json 失败，继续使用内置默认值。$_"
  }

  return $defaults
}

function Assert-DockerInstalled {
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "docker 未安装或未加入 PATH，请先安装 Docker Desktop / Docker Engine。"
  }
}

$defaults = Get-RedisDefaults
if (-not $Image) {
  $Image = $defaults.Image
}
if (-not $ContainerName) {
  $ContainerName = $defaults.ContainerName
}
if ($null -eq $Port) {
  $Port = $defaults.Port
}

$root = Get-RepoRoot
$runtimeRedis = Join-Path $root ".runtime\\redis"
$runtimeRedisData = Join-Path $runtimeRedis "data"
New-Item -ItemType Directory -Force -Path $runtimeRedisData | Out-Null

Assert-DockerInstalled

$dockerDataDir = (Resolve-Path $runtimeRedisData).Path -replace '\\', '/'
$existing = docker ps -a --filter "name=^/${ContainerName}$" --format "{{.Status}}"
if ($LASTEXITCODE -ne 0) {
  throw "无法读取 Redis 容器状态，请确认 Docker 已启动。"
}

if ($existing) {
  if ($existing -like "Up*") {
    Write-Host "OK: redis already running in container $ContainerName (127.0.0.1:$Port)"
    exit 0
  }
  docker start $ContainerName | Out-Host
  if ($LASTEXITCODE -ne 0) {
    throw "启动已有 Redis 容器失败：$ContainerName"
  }
} else {
  docker run -d `
    --name $ContainerName `
    -p "${Port}:6379" `
    -v "${dockerDataDir}:/data" `
    $Image `
    redis-server --appendonly yes | Out-Host
  if ($LASTEXITCODE -ne 0) {
    throw "创建 Redis 容器失败，请检查端口 $Port 是否已被占用。"
  }
}

$ok = $false
for ($i = 0; $i -lt 20; $i++) {
  $pong = docker exec $ContainerName redis-cli ping 2>$null
  if ($LASTEXITCODE -eq 0 -and "$pong".Trim() -eq "PONG") {
    $ok = $true
    break
  }
  Start-Sleep -Milliseconds 500
}

if (-not $ok) {
  throw "Redis 容器已启动，但健康检查未通过：$ContainerName"
}

Write-Host "OK: redis started in container $ContainerName (127.0.0.1:$Port)"
