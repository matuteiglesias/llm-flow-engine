#!/bin/bash
# scripts/dev_start.sh

set -a
source .env
set +a

uvicorn api.main:app --reload
