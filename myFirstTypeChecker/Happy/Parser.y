{
{- |
Module      :  Lexer
Description :  Lexer for the Simple programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Vasco T. Vasconcelos
-}

module Parser (parse) where

import Lexer
import Syntax
}

%name parse
%tokentype { Token }
%error { parseError }

%token
    let  { TokenLet _ }
    in   { TokenIn _ }
    if   { TokenIf _ }
    then { TokenThen _ }
    else { TokenElse _ }
    int  { TokenInt _ $$ }
    bool { TokenBool _ $$ }
    var  { TokenId _ $$ }
    '='  { TokenEq _ }
    '+'  { TokenPlus _ }
    '*'  { TokenTimes _ }
    '&&' { TokenAnd _ }
    '||' { TokenOr _ }
    not  { TokenNot _ }
    '('  { TokenLParen _ }
    ')'  { TokenRParen _ }

%right in
%right else
%left '||'
%left '&&'
%left not
%left '+'
%left '+'
%left '*'

%%

Exp : int                      { IntLit $1 }
    | bool                     { BoolLit $1 }
    | var                      { Var $1 }
    | let var '=' Exp in Exp   { Let $2 $4 $6 }
    | if Exp then Exp else Exp { Cond $2 $4 $6 }
    | Exp '+' Exp              { Plus $1 $3 }
    | Exp '*' Exp              { Times $1 $3 }
    | Exp '&&' Exp             { And $1 $3 }
    | Exp '||' Exp             { Or $1 $3 }
    | Exp not Exp              { Not $1 }
    | '(' Exp ')'              { $2 }

{

parseError :: [Token] -> a
parseError (t:_) = error $ "Parse error at " ++ (show t)

}
