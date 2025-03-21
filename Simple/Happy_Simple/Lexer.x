{
{- |
Module      :  Lexer
Description :  Lexer for the Simple programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Alcides Fonseca
               Vasco T. Vasconcelos

Run as:
  $ alex Lexer.x

to obtain Lexer.hs

To install alex run
  $ stack install alex
or
  $ cabal install alex

To install haskell (and cabal or stack) use ghcup, https://www.haskell.org/ghcup/dev/
-}

module Lexer where
}

%wrapper "basic"

$digit = 0-9
$alpha = [a-zA-Z]

tokens :-

  $white+                       ;
  "--".*                        ;
  let                           { \s -> TokenLet }
  in                            { \s -> TokenIn }
  $digit+                       { \s -> TokenInt (read s) }
  \=                            { \s -> TokenEq }
  \+                            { \s -> TokenPlus }
  \-                            { \s -> TokenMinus }
  \*                            { \s -> TokenTimes }
  \/                            { \s -> TokenDiv }
  \(                            { \s -> TokenLParen }
  \)                            { \s -> TokenRParen }
  $alpha [$alpha $digit \_ \']* { \s -> TokenId s }

{

-- The datatype for tokens
data Token = TokenLet
           | TokenIn
           | TokenInt Int
           | TokenId String
           | TokenEq
           | TokenPlus
           | TokenMinus
           | TokenTimes
           | TokenDiv
           | TokenLParen
           | TokenRParen
           deriving (Eq, Show)

scanTokens = alexScanTokens

}
