#!/bin/bash

echo "--- Stopped containers ---"
docker ps -a --filter "status=exited"

echo "--- Dangling images ---"
docker images --filter "dangling=true"

read -p "Remove all stopped containers and dangling images? (y/n) " confirm
if [[ "$confirm" == "y" ]]; then
  docker container prune -f
  docker image prune -f
  echo "Cleaned up."
else
  echo "Skipped."
fi

