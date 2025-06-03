module Main ( main ) where

import Aguda
import qualified System.Environment as SE

main :: IO ()
main = do
  (filename:_) <- SE.getArgs
  ast <- aguda filename
  print ast
  
  
