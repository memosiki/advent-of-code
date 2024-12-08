package main

import (
	"bufio"
	"fmt"
	"github.com/boljen/go-bitmap"
	"os"
	"strconv"
	"strings"
)

const Debug = false // print debugging information
const (
	padding = 10_000 // adjust manually
)

const Rounds = 1000

type Direction int8

func (direction Direction) String() string {
	switch direction {
	case North:
		return "North"
	case South:
		return "South"
	case West:
		return "West"
	case East:
		return "East"
	default:
		panic(direction)
	}
}

const (
	North Direction = iota
	South
	West
	East
)

var directions = []Direction{North, South, West, East}

type Stage []bitmap.Bitmap

func indexOf[Element comparable](data []Element, element Element) int {
	for k, v := range data {
		if element == v {
			return k
		}
	}
	return -1 //not found.
}
func (stage Stage) Print(elves []Position) {
	if Debug {
		var builder strings.Builder
		for i, bm := range stage {
			for j := 0; j < bm.Len(); j++ {
				if bm.Get(j) {
					const maxIdx = 36                              //= len(strconv.digits)
					idx := indexOf(elves, Position{i, j}) % maxIdx // index of elf
					aidx := strconv.FormatInt(int64(idx), 36)      // single alphanumeric index of elf
					builder.WriteString(aidx)
				} else {
					builder.WriteByte('.')
				}
			}
			builder.WriteByte('\n')
		}
		debug(builder.String())
	}
}

type Position struct {
	x, y int
}

func debug(a ...any) {
	if Debug {
		fmt.Println(a...)
	}
}
func (pos Position) Lonesome(stage Stage) bool {
	return !(stage[pos.x-1].Get(pos.y-1) || stage[pos.x].Get(pos.y-1) || stage[pos.x+1].Get(pos.y-1) ||
		stage[pos.x-1].Get(pos.y+1) || stage[pos.x].Get(pos.y+1) || stage[pos.x+1].Get(pos.y+1) ||
		stage[pos.x-1].Get(pos.y) || stage[pos.x+1].Get(pos.y))
}
func (pos Position) Occupied(direction Direction, stage Stage) bool {
	switch direction {
	case North:
		line := stage[pos.x-1]
		return line.Get(pos.y-1) || line.Get(pos.y) || line.Get(pos.y+1)
	case South:
		line := stage[pos.x+1]
		return line.Get(pos.y-1) || line.Get(pos.y) || line.Get(pos.y+1)
	case West:
		column := pos.y - 1
		return stage[pos.x-1].Get(column) || stage[pos.x].Get(column) || stage[pos.x+1].Get(column)
	case East:
		column := pos.y + 1
		return stage[pos.x-1].Get(column) || stage[pos.x].Get(column) || stage[pos.x+1].Get(column)
	default:
		panic(direction)
	}
}
func (pos Position) Move(direction Direction) Position {
	switch direction {
	case North:
		return Position{pos.x - 1, pos.y}
	case South:
		return Position{pos.x + 1, pos.y}
	case West:
		return Position{pos.x, pos.y - 1}
	case East:
		return Position{pos.x, pos.y + 1}
	default:
		panic(direction)
	}
}
func (pos *Position) Update(newPos Position, stage Stage) {
	stage[pos.x].Set(pos.y, false)      // remove old position
	stage[newPos.x].Set(newPos.y, true) // add new position
	pos.x, pos.y = newPos.x, newPos.y
}
func main() {
	file, _ := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var ( // sizes of initial grid, input manually
		height int
		width  int
	)
	for scanner.Scan() {
		width = len(scanner.Bytes())
		height++
	}
	var ( // sizes of stage with padding, so elves can move oob
		verticalBound   = padding + height + padding
		horizontalBound = padding + width + padding
	)
	fmt.Println(width, height)
	_, _ = file.Seek(0, 0)
	scanner = bufio.NewScanner(file)

	stage := make(Stage, verticalBound)
	var elves []Position
	for i := 0; i < verticalBound; i++ {
		stage[i] = bitmap.New(horizontalBound)
	}
	for i := 0; scanner.Scan(); i++ {
		for k, char := range scanner.Text() {
			if char == '#' {
				stage[padding+i].Set(padding+k, true)
				elves = append(elves, Position{padding + i, padding + k})
			}
		}
	}

	newPosition := make([]Position, len(elves))
	var InvalidPosition = Position{0, 0} // used as a marker of wrong position
	for round := 0; round < Rounds; round++ {
		if round%100 == 0 {
			fmt.Println("Round", round+1)
		}
		stage.Print(elves)
		occupants := map[Position]int{} // invalid position always occupied
		for i, elf := range elves {
			found := false
			var direction Direction
			if !elf.Lonesome(stage) {
				for j := range directions {
					direction = directions[(round+j)%len(directions)]
					if !elf.Occupied(direction, stage) {
						found = true
						break
					}
				}
			}
			if found {
				newPosition[i] = elf.Move(direction)
				debug("Elf", i, "moving to", direction)
			} else {
				newPosition[i] = InvalidPosition
				debug("Elf", i, "no prediction")
			}
			occupants[newPosition[i]]++
		}
		// none of the elves moved
		if occupants[InvalidPosition] == len(elves) {
			fmt.Println("All elves stable at", round+1)
			break
		}
		for i, newPos := range newPosition {
			if newPos != InvalidPosition && occupants[newPos] == 1 {
				elves[i].Update(newPos, stage)
			}
		}
	}
	stage.Print(elves)

	// calculate bounding rectangle
	var westward, eastward, northward, southward int
	westward = horizontalBound
	northward = verticalBound
	for i := 0; i < verticalBound; i++ {
		for j := 0; j < horizontalBound; j++ {
			if stage[i].Get(j) {
				southward = Max2(southward, i)
				westward = Min2(westward, j)
				eastward = Max2(eastward, j)
				northward = Min2(northward, i)
			}
		}
	}
	var freeSpaces int
	for i := northward; i <= southward; i++ {
		for j := westward; j <= eastward; j++ {
			if !stage[i].Get(j) {
				freeSpaces++
			}
		}
	}
	fmt.Println("Free spaces in bb", freeSpaces)
}

func Max2(a, b int) int {
	if a > b {
		return a
	}
	return b
}
func Min2(a, b int) int {
	if a < b {
		return a
	}
	return b
}
