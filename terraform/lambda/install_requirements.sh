#!/bin/sh

cd $1

# clean files
find . -path "*/__pycache__*" -delete 1>/dev/null


pip install -q -r requirements/production.txt --target .
