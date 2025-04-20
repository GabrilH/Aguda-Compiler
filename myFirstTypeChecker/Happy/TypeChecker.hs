{- |
Module      :  TypeChecker
Description :  A type checker for the Simple programming language
Copyright   :  Técnicas de Compilação
               Mestrado em Engenharia Informática
               Faculdade de Ciências
               Universidade de Lisboa
               2024/2025
               Vasco T. Vasconcelos
-}

module TypeChecker (typeof) where

import Syntax
import qualified Data.Map.Strict as Map

type Ctx = Map.Map String Type -- Symbol Table

type Error = String

typeof :: Ctx -> Exp -> Either Error Type
typeof _ (IntLit _) = Right IntType
typeof _ (BoolLit _) = Right BoolType
typeof ctx (Var v) =
  typeofVar ctx v
typeof ctx (Let s e1 e2) = do
  t <- typeof ctx e1
  typeof (Map.insert s t ctx) e2
typeof ctx (Cond e1 e2 e3) = do
  _ <- checkAgainst ctx e1 BoolType
  t2 <- typeof ctx e2
  t3 <- typeof ctx e3
  _ <- checkEqualTypes t2 t3
  return t2
typeof ctx (Plus e1 e2) = do
  _ <- checkAgainst ctx e1 IntType
  _ <- checkAgainst ctx e2 IntType
  Right IntType
typeof ctx (Times e1 e2) = do
  _ <- checkAgainst ctx e1 IntType
  _ <- checkAgainst ctx e2 IntType
  Right IntType
typeof ctx (And e1 e2) = do
  _ <- checkAgainst ctx e1 BoolType
  _ <- checkAgainst ctx e2 BoolType
  return BoolType
typeof ctx (Or e1 e2) = do
  _ <- checkAgainst ctx e1 BoolType
  _ <- checkAgainst ctx e2 BoolType
  return BoolType

checkAgainst :: Ctx -> Exp -> Type -> Either Error ()
checkAgainst _ (IntLit _) IntType = Right ()
checkAgainst _ (BoolLit _) BoolType = Right ()
checkAgainst ctx (Var v) t = do
  u <- typeofVar ctx v
  checkEqualTypes t u
checkAgainst ctx (Let s e1 e2) t = do
  u <- typeof ctx e1
  checkAgainst (Map.insert s u ctx) e2 t
checkAgainst ctx (Plus e1 e2) IntType = do
  _ <- checkAgainst ctx e1 IntType
  _ <- checkAgainst ctx e2 IntType
  Right ()
checkAgainst ctx (Times e1 e2) IntType = do
  _ <- checkAgainst ctx e1 IntType
  _ <- checkAgainst ctx e2 IntType
  Right ()
checkAgainst ctx (And e1 e2) BoolType = do
  _ <- checkAgainst ctx e1 BoolType
  _ <- checkAgainst ctx e2 BoolType
  Right ()
checkAgainst ctx (Or e1 e2) BoolType = do
  _ <- checkAgainst ctx e1 BoolType
  _ <- checkAgainst ctx e2 BoolType
  Right ()
checkAgainst ctx (Not e) BoolType = do
  _ <- checkAgainst ctx e BoolType
  Right ()
checkAgainst ctx e t = Left $
  "Expecting type " ++ show t ++
  ", found type " ++ show (typeof ctx e) ++
  " for expression " ++ show e

typeofVar :: Ctx -> String -> Either Error Type
typeofVar ctx v =
  case ctx Map.!? v of
    Just t -> Right t
    Nothing -> Left $ "Unresolved symbol: " ++ v

checkEqualTypes :: Type -> Type -> Either Error ()
checkEqualTypes t u
  | t == u = Right ()
  | otherwise = Left $ "Expecting equal types, found " ++ show t ++ " and " ++ show u
