#!/bin/sh
set -eu

repoDir="/opt/reporili"
backupDir="/root/reporili-backups"
keepCount=4

mkdir -p "$backupDir"

stamp="$(date -u +%Y%m%d-%H%M%S)"
archive="$backupDir/reporili-env-$stamp.tar.gz"

files=""
for path in .env backend/.env frontend/.env; do
  if [ -f "$repoDir/$path" ]; then
    files="$files $path"
  fi
done

if [ -z "$files" ]; then
  echo "no env files found in $repoDir"
  exit 1
fi

tar czf "$archive" -C "$repoDir" $files
chmod 600 "$archive"

ls -1t "$backupDir"/reporili-env-*.tar.gz 2>/dev/null | tail -n +$((keepCount + 1)) | xargs -r rm -f --

echo "backup saved: $archive"
