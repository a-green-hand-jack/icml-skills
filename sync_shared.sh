#!/usr/bin/env bash
# 将 _shared/ 中的单一可信源复制到每个 skill 文件夹。
# 每个已安装的 skill 必须自包含，因此共享文件会被重复复制；
# 只在 _shared/ 中编辑它们，然后重新运行此脚本。
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
echo "共享文件已同步"
