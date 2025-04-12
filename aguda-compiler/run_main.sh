#!/bin/sh

# Ensure the output directory exists
mkdir -p output

if [ "$#" -eq 0 ]; then
    # Run all tests and save logs to the output directory
    python3 main.py
    cp test/*.log output/
else
    # Run a single test with the provided test filepath
    python3 main.py "$1"
fi