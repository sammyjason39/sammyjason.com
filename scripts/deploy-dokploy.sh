#!/usr/bin/env bash
# Deploy sammyjason.com to Dokploy and verify the live bytes match this commit.
#
# Why this exists: the compose build clones the repo with a fixed instruction
# string, so Docker reuses the cached clone layer and serves stale content.
# Pinning CACHEBUST to the commit sha busts exactly that layer, nothing else.
#
# Usage: DOKPLOY_API_KEY=... scripts/deploy-dokploy.sh
# Env:   DOKPLOY_API_URL (default http://127.0.0.1:3000)
set -euo pipefail

: "${DOKPLOY_API_KEY:?set DOKPLOY_API_KEY}"
API="${DOKPLOY_API_URL:-http://127.0.0.1:3000}"
COMPOSE_ID="${DOKPLOY_COMPOSE_ID:-n8W3n38po1-JjoZjc2j9_}"
SITE="${SITE_URL:-https://sammyjason.com}"

cd "$(dirname "$0")/.."
SHA="$(git rev-parse HEAD)"
echo "deploying commit $SHA"

compose_file=$(cat <<YAML
services:
  web:
    build:
      context: .
      args:
        CACHEBUST: "$SHA"
      dockerfile_inline: |
        FROM node:22-alpine AS builder
        WORKDIR /app
        ARG CACHEBUST
        RUN apk add --no-cache git
        RUN git clone --depth 1 https://github.com/sammyjason39/sammyjason.com . \\
         && git fetch --depth 1 origin main \\
         && git reset --hard origin/main \\
         && echo "cloned at build \$CACHEBUST"
        RUN npm ci --no-audit --no-fund
        RUN npm run build
        FROM nginx:alpine
        COPY --from=builder /app/dist /usr/share/nginx/html
        COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf
        EXPOSE 80
        CMD ["nginx", "-g", "daemon off;"]
    container_name: sammyjason-web
    ports:
      - "3007:80"
    restart: unless-stopped
YAML
)

curl -sS -X POST "$API/api/compose.update" \
  -H "x-api-key: $DOKPLOY_API_KEY" -H 'Content-Type: application/json' \
  -d "$(python3 -c 'import json,sys; print(json.dumps({"composeId":sys.argv[1],"composeFile":sys.argv[2],"sourceType":"raw"}))' "$COMPOSE_ID" "$compose_file")" \
  -o /dev/null -w 'compose.update http=%{http_code}\n'

curl -sS -X POST "$API/api/compose.deploy" \
  -H "x-api-key: $DOKPLOY_API_KEY" -H 'Content-Type: application/json' \
  -d "$(python3 -c 'import json,sys; print(json.dumps({"composeId":sys.argv[1]}))' "$COMPOSE_ID")" \
  -w '\n' | head -c 200

# Verify the live asset matches the repo byte for byte; fail loud if stale.
for i in $(seq 1 20); do
  sleep 15
  ok=1
  for f in public/assets/downloads/*.pdf; do
    live=$(curl -sS -m 20 -o /tmp/.deploy-check.pdf -w '%{http_code}' "$SITE/assets/downloads/$(basename "$f")?cb=$RANDOM")
    if [ "$live" != "200" ]; then ok=0; break; fi
    cmp -s "$f" /tmp/.deploy-check.pdf || { ok=0; break; }
  done
  if [ "$ok" = "1" ]; then echo "verified live at $SITE after $((i*15))s"; exit 0; fi
done

echo "FAILED: live content still stale after deploy" >&2
exit 1
