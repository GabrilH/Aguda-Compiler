{- |
Module      :  Syntax
Description :  Abstract syntax for the Simple programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Vasco T. Vasconcelos
-}

module Syntax (Exp(..), Type(..)) where


data Exp = Let String Exp Exp
  | Cond Exp Exp Exp
  | Plus Exp Exp
  | Times Exp Exp
  | And Exp Exp
  | Or Exp Exp
  | Not Exp
  | IntLit Int
  | BoolLit Bool
  | Var String
  deriving Show

data Type = IntType | BoolType
  deriving (Eq, Show)

