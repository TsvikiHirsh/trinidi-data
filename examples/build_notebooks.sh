#!/usr/bin/env bash
# Builds example notebooks and converts the files to python scripts.

cd "${0%/*}" # go to script


# Building single notebook by passing the file name of the script
# otherwise building all notebooks.

if [ $1 ]; then
    filename=$(basename -- "$1")
    outfile_ipynb="./notebooks/${filename%.*}.ipynb"

    echo "Running on $filename"

    python -m py2jn "examples/${filename}" "$outfile_ipynb"


    jupyter nbconvert --to=notebook --inplace --execute "$outfile_ipynb"
    jupyter nbconvert --to=html "$outfile_ipynb"

    # outfile_html="./notebooks/${filename%.*}.html"
    # open -a "Safari" "$outfile_html"

else
    echo "Running on all files in ./examples/*.py"

    for f in ./examples/*.py; do
        filename=$(basename -- "$f")
        outfile="./notebooks/${filename%.*}.ipynb"

        python -m py2jn "$f" "$outfile"
    done

    jupyter nbconvert --to=notebook --inplace --execute notebooks/*.ipynb
    jupyter nbconvert --to=html notebooks/*.ipynb

    # open -a "Safari" notebooks/*.html


fi
