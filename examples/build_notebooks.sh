#!/usr/bin/env bash
# Builds example notebooks and converts the files to python scripts.

cd "${0%/*}" # go to script

###################################### from notebook to script
# jupyter run notebooks/*.ipynb
# jupyter nbconvert --to python notebooks/*.ipynb  --output-dir examples/


# for f in ./examples/*.py; do
#     sed -E -i '' '/^# In\[[0-9]+\]:/,+2d' $f
# done
########################################


# from script to notebook
for f in ./examples/*.py; do
    filename=$(basename -- "$f")
    outfile="./notebooks/${filename%.*}.ipynb"

    python -m py2jn "$f" "$outfile"
done

# use these to run all files
jupyter nbconvert --to=notebook --inplace --execute notebooks/*.ipynb
jupyter nbconvert --to=html notebooks/*.ipynb

# use these to run single notebook 
# jupyter nbconvert --to=notebook --inplace --execute notebooks/time_energy_calibration_demo.ipynb
# jupyter nbconvert --to=html notebooks/time_energy_calibration_demo.ipynb

