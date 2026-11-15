#!/bin/bash
set -euo pipefail
cd /home/project
if [ ! -d Back-end-Development-Capstone ]; then
    git clone https://github.com/igiiaw/Back-end-Development-Capstone.git
fi
cd Back-end-Development-Capstone
git pull --ff-only
docker build -t capstone-main-lab .
docker run --rm --name capstone-main-lab -p 8000:8000 \
    -e PICTURES_API_URL=https://pictures.2h79v0rtfn9k.us-south.codeengine.appdomain.cloud \
    capstone-main-lab
