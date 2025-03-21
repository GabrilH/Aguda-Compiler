{
{- |
Module      :  Main
Description :  Lexer for the lang programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Vasco Vasconcelos

Run as:
  $ alex Tokens.x
  $ runHaskell Tokens < example.lang
or
  $ alex Tokens.x
  $ ghc --make Tokens
  $ ./Tokens < example.lang

To install alex run
  $ stack install alex
or
  $ cabal install alex

To install haskell (and cabal or stack) use ghcup, https://www.haskell.org/ghcup/dev/

This lexer example is taken from https://haskell-alex.readthedocs.io/, with minor adaptations to the lang language
-}

module Main (main) where
}

%wrapper "basic"

$digit = 0-9            -- digits
$alpha = [a-zA-Z]       -- alphabetic characters

tokens :-

  $white+                        ;
  "--".*                         ;
  print                          { \s -> Print }
  $digit+                        { \s -> Int (read s) }
  [\=\+\-\*\/\(\)]               { \s -> Sym (head s) }
  $alpha [$alpha $digit \_ \']*  { \s -> Var s }

{
-- Each action has type :: String -> Token

-- The token type:
data Token
  = Print
  | Sym Char
  | Var String
  | Int Int
  deriving (Eq, Show)

main = do
  s <- getContents
  print (alexScanTokens s)
}
