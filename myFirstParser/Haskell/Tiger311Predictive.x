{
{- |
Module      :  Main
Description :  Lexer for the lang programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Vasco T. Vasconcelos

Run as:
  $ alex Tiger311Predictive.x
  $ runHaskell Tiger311Predictive < example.tiger311
or
  $ alex Tiger311Predictive.x
  $ ghc --make Tiger311Predictive
  $ ./Tiger311Predictive < example.tiger311

To install alex run
  $ stack install alex
or
  $ cabal install alex

To install haskell (and cabal or stack) use ghcup, https://www.haskell.org/ghcup/dev/

This lexer example is taken from https://haskell-alex.readthedocs.io/, with minor adaptations to the lang language

The grammar is that of Grammar 3.11, Modern Compiler Implementation in Java, A. Appel
-}

module Main (main) where
}

%wrapper "basic"

$digit = 0-9            -- digits
$alpha = [a-zA-Z]       -- alphabetic characters

tokens :-
  $white+                      ;
  "--".*                       ;
  if                           { \s -> If }
  then                         { \s -> Then }
  else                         { \s -> Else }
  "{"                          { \s -> Begin }
  "}"                          { \s -> End }
  print                        { \s -> Print }
  ";"                          { \s -> Semi }
  $digit+                      { \s -> Num (read s) }
  "=="                         { \s -> Eq }
{
-- Each action has type :: String -> Token

-- The token type:
data Token
  = If
  | Then
  | Else
  | Begin
  | End
  | Print
  | Semi
  | Num Int
  | Eq
  deriving (Eq, Show)

statement, expression, list :: [Token] -> [Token]

statement (If : ts) =
  let (Then : ts1) = expression ts
      (Else : ts2) = statement ts1
  in statement ts2
statement (Begin : ts) =
  let ts1 = statement ts
  in list ts1
statement (Print : ts) = expression ts
statement ts = error $ "Parse error. Remaining input at statement: " ++ show ts

list (End : ts) = ts
list (Semi : ts) =
  let ts1 = statement ts
  in list ts1
list ts = error $ "Parse error. Remaining input at list: " ++ show ts

expression (Num _ : Eq : Num _ : ts) = ts
expression ts = error $ "Parse error. Remaining input at expression: " ++ show ts

parse :: [Token] -> IO ()
parse ts = let ![] = statement ts in return ()

main = do
  s <- getContents
  parse (alexScanTokens s)
}
