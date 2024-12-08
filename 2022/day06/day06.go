package main

import (
	"bufio"
	"fmt"
	"golang.org/x/exp/constraints"
	"os"
)

const PACKET_SIZE = 14

func isUnique(window []byte) bool {
	return NewCounter(string(window)).IsUnique()
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanBytes)
	var ind = PACKET_SIZE
	var letter byte
	var window = make([]byte, PACKET_SIZE)
	for i := 0; i < PACKET_SIZE; i++ {
		scanner.Scan()
		window[i] = scanner.Bytes()[0]
	}
	if isUnique(window) {
		fmt.Println(ind)
		return
	}
	for scanner.Scan() {
		letter = scanner.Bytes()[0]
		window = append(window[1:], letter)
		ind++
		if isUnique(window) {
			fmt.Println(ind)
			break
		}
	}
}

// Counter -- это реализация collections.Counter из Python для строк
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
func (counter Counter) Intersection(other Counter) (counts Counter) {
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

// GetAny возвращает произвольный элемент
func (counter Counter) GetAny() (key rune, value int, ok bool) {
	for k, val := range counter {
		return k, val, true
	}
	return 0, 0, false
}

// IsUnique возвращает true если символы в counter уникальны
func (counter Counter) IsUnique() bool {
	for _, count := range counter {
		if count > 1 {
			return false
		}
	}
	return true
}
