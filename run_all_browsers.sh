#!/bin/zsh
for BROWSER in chromium firefox webkit; do
  echo "Running tests on $BROWSER..."
  BROWSER=$BROWSER ./run.sh || exit 1
done
