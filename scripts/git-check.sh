#!/bin/bash

cd ~/devops-portfolio
echo "=== Current branch ==="
git branch --show-current

echo ""
echo "=== Uncommitted changes ==="
git status --short

echo ""
echo "=== Last 5 commits ==="
git log --oneline -5
