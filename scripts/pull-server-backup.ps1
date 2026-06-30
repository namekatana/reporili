param(
  [string]$Server = "root@165.227.201.61",
  [string]$TargetDir = "backups"
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

$remotePattern = "/root/reporili-backups/reporili-env-*.tar.gz"
$latest = ssh $Server "ls -1t $remotePattern 2>/dev/null | head -1"

if (-not $latest) {
  Write-Error "No backups found on server. Run deploy/server-backup.sh on the droplet first."
}

scp "${Server}:${latest}" $TargetDir/
Write-Output "Downloaded to $TargetDir"
