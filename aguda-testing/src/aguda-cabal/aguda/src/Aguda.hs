module Aguda ( aguda ) where

data Program = Program
  deriving Show

aguda :: FilePath -> IO Program
aguda filename = do
  return Program

