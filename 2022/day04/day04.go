package main

import (
	"fmt"
	"os"
)

type pair struct {
	s, f int // start, finish
}

func toInt(a bool) int {
	if a {
		return 1
	}
	return 0
}

func contains(a, b pair) int {
	return map[bool]int{false: 0, true: 1}[a.s <= b.s && a.f >= b.f || b.s <= a.s && b.f >= a.f]
}
func overlap(a, b pair) bool {
	return a.s <= b.s && a.f >= b.s || b.s <= a.s && b.f >= a.s
}
func main() {
	file, _ := os.Open("input")
	defer file.Close()

	var count int
	var elf1, elf2 pair
	_, err := fmt.Fscanf(file, "%d-%d,%d-%d", &elf1.s, &elf1.f, &elf2.s, &elf2.f)
	for err == nil {
		count += toInt(overlap(elf1, elf2))
		_, err = fmt.Fscanf(file, "%d-%d,%d-%d", &elf1.s, &elf1.f, &elf2.s, &elf2.f)
	}
	print(count)
}
