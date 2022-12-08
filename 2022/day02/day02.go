package main

import (
	"fmt"
	"os"
)

type tuple[T comparable] struct {
	op, me T
}
type match tuple[string]

func main() {
	//	matchup := map[match]int{
	//		{"A", "X"}: 1 + 3,
	//		{"B", "X"}: 1 + 0,
	//		{"C", "X"}: 1 + 6,
	//		{"A", "Y"}: 2 + 6,
	//		{"B", "Y"}: 2 + 3,
	//		{"C", "Y"}: 2 + 0,
	//		{"A", "Z"}: 3 + 0,
	//		{"B", "Z"}: 3 + 6,
	//		{"C", "Z"}: 3 + 3,
	//	}
	matchup := map[match]int{
		{"A", "X"}: 0 + 3,
		{"B", "X"}: 0 + 1,
		{"C", "X"}: 0 + 2,
		{"A", "Y"}: 3 + 1,
		{"B", "Y"}: 3 + 2,
		{"C", "Y"}: 3 + 3,
		{"A", "Z"}: 6 + 2,
		{"B", "Z"}: 6 + 3,
		{"C", "Z"}: 6 + 1,
	}
	file, err := os.Open("input")
	if err != nil {
		panic(file)
	}
	var round match
	var score int
	_, err = fmt.Fscanln(file, &round.op, &round.me)
	for err == nil {
		score += matchup[round]
		_, err = fmt.Fscan(file, &round.op, &round.me)
	}
	println(score)
}
