#!/bin/sh

if [ "$#" -eq 0 ]; then
    # Run all tests and save logs to the output directory
    python3 main.py
else
    # Run a single test with the provided test filepath
    python3 main.py "$1"
fi