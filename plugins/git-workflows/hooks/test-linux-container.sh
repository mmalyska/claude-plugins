#!/bin/sh
set -e
apt-get update -qq
apt-get install -y -qq git jq >/dev/null 2>&1
echo "--- linux toolchain ---"
bash --version | head -1
git --version
jq --version
echo "--- running suite ---"
exec bash /w/plugins/git-workflows/hooks/test-guard.sh
