#!/bin/sh

set -e

flask db upgrade

gunicorn --bind 0.0.0.0:5000 app:app
