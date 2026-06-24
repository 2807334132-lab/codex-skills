$ErrorActionPreference = "Stop"

$skills = Split-Path -Parent $MyInvocation.MyCommand.Path
$gitCandidates = @(
  "C:\Program Files\Git\cmd\git.exe",
  "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Git.MinGit_Microsoft.Winget.Source_8wekyb3d8bbwe\cmd\git.exe"
)

$git = $gitCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $git) {
  $cmd = Get-Command git -ErrorAction SilentlyContinue
  if ($cmd) { $git = $cmd.Source }
}
if (-not $git) {
  throw "Git was not found. Install Git for Windows first."
}

Write-Host "Syncing Codex skills in $skills"
& $git -C $skills pull --rebase --autostash
& $git -C $skills add -A

$staged = & $git -C $skills diff --cached --name-only
if ($staged) {
  & $git -C $skills commit -m "Sync skills"
} else {
  Write-Host "No local skill changes to commit."
}

& $git -C $skills push
Write-Host "Done."
Read-Host "Press Enter to close"
