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

calibrate line = do
  let lookup x = (x, search line x)
  let findings = map lookup patterns
  let leftPattern = snd $ minimum [(safeMinimum pos, key) | (key, pos) <- findings]
  let rightPattern = snd $ maximum [(safeMaximum pos, key) | (key, pos) <- findings]
  let left = fromJust $ Map.lookup leftPattern spell
  let right = fromJust $ Map.lookup rightPattern spell
  left * 10 + right
  where
    patterns = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"] ++ map show [1 .. 9]
    spell = Map.fromList $ zip patterns (cycle [1 .. 9])

main :: IO ()
main = do
  input <- getContents
  print $ sum $ map calibrate (lines input)
