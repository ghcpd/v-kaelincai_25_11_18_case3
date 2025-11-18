#!/bin/sh
set -e
WORKDIR=$(cd "$(dirname "$0")" && pwd)
RESULTS_DIR="$WORKDIR/results"
PROJECT_OUTPUT="$RESULTS_DIR/artifacts"
rm -rf "$RESULTS_DIR"
mkdir -p "$PROJECT_OUTPUT"
./setup.sh
python run_projects.py --output "$PROJECT_OUTPUT"
pytest tests -q --disable-warnings --maxfail=1 --junitxml="$RESULTS_DIR/pytest.xml"
