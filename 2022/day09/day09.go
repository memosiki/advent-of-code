package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/emirpasic/gods/sets/hashset"
	"golang.org/x/exp/constraints"
	"os"
)

type Knot struct {
	x, y int
}

func (knot *Knot) move(dir string) {
	if dir == "R" {
		knot.x += 1
	} else if dir == "L" {
		knot.x -= 1
	} else if dir == "U" {
		knot.y += 1
	} else if dir == "D" {
		knot.y -= 1
	}
}
func abs[T constraints.Signed](a T) T {
	var zero T
	if zero > a {
		return -a
	}
	return a
}
func sign[T constraints.Signed](a T) T {
	if 0 > a {
		return -1
	} else if 0 < a {
		return +1
	}
	return 0
}
func (knot *Knot) isTouching(other Knot) bool {
	return abs(knot.x-other.x) <= 1 && abs(knot.y-other.y) <= 1
}
func (knot *Knot) follow(followee Knot) {
	if knot.isTouching(followee) {
		return
	}
	knot.x += sign(followee.x - knot.x)
	knot.y += sign(followee.y - knot.y)
}

const TotalKnots = 10

func main() {
	var knots = make([]Knot, TotalKnots)
	var head, tail *Knot = &knots[0], &knots[len(knots)-1]
	var dir string
	var steps int
	visited := hashset.New(*head)

	file, _ := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		_, _ = fmt.Fscan(bytes.NewReader(scanner.Bytes()), &dir, &steps)
		for i := 0; i < steps; i++ {
			head.move(dir)
			for j := 1; j < len(knots); j++ {
				knots[j].follow(knots[j-1])
			}
			visited.Add(*tail)
		}
	}
	fmt.Println(visited.Size())
}
