param(
    [Parameter(Position = 0)]
    [ValidateSet('install', 'dev', 'typecheck', 'test', 'build', 'e2e', 'browser')]
    [string]$Task = 'dev'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pnpmCommand = Get-Command pnpm.cmd -ErrorAction SilentlyContinue
if (-not $pnpmCommand) { $pnpmCommand = Get-Command pnpm -ErrorAction SilentlyContinue }
if ($pnpmCommand) {
    $pnpmPath = $pnpmCommand.Source
} else {
    $pnpmPath = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd'
    if (-not (Test-Path -LiteralPath $pnpmPath)) { throw '请安装 Node.js 22.12+ 和 pnpm 11.19.0，并将 pnpm 加入 PATH。' }
}
$frontendPath = Join-Path $projectRoot 'frontend'
if ($Task -eq 'install') {
    & $pnpmPath --dir $frontendPath install --frozen-lockfile
} elseif ($Task -eq 'browser') {
    & $pnpmPath --dir $frontendPath exec playwright install chromium
} else {
    & $pnpmPath --dir $frontendPath run $Task
}
exit $LASTEXITCODE
