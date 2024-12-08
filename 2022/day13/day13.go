package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sort"
)

type Node = []any
type NodeLeaf = float64

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	var expressions = make([]Node, 0)
	scanner := bufio.NewScanner(file)

	for idx := 1; scanner.Scan(); idx++ {
		var expr Node
		err := json.Unmarshal(scanner.Bytes(), &expr)
		if err != nil {
			log.Fatalln(err)
		}
		expressions = append(expressions, expr)

		if idx%2 == 0 {
			scanner.Scan()
		}

	}

	var divider1, divider2 Node
	_ = json.Unmarshal([]byte("[[2]]"), &divider1)
	_ = json.Unmarshal([]byte("[[6]]"), &divider2)
	expressions = append(expressions, divider1, divider2)

	sort.Slice(expressions, func(i, j int) bool {
		var ans = make(chan bool)
		defer close(ans)
		go isCorrectOrder(expressions[i], expressions[j], ans)
		return <-ans
	})

	fmt.Println(expressions)
	for i := 0; i < len(expressions); i++ {
		if same(expressions[i], divider1) {
			fmt.Println("divider1", i+1)
		}

		if same(expressions[i], divider2) {
			fmt.Println("divider2", i+1)
		}
	}
}

const MaxRecursion = 10_000

func same(lhs, rhs any) bool {
	var ans = make(chan bool, MaxRecursion)
	defer close(ans)
	isCorrectOrder(lhs, rhs, ans)
	return len(ans) == 0
}
func isCorrectOrder(lhs, rhs any, cmp chan<- bool) {
	defer func() { recover() }()
	leafLhs, leafLhsOk := lhs.(NodeLeaf)
	leafRhs, leafRhsOk := rhs.(NodeLeaf)
	listLhs, listLhsOk := lhs.(Node)
	listRhs, listRhsOk := rhs.(Node)
	switch {
	case leafLhsOk && leafRhsOk:
		if leafLhs != leafRhs {
			cmp <- leafLhs < leafRhs
		}
	case listLhsOk && listRhsOk:
		for i := range listLhs {
			if i >= len(listRhs) {
				cmp <- false
				break
			}
			isCorrectOrder(listLhs[i], listRhs[i], cmp)
		}
		if len(listLhs) < len(listRhs) {
			cmp <- true
		}
	case leafLhsOk:
		isCorrectOrder(Node{leafLhs}, rhs, cmp)
	case leafRhsOk:
		isCorrectOrder(lhs, Node{leafRhs}, cmp)
	}
}
