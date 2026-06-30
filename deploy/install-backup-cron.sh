#!/bin/sh
set -eu

repoDir="/opt/reporili"
backupScript="$repoDir/deploy/server-backup.sh"
cronLine="0 3 * * 0 $backupScript >> /var/log/reporili-backup.log 2>&1"

chmod +x "$backupScript"
touch /var/log/reporili-backup.log
chmod 600 /var/log/reporili-backup.log

current="$(crontab -l 2>/dev/null || true)"
filtered="$(printf '%s\n' "$current" | grep -v 'deploy/server-backup.sh' || true)"
printf '%s\n%s\n' "$filtered" "$cronLine" | sed '/^$/d' | crontab -

echo "cron installed: $cronLine"
