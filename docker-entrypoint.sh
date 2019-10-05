#!/bin/bash

set -e

exec python /app/OpenNMT-py/server.py  &
exec python src/app.py
