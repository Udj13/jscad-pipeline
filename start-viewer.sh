#!/usr/bin/env bash
# Start JSCAD 3D viewer with local file serving
# Serves the project root so viewer/ and *.stl files are accessible

set -e
cd "$(dirname "$0")"

PORT="${1:-8080}"

echo "========================================"
echo "  JSCAD 3D Viewer"
echo "  http://localhost:${PORT}/viewer/"
echo ""
echo "  STL files auto-discovered from /"
echo "  Direct link: http://localhost:${PORT}/viewer/?model=box-test.stl"
echo "  Press Ctrl+C to stop"
echo "========================================"

python3 server.py "$PORT"
