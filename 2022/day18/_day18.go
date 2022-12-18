package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/emirpasic/gods/sets/hashset"
	"os"
)

type Side struct {
	x1, y1, z1 int // two points representing a side of a cube
	x2, y2, z2 int // coordinates should be in an increasing order
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)

	set := hashset.New()
	var x, y, z int
	for scanner.Scan() {
		_, _ = fmt.Fscanf(
			bytes.NewReader(scanner.Bytes()),
			"%d,%d,%d\n",
			&x,
			&y,
			&z,
		)
		sides := []Side{
			Side{x, y, z, x + 1, y, z + 1},
			Side{x, y + 1, z, x + 1, y + 1, z + 1},
			Side{x, y, z, x, y + 1, z + 1},
			Side{x + 1, y, z, x + 1, y + 1, z + 1},
			Side{x, y, z, x + 1, y + 1, z},
			Side{x, y, z + 1, x + 1, y + 1, z + 1},
		}
		for _, side := range sides {
			if set.Contains(side) {
				set.Remove(side)
			} else {
				set.Add(side)
			}
		}
	}
	fmt.Println("Not connected sides", set.Size())
}
