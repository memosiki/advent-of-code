package main

import (
	"fmt"
)

const (
	AgeAfterReborn   = 6
	AgeAfter1stBirth = 8
)

var overall int

// todo: cache
func countReborns(daysLeft int) {
	if daysLeft < 0 {
		return
	}
	// count all the children
	for ; daysLeft >= 0; daysLeft -= AgeAfterReborn {
		overall += 1
		countReborns(daysLeft - AgeAfter1stBirth)
	}
}

const TotalDays = 8

var fishes = []int{3, 4, 3, 1, 2}

func main() {
	overall += len(fishes)
	for _, fishAge := range fishes {
		countReborns(TotalDays - fishAge)
	}
	fmt.Println("All the fishies", overall)
}
