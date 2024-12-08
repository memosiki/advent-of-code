import Data.List.Split

main :: IO ()
main = do
  contents <- getContents
  print $ sum $ map validateGames (lines contents)

validateGames line =
  let [game_name, games] = splitOn ": " line
      [_, game_id] = words game_name
   in if all validate (splitOn ";" games)
        then read game_id
        else 0

validate game =
  let colors = splitOn ", " game
   in all validateColor colors

validateColor line =
  let [countL, color] = words line
      count = read countL :: Int
   in case color of
        "red" -> count <= max_red
        "green" -> count <= max_green
        "blue" -> count <= max_blue
  where
    max_red = 12
    max_green = 13
    max_blue = 14