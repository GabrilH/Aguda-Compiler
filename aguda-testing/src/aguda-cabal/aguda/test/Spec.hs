{-# LANGUAGE ScopedTypeVariables #-}
import Aguda ( aguda )
import Test.Hspec
import Test.HUnit
import System.Directory
import Control.Monad -- ( forM_ )
import System.FilePath ( isExtensionOf )
import Control.Exception 
import Data.List

baseDir, validTestDir, invalidTestDir :: FilePath

baseDir = "/Users/vv/workspace/aguda-testing/test/"
validTestDir = baseDir ++ "valid/"
invalidTestDir = baseDir ++ "invalid/"

main :: IO ()
main = hspec $ do
  -- valid
  describe "Valid Aguda Programs" $ do
    testDirs <- runIO $ listDirectory validTestDir
    forM_ (sort testDirs) $
      \dir -> getSource validTestDir dir >>= parses
  -- invalid
  describe "\nInvalid Aguda Programs" $ do
    testDirs <- runIO $ listDirectory invalidTestDir
    forM_ (sort testDirs) $
      \dir -> getSource invalidTestDir dir >>= parsesNot

parses :: FilePath -> SpecWith ()
parses filePath = do
  it filePath $ do
    ast <- aguda filePath
    catch (void $ evaluate ast) 
      (\(e :: ErrorCall) -> assertFailure (show e))
  
parsesNot :: FilePath -> SpecWith ()
parsesNot filePath = do
  it filePath $ do
    ast <- aguda filePath
    r <- try (evaluate ast)
    case r of
      Left (_ :: ErrorCall) -> return ()
      Right _ -> assertFailure "Expected an error but none was thrown."

-- getSource :: FilePath -> FilePath -> IO FilePath
getSource base dirName = do
  let filePath = base ++ dirName
  testFiles <- runIO $ listDirectory filePath
  let aguFiles = filter (".agu" `isExtensionOf`) testFiles
  case aguFiles of
    [] -> return $ error $ "No agu files found in folder " ++ dirName ++ "!"
    (f:_) -> return $ filePath ++ "/" ++ f
