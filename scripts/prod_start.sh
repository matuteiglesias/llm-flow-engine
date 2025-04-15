#!/bin/bash
# scripts/prod_start.sh

set -a
source .env
set +a

#!/bin/bash
exec gunicorn api.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
