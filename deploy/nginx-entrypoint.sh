#!/bin/sh
set -e

export PROXY_SECRET="${PROXY_SECRET:-}"
envsubst '$PROXY_SECRET' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf
exec "$@"
