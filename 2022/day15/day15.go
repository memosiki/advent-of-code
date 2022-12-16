package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/emirpasic/gods/sets/hashset"
	"log"
	"os"
)

const (
	lookupRow      = 2_000_000
	searchBoundary = 4_000_000
	//lookupRow      = 10
	//searchBoundary = 20
)

type Sensor struct {
	x, y   int // position
	radius int // distance to closest beacon
}

func Abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}
func Max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
func (s Sensor) covers(x, y int) bool {
	return Abs(s.x-x)+Abs(s.y-y) <= s.radius
}
func (s Sensor) leaveInfluence(y int) int {
	return s.x + (s.radius - Abs(y-s.y))
}

func main() {
	file, err := os.Open("input")
	defer file.Close()

	var sensors []Sensor
	var interceptingBeacons = hashset.New()
	scanner := bufio.NewScanner(file)
	var x, y, xB, yB int
	var leftBound, rightBound int
	for scanner.Scan() {
		_, err = fmt.Fscanf(bytes.NewReader(scanner.Bytes()), "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d\n", &x, &y, &xB, &yB)
		if err != nil {
			log.Panicln(err)
		}
		dist := Abs(x-xB) + Abs(y-yB)
		sensors = append(sensors, Sensor{x, y, dist})
		leftBound = Min(leftBound, x-dist)
		rightBound = Max(rightBound, x+dist)
		if yB == lookupRow {
			interceptingBeacons.Add(xB)
		}
	}
	coverage := make([]bool, rightBound-leftBound)
	fmt.Println("boundaries", leftBound, rightBound)
	for i := leftBound; i <= rightBound; i++ {
		for _, sensor := range sensors {
			if sensor.covers(i, lookupRow) {
				//fmt.Println(i, "covered by", sensor)
				coverage[i-leftBound] = true
			}
		}
	}
	var totalCovered int
	for _, covered := range coverage {
		if covered {
			totalCovered++
		}
	}
	totalCovered -= interceptingBeacons.Size()
	fmt.Println("total covered spaces", totalCovered)

searchLoop:
	for y := 0; y <= searchBoundary; y++ {
	nextCell:
		for x := 0; x <= searchBoundary; x++ {
			for _, sensor := range sensors {
				if sensor.covers(x, y) {
					x = sensor.leaveInfluence(y)
					continue nextCell
				}
			}
			fmt.Println("beacon at", x, y, searchBoundary*x+y)
			break searchLoop
		}
	}
}
