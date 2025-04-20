{- |
Module      :  TypeChecker
Description :  A type checker the Simple programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Vasco T. Vasconcelos
-}

module Main (main) where

import Lexer
import Parser
import TypeChecker
import qualified Data.Map.Strict as Map


main :: IO ()
main = do
    s <- getContents
    let ast = parse (alexScanTokens s)
    -- print ast
    case typeof Map.empty ast of
      Left msg -> putStrLn $ "Error: " ++ msg
      Right t -> putStrLn $ "Valid expression of type: " ++ show t
