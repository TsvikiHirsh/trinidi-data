#!/usr/bin/env bash

# Builds example notebooks and converts the files to python scripts.
cd "${0%/*}" # go to 

###################################### from notebook to script
# jupyter run notebooks/*.ipynb
# jupyter nbconvert --to python notebooks/*.ipynb  --output-dir scripts/


# for f in ./scripts/*.py; do
#     sed -E -i '' '/^# In\[[0-9]+\]:/,+2d' $f
# done
########################################


# from script to notebook
for f in ./scripts/*.py; do
    filename=$(basename -- "$f")
    outfile="./notebooks/${filename%.*}.ipynb"

    python -m py2jn "$f" "$outfile"

done

jupyter nbconvert --to=notebook --inplace --execute notebooks/*.ipynb
jupyter nbconvert --to=html notebooks/*.ipynb

