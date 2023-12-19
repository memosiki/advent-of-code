import Data.List
import Data.Map qualified as Map
import Data.Maybe

safeMaximum :: (Ord a, Bounded a) => [a] -> a
safeMaximum [] = minBound
safeMaximum x = maximum x

safeMinimum :: (Ord a, Bounded a) => [a] -> a
safeMinimum [] = maxBound
safeMinimum x = minimum x

search :: (Eq a) => [a] -> [a] -> [Int]
search haystack needle = findIndices (isPrefixOf needle) (tails haystack)

calibrate :: (Num a, Enum a) => [Char] -> a
calibrate line = 
  let lookup x = (x, search line x)
      findings = map lookup patterns
      leftPattern = snd $ minimum [(safeMinimum pos, key) | (key, pos) <- findings]
      rightPattern = snd $ maximum [(safeMaximum pos, key) | (key, pos) <- findings]
      left = fromJust $ Map.lookup leftPattern spell
      right = fromJust $ Map.lookup rightPattern spell
  in left * 10 + right
  where
    patterns = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"] ++ map show [1 .. 9]
    spell = Map.fromList $ zip patterns (cycle [1 .. 9])

main :: IO ()
main = do
  input <- getContents
  print $ sum $ map calibrate (lines input)
