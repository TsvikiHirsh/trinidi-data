#!/usr/bin/env bash

# Builds example notebooks and converts the files to python scripts.
cd "${0%/*}" # go to 

jupyter run notebooks/*.ipynb
jupyter nbconvert --to python notebooks/*.ipynb  --output-dir scripts/


for f in ./scripts/*.py; do
    sed -E -i '' '/^# In\[[0-9]+\]:/,+2d' $f
done

