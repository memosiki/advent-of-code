package main

import (
	"fmt"
	"sort"
)

// var items [][]int
// ops
//
//	func parseInput() {
//		file, _ := os.Open("input")
//		defer file.Close()
//		scanner := bufio.NewScanner(file)
//		var curMonkey int
//		for scanner.Scan() {
//			fmt.Fscanln(bytes.NewReader(scanner.Bytes()), "Monkey %d:", &curMonkey)
//			scanner.Scan()
//			itemsRow := bytes.NewReader(scanner.Bytes())
//			fmt.Fscan(itemsRow, "Starting items: ")
//			fmt.Fscan()
//		}
//	}

type Monkey struct {
	items []int
	op    func(int) int
	div   int
	next  [2]int
}

func (m Monkey) test(item int) int {
	if item%m.div == 0 {
		return 0
	}
	return 1
}
func mul(operand int) func(int) int {
	return func(x int) int {
		return x * operand
	}
}
func pow2() func(int) int {
	return func(x int) int {
		return x * x
	}
}
func add(operand int) func(int) int {
	return func(x int) int {
		return x + operand
	}
}

var monkeysTest = []Monkey{
	/*
		Monkey 0:
		  Starting items: 79, 98
		  Operation: new = old * 19
		  Test: divisible by 23
		    If true: throw to monkey 2
		    If false: throw to monkey 3

		Monkey 1:
		  Starting items: 54, 65, 75, 74
		  Operation: new = old + 6
		  Test: divisible by 19
		    If true: throw to monkey 2
		    If false: throw to monkey 0

		Monkey 2:
		  Starting items: 79, 60, 97
		  Operation: new = old * old
		  Test: divisible by 13
		    If true: throw to monkey 1
		    If false: throw to monkey 3

		Monkey 3:
		  Starting items: 74
		  Operation: new = old + 3
		  Test: divisible by 17
		    If true: throw to monkey 0
		    If false: throw to monkey 1
	*/
	{
		items: []int{79, 98},
		op:    mul(19),
		div:   23,
		next:  [2]int{2, 3},
	},
	{
		items: []int{54, 65, 75, 74},
		op:    add(6),
		div:   19,
		next:  [2]int{2, 0},
	},
	{
		items: []int{79, 60, 97},
		op:    pow2(),
		div:   13,
		next:  [2]int{1, 3},
	},
	{
		items: []int{74},
		op:    add(3),
		div:   17,
		next:  [2]int{0, 1},
	},
}

var monkeyProd = []Monkey{
	/*
		Monkey 0:
		  Starting items: 91, 66
		  Operation: new = old * 13
		  Test: divisible by 19
		    If true: throw to monkey 6
		    If false: throw to monkey 2

		Monkey 1:
		  Starting items: 78, 97, 59
		  Operation: new = old + 7
		  Test: divisible by 5
		    If true: throw to monkey 0
		    If false: throw to monkey 3

		Monkey 2:
		  Starting items: 57, 59, 97, 84, 72, 83, 56, 76
		  Operation: new = old + 6
		  Test: divisible by 11
		    If true: throw to monkey 5
		    If false: throw to monkey 7

		Monkey 3:
		  Starting items: 81, 78, 70, 58, 84
		  Operation: new = old + 5
		  Test: divisible by 17
		    If true: throw to monkey 6
		    If false: throw to monkey 0

		Monkey 4:
		  Starting items: 60
		  Operation: new = old + 8
		  Test: divisible by 7
		    If true: throw to monkey 1
		    If false: throw to monkey 3

		Monkey 5:
		  Starting items: 57, 69, 63, 75, 62, 77, 72
		  Operation: new = old * 5
		  Test: divisible by 13
		    If true: throw to monkey 7
		    If false: throw to monkey 4

		Monkey 6:
		  Starting items: 73, 66, 86, 79, 98, 87
		  Operation: new = old * old
		  Test: divisible by 3
		    If true: throw to monkey 5
		    If false: throw to monkey 2

		Monkey 7:
		  Starting items: 95, 89, 63, 67
		  Operation: new = old + 2
		  Test: divisible by 2
		    If true: throw to monkey 1
		    If false: throw to monkey 4
	*/
	{
		items: []int{91, 66},
		op:    mul(13),
		div:   19,
		next:  [2]int{6, 2},
	},
	{
		items: []int{78, 97, 59},
		op:    add(7),
		div:   5,
		next:  [2]int{0, 3},
	},
	{
		items: []int{57, 59, 97, 84, 72, 83, 56, 76},
		op:    add(6),
		div:   11,
		next:  [2]int{5, 7},
	},
	{
		items: []int{81, 78, 70, 58, 84},
		op:    add(5),
		div:   17,
		next:  [2]int{6, 0},
	},
	{
		items: []int{60},
		op:    add(8),
		div:   7,
		next:  [2]int{1, 3},
	},
	{
		items: []int{57, 69, 63, 75, 62, 77, 72},
		op:    mul(5),
		div:   13,
		next:  [2]int{7, 4},
	},
	{
		items: []int{73, 66, 86, 79, 98, 87},
		op:    pow2(),
		div:   3,
		next:  [2]int{5, 2},
	},
	{
		items: []int{95, 89, 63, 67},
		op:    add(2),
		div:   2,
		next:  [2]int{1, 4},
	},
}

func main() {
	monkeys := monkeyProd
	var lcm int = 1
	for i := range monkeys {
		lcm = LCM(lcm, monkeys[i].div)
	}
	inspections := make([]int, len(monkeys))
	for round := 0; round < 10000; round++ {
		for i, monkey := range monkeys {
			inspections[i] += len(monkey.items)
			for _, item := range monkey.items {
				worry := monkey.op(item) % lcm
				next := monkey.next[monkey.test(worry)]
				monkeys[next].items = append(monkeys[next].items, worry)
			}
			monkeys[i].items = monkey.items[:0]
		}
	}
	fmt.Printf("%v\n", monkeys)
	fmt.Println(inspections)
	sort.Sort(sort.Reverse(sort.IntSlice(inspections)))
	fmt.Println(inspections[:2], uint64(inspections[0])*uint64(inspections[1]))
}

func GCD(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func LCM(a, b int) int {
	return a * b / GCD(a, b)
}
