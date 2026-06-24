param(
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $Repo

function Find-Git {
    $cmd = Get-Command git -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $candidates = @(
        "C:\Program Files\Git\cmd\git.exe",
        "$env:USERPROFILE\AppData\Local\Microsoft\WinGet\Packages\Git.MinGit_Microsoft.Winget.Source_8wekyb3d8bbwe\cmd\git.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }

    throw "Git was not found. Install Git or update this script with the git.exe path."
}

$Git = Find-Git
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = "Update skills $timestamp"
}

Write-Host "Codex skills sync" -ForegroundColor Cyan
Write-Host "Repo: $Repo"
Write-Host ""

Write-Host "1/4 Pulling latest changes..."
& $Git pull --rebase --autostash
if ($LASTEXITCODE -ne 0) {
    throw "Pull failed. Resolve the conflict, then run this script again."
}

Write-Host ""
Write-Host "2/4 Checking local changes..."
& $Git add -A
& $Git diff --cached --quiet
$hasChanges = $LASTEXITCODE -ne 0

if ($hasChanges) {
    Write-Host ""
    Write-Host "3/4 Committing changes..."
    & $Git commit -m $Message
    if ($LASTEXITCODE -ne 0) {
        throw "Commit failed."
    }
} else {
    Write-Host "No local changes to commit."
}

Write-Host ""
Write-Host "4/4 Pushing to GitHub..."
& $Git push
if ($LASTEXITCODE -ne 0) {
    throw "Push failed. Check your network or GitHub login, then run this script again."
}

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "Press any key to close..."
[void][System.Console]::ReadKey($true)
