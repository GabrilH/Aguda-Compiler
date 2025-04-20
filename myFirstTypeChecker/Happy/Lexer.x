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
-}

module Lexer (alexScanTokens, Token(..)) where
}

%wrapper "posn"

$digit = 0-9
$alpha = [a-zA-Z]

tokens :-

  $white+                       ;
  "--".*                        ;
  let                           { \pos _ -> TokenLet pos}
  in                            { \pos _ -> TokenIn pos }
  $digit+                       { \pos s -> TokenInt pos (read s) }
  true                          { \pos s -> TokenBool pos (read s) }
  false                         { \pos s -> TokenBool pos (read s) } 
  if                            { \pos _ -> TokenIf pos } 
  then                          { \pos _ -> TokenThen pos } 
  else                          { \pos _ -> TokenElse pos } 
  \=                            { \pos _ -> TokenEq pos }
  \+                            { \pos _ -> TokenPlus pos }
  \-                            { \pos _ -> TokenMinus pos }
  \*                            { \pos _ -> TokenTimes pos }
  "&&"                          { \pos _ -> TokenAnd pos }
  "||"                          { \pos _ -> TokenOr pos }
  not                           { \pos _ -> TokenNot pos }
  \/                            { \pos _ -> TokenDiv pos }
  \(                            { \pos _ -> TokenLParen pos }
  \)                            { \pos _ -> TokenRParen pos }
  $alpha [$alpha $digit \_ \']* { TokenId }

{
type Pos = AlexPosn
  
-- The datatype for tokens
data Token = TokenLet Pos
           | TokenIn Pos
           | TokenIf Pos
           | TokenThen Pos
           | TokenElse Pos
           | TokenInt Pos Int
           | TokenBool Pos Bool
           | TokenId Pos String
           | TokenEq Pos
           | TokenPlus Pos
           | TokenMinus Pos
           | TokenTimes Pos
           | TokenDiv Pos
           | TokenAnd Pos
           | TokenOr Pos
           | TokenNot Pos
           | TokenLParen Pos
           | TokenRParen Pos
           deriving (Eq, Show)

}
