{- |
Module      :  Calc
Description :  A calculator for the Simple programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Alcides Fonseca
               Vasco T. Vasconcelos
-}

module Calc (main) where

import Lexer
import Parser
import Syntax
import Data.Map.Strict

type Env = Map String Int

eval :: Env -> Exp -> Int
eval _   (Int v)       = v
eval env (Plus e1 e2)  = eval env e1 + eval env e2
eval env (Minus e1 e2) = eval env e1 - eval env e2
eval env (Times e1 e2) = eval env e1 * eval env e2
eval env (Div e1 e2)   = eval env e1 `div` eval env e2
eval env (Negate e)    = - (eval env e)
eval env (Var s)       = env ! s
eval env (Let s e1 e2) = eval env' e2
    where v = eval env e1
          env' = insert s v env
    
main :: IO ()
main = do
    s <- getContents
    let ast = parseCalc (alexScanTokens s)
    print ast
    print (eval empty ast)

