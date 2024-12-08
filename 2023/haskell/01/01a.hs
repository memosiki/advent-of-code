import Data.Char (isDigit)

main :: IO ()
main = do
  input <- getContents
  let inputData = lines input
  let calibrate = sum . map calibrateLine
  print $ calibrate inputData

calibrateLine :: [Char] -> Int
calibrateLine line =
  read [head numbers, last numbers] :: Int
  where
    numbers = filter isDigit line
