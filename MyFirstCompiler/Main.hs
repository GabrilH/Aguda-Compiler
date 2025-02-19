{- |
Module      :  Main
Description :  My First Compiler
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Vasco Vasconcelos

    Basic interpreter and compiler for the lang programming language
-}

module Main where

import Data.Char ( isDigit, isSpace )
import Data.List ( lines )
import qualified Data.Map.Strict as Map
import qualified Data.Set as Set
import System.Environment ( getArgs )
import System.Exit ( exitFailure )
import System.Process ( callCommand )

data Exp = Literal Int | Variable String | Plus Exp Exp
    deriving Show

data Stmt = Assign String Exp | Print Exp
    deriving Show

-- Parsing 
parseExp :: String -> Exp
parseExp s | '+' `elem` s =
    let (s1, s2) = split s '+'
    in Plus (parseExp(trim s1)) (parseExp(trim s2))
parseExp s | isDigit (head s) =
    Literal (read s)
parseExp s = Variable s

parseStmt :: String -> Stmt
parseStmt ('p' : 'r' : 'i' : 'n' : 't' : s) =
    Print (parseExp (trim s))
parseStmt s | '=' `elem` s =
    let (s1, s2) = split s '='
    in Assign (trim s1) (parseExp (trim s2))

parse :: String -> [Stmt]
parse s = map parseStmt ss
  where ss = filter (\l -> not (null l) && (head l) /= '#') (lines s)

-- Interpreting
type Store = Map.Map String Int

eval :: Store -> Exp -> Int
eval _     (Literal n) = n
eval store (Variable s) = store Map.! s
eval store (Plus e1 e2) = eval store e1 + eval store e2

interpret :: [Stmt] -> [String]
interpret = interp Map.empty
  where
    interp :: Store -> [Stmt] -> [String]
    interp _ [] = [""]
    interp store (Assign s e : stmts) =
        interp (Map.insert s (eval store e) store) stmts
    interp store (Print e : stmts) = show (eval store e) : interp store stmts

-- Validating
type Declarations = Set.Set String

validExp :: Declarations -> Exp -> Bool
validExp _     (Literal _) = True
validExp decls (Variable s) = s `Set.member` decls
validExp decls (Plus e1 e2) = validExp decls e1 && validExp decls e2

valid :: [Stmt] -> Bool
valid = validStms Set.empty
    where
        validStms :: Declarations -> [Stmt] -> Bool
        validStms _ [] = True
        validStms decls (Assign s e : stmts) =
            validExp decls e && validStms (Set.insert s decls) stmts
        validStms decls (Print e : stmts) = validExp decls e && validStms decls stmts

-- Compiling
compileExp :: Exp -> String
compileExp (Literal n) = show n
compileExp (Variable s) = s
compileExp (Plus (Literal n1) (Literal n2)) = show $ n1 + n2
compileExp (Plus e1 e2) = compileExp e1 ++ " + " ++ compileExp e2

compileStmt :: Stmt -> String
compileStmt (Print e) = "  printf(\"%d\\n\", " ++ compileExp e ++ ");\n"
compileStmt (Assign s e) = "  int " ++ s ++ " = " ++ compileExp e ++ ";\n"

compile :: [Stmt] -> IO ()
compile stmts = do
    writeFile "middle.c" src
    callCommand "gcc -o executable middle.c"
    where
        code = concatMap compileStmt stmts
        src = "#include <stdio.h>\nint main() {\n" ++ code ++ "  return 0;\n}\n"

-- Main
main = do
    [prog] <- getArgs
    contents <- readFile prog
    let stmts = parse contents
    if not $ valid stmts
        then putStrLn "Invalid program!" >> exitFailure
        -- else mapM_ putStrLn (interpret stmts)
        else compile stmts

-- String utils
split :: Eq a => [a] -> a -> ([a], [a])
split xs y = (takeWhile (/= y) xs, tail (dropWhile (/= y) xs))

trim :: String -> String
trim = dropWhile isSpace . reverse . dropWhile isSpace . reverse

-- A couple of programs
prog = "# An example of a program written in the lang programming language\n\nx = 1 + 2\ny = 1 + x\nprint y + x\nz = x + 1\nprint z"
invalid = "# An example of a program written in the lang programming language\n\nx = 1\ny = 1 + x\nprint y + a\nz = x + 1\nprint z"
