package main

import (
	"fmt"
	"golang.org/x/exp/constraints"
	"os"
)

func getPriority(elem rune) int {
	if elem >= 'A' && elem <= 'Z' {
		return int(elem - 'A' + 27)
	}
	return int(elem - 'a' + 1)
}
func main() {
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	var elf1, elf2, elf3 string

	var overall int
	_, err = fmt.Fscan(file, &elf1, &elf2, &elf3)
	for err == nil {
		elem, _, _ := NewCounter(elf1).Difference(NewCounter(elf2)).Difference(NewCounter(elf3)).GetAny()
		overall += getPriority(elem)
		fmt.Println(string(elem), getPriority(elem), overall)
		_, err = fmt.Fscan(file, &elf1, &elf2, &elf3)
	}
	println(overall)
}

// Counter
type Counter map[rune]int

func NewCounter(s string) Counter {
	counts := make(map[rune]int)
	var letter rune
	for _, letter = range s {
		if _, ok := counts[letter]; ok {
			counts[letter] += 1
		} else {
			counts[letter] = 1
		}
	}
	return counts
}
func (counter Counter) Copy() Counter {
	counts := make(map[rune]int)
	for k, v := range counter {
		counts[k] = v
	}
	return counts
}
func min[T constraints.Ordered](a, b T) T {
	if a < b {
		return a
	}
	return b
}

func (counter Counter) Difference(other Counter) (counts Counter) {
	counts = make(map[rune]int)
	for key, value := range counter {
		if min := min(value, other.Get(key)); min > 0 {
			counts[key] = min
		}
	}
	return
}
func (counter Counter) Get(key rune) (value int) {
	value, ok := counter[key]
	if !ok {
		return 0
	}
	return
}
func (counter Counter) Add(key rune, increment int) {
	if _, ok := counter[key]; ok {
		counter[key] += increment
	} else {
		counter[key] = increment
	}
}
func (counter Counter) GetAny() (key rune, value int, ok bool) {
	for k, val := range counter {
		return k, val, true
	}
	return 0, 0, false
}
