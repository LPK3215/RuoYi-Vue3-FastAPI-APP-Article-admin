param(
  [string]$Image,
  [string]$ContainerName
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

$root = Get-RepoRoot
$runtimeRedis = Join-Path $root ".runtime\\redis"
$runtimeRedisData = Join-Path $runtimeRedis "data"
New-Item -ItemType Directory -Force -Path $runtimeRedisData | Out-Null

Assert-DockerInstalled

Write-Host "Pulling Redis image $Image ..."
docker pull $Image | Out-Host
if ($LASTEXITCODE -ne 0) {
  throw "docker pull 失败，请检查 Docker 是否正常联网。"
}

$metaPath = Join-Path $runtimeRedis "redis-image.txt"
Set-Content -Path $metaPath -Value "$Image`n$ContainerName" -Encoding UTF8

Write-Host "OK: Redis image is ready ($Image)"
Write-Host "Data directory: $runtimeRedisData"
