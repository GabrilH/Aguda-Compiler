# A calculator for the Simple programming language

## Usage:
  $ make

## Installing

### Haskell

To install haskell (and cabal or stack) use ghcup, https://www.haskell.org/ghcup/dev/

### Alex and Happy

To install alex and happy run
  $ stack install alex
  $ stack install happy
or
  $ cabal install alex
  $ cabal install happy

## The grammar of the Simple programming language

```
Exp : let var = Exp in Exp
    | Exp + Exp
    | Exp - Exp
    | Exp * Exp
    | Exp / Exp
    | ( Exp )
    | - Exp
    | int
    | var
```

### Copyright

Técnicas de Compilação
Mestrado em Engenharia Informática
Faculdade de Ciências
Universidade de Lisboa
2024/2025
Vasco T. Vasconcelos
