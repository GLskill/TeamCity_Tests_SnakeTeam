#!/bin/sh
set -eu

cat > /app/resources/config.properties <<EOF
baseurl=${SERVER}
UI_BASE_URL=${UI_BASE_URL}
EOF

exec "$@"
