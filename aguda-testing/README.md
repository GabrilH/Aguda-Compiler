# Aguda Testing

## Técnicas de Compilação, 2024-2025

Shared tests for the Aguda Programming Language

## Structure

There are two folders, one for valid tests (that is programs that should compile) and invalid tests (source code that does not represent a program, either because of a lexing, parsing or validation problem).

Each program (valid or invalid) must be included in a distinct folder. Valid test folders should contain two files. For a program `p`, include a `p.agu` (the source code) and a `p.expect` (a txt file with the expected output of program `p`). Folders for invalid tests contain one `.agu` file only.

## Contributing

Issue a pull request with your test proposals.
