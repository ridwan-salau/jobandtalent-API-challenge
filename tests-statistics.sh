#!/bin/sh

set -e

coverage run --source=api -m unittest -b
echo "Coverage Report"
coverage html