package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
)

const sourceX, sourceY = 500, 0

var occupied [1000][1000]bool
var FarthestPoint int

func fill(xStart, xEnd, yStart, yEnd int) {
	xStart, xEnd = Min(xStart, xEnd), Max(xStart, xEnd)
	yStart, yEnd = Min(yStart, yEnd), Max(yStart, yEnd)
	for i := xStart; i <= xEnd; i++ {
		for j := yStart; j <= yEnd; j++ {
			occupied[i][j] = true
		}
	}
	FarthestPoint = Max(FarthestPoint, yEnd)
}
func fall() {
	x, y := sourceX, sourceY
fallingLoop:
	for {
		switch {
		case y == FarthestPoint+1:
			break fallingLoop
		case !occupied[x][y+1]:
			y = y + 1
		case !occupied[x-1][y+1]:
			x, y = x-1, y+1
		case !occupied[x+1][y+1]:
			x, y = x+1, y+1
		default:
			break fallingLoop
		}
	}
	occupied[x][y] = true
}

func main() {
	// input parsing
	file, err := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var x, y, xNext, yNext int
	for scanner.Scan() {
		line := bytes.NewReader(scanner.Bytes())

		firstScan := true
		err = nil
		for err == nil {
			x, y = xNext, yNext
			_, err = fmt.Fscanf(line, "%d,%d", &xNext, &yNext)
			_, err = fmt.Fscanf(line, " -> ")

			if firstScan {
				firstScan = false
				continue
			}
			fill(x, xNext, y, yNext)
		}
	}

	// simulation
	var sandShards int
	for ; !occupied[sourceX][sourceY]; sandShards++ {
		fall()
	}
	fmt.Println(sandShards)
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
