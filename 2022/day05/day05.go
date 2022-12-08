package main

import (
	"fmt"
	"golang.org/x/exp/constraints"
	"os"
)

func reverse[G []T, T constraints.Ordered](container G) {
	for i, j := 0, len(container)-1; i < j; i, j = i+1, j-1 {
		container[i], container[j] = container[j], container[i]
	}
}
func main() {
	dock := [][]rune{
		/* Generated with get_init.py */
		{},
		{'S', 'Z', 'P', 'D', 'L', 'B', 'F', 'C'},
		{'N', 'V', 'G', 'P', 'H', 'W', 'B'},
		{'F', 'W', 'B', 'J', 'G'},
		{'G', 'J', 'N', 'F', 'L', 'W', 'C', 'S'},
		{'W', 'J', 'L', 'T', 'P', 'M', 'S', 'H'},
		{'B', 'C', 'W', 'G', 'F', 'S'},
		{'H', 'T', 'P', 'M', 'Q', 'B', 'W'},
		{'F', 'S', 'W', 'T'},
		{'N', 'C', 'R'},
		//				{'Z', 'N'}, {'M', 'C', 'D'}, {'P'},
	}
	file, _ := os.Open("input")
	defer file.Close()

	var amount, from, to int
	var err error
	for {
		// skip to moves
		_, err = fmt.Fscanf(file, "move %d from %d to %d\n", &amount, &from, &to)
		if err == nil {
			break
		}
	}
	for err == nil {
		offset := len(dock[from]) - amount
		//		reverse(dock[from][offset:])
		dock[to] = append(dock[to], dock[from][offset:]...)
		dock[from] = dock[from][:offset]
		// ex: move 25 from 2 to 4
		_, err = fmt.Fscanf(file, "move %d from %d to %d\n", &amount, &from, &to)
	}
	ans := make([]rune, len(dock)-1)
	for i, col := range dock[1:] {
		ans[i] = col[len(col)-1]
	}
	fmt.Println(dock)
	print(string(ans))
}
