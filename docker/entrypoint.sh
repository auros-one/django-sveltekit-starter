#!/bin/bash
set -e

# if SKIP_MIGRATIONS is set and not false, don't to dhem
if [ -z "$SKIP_MIGRATIONS" ] || [ "$SKIP_MIGRATIONS" = "false" ]; then
    # Run Django database migrations
    echo "[entrypoint.sh] Running database migrations..."
    python manage.py migrate
fi

# Execute the command provided as arguments to the entrypoint (from CMD)
echo "[entrypoint.sh] Executing command: $@"
exec "$@"
