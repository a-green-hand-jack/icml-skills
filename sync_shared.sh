#!/usr/bin/env bash
# Copy the single source of truth from _shared/ into each skill folder.
# Each installed skill must be self-contained, so shared files are duplicated;
# edit them only in _shared/, then rerun this script.
set -euo pipefail
cd "$(dirname "$0")"
for s in icml-write icml-cite icml-review icml-rebuttal icml-camera-ready; do
  mkdir -p "$s/references" "$s/scripts"
  cp _shared/references/icml-venue-facts.md "$s/references/"
  cp _shared/references/workspace-contract.md "$s/references/"
  cp _shared/scripts/init_workspace.py "$s/scripts/"
done
for s in icml-write icml-review icml-camera-ready; do
  cp _shared/scripts/check_submission.py "$s/scripts/"
done
echo "Shared files synchronized"
