package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/emirpasic/gods/queues/arrayqueue"
	"github.com/emirpasic/gods/sets/hashset"
	"os"
)

type Side struct {
	x1, y1, z1 int // two points representing a side of a cube
	x2, y2, z2 int // coordinates should be in an increasing order
}

type Cube struct {
	x, y, z int
}

const (
	MaxCoord     = 19 // calculated with parseinput.py
	MinCoord     = 0  // --
	offset       = 1
	bbsizeoffset = offset + 1                         // adding +1 from two sides for additional layer of air around the bounding box
	BBsize       = MaxCoord - MinCoord + bbsizeoffset // bounding box size
)

func main() {
	file, _ := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var visited [BBsize][BBsize][BBsize]bool

	var x, y, z int
	var dropletCubes, pocketCubes = hashset.New(), hashset.New()
	for scanner.Scan() {
		_, _ = fmt.Fscanf(
			bytes.NewReader(scanner.Bytes()),
			"%d,%d,%d\n",
			&x,
			&y,
			&z,
		)
		visited[x+offset][y+offset][z+offset] = true
		dropletCubes.Add(Cube{x + offset, y + offset, z + offset})
	}
	queue := arrayqueue.New()
	queue.Enqueue(Cube{0, 0, 0}) // 0,0,0 guaranteed to be outside droplet because of offset
	visited[0][0][0] = true
	// bfs
	for !queue.Empty() {
		qcube, _ := queue.Dequeue()
		cube := qcube.(Cube)
		x, y, z := cube.x, cube.y, cube.z

		if x-1 >= 0 && !visited[x-1][y][z] {
			visited[x-1][y][z] = true
			queue.Enqueue(Cube{x - 1, y, z})
		}
		if x+1 < BBsize && !visited[x+1][y][z] {
			visited[x+1][y][z] = true
			queue.Enqueue(Cube{x + 1, y, z})
		}
		if y-1 >= 0 && !visited[x][y-1][z] {
			visited[x][y-1][z] = true
			queue.Enqueue(Cube{x, y - 1, z})
		}
		if y+1 < BBsize && !visited[x][y+1][z] {
			visited[x][y+1][z] = true
			queue.Enqueue(Cube{x, y + 1, z})
		}
		if z-1 >= 0 && !visited[x][y][z-1] {
			visited[x][y][z-1] = true
			queue.Enqueue(Cube{x, y, z - 1})
		}
		if z+1 < BBsize && !visited[x][y][z+1] {
			visited[x][y][z+1] = true
			queue.Enqueue(Cube{x, y, z + 1})
		}
	}
	for i := 0; i < BBsize; i++ {
		for j := 0; j < BBsize; j++ {
			for k := 0; k < BBsize; k++ {
				if !visited[i][j][k] {
					pocketCubes.Add(Cube{i, j, k})
				}
			}
		}
	}

	fmt.Println("Not connected sides", findArea(dropletCubes))
	fmt.Println("Area without pockets", findArea(dropletCubes)-findArea(pocketCubes))
}

func findArea(cubes *hashset.Set) int {
	seen := hashset.New()
	for _, scube := range cubes.Values() {
		cube := scube.(Cube)
		x, y, z := cube.x, cube.y, cube.z
		sides := []Side{
			Side{x, y, z, x + 1, y, z + 1},
			Side{x, y + 1, z, x + 1, y + 1, z + 1},
			Side{x, y, z, x, y + 1, z + 1},
			Side{x + 1, y, z, x + 1, y + 1, z + 1},
			Side{x, y, z, x + 1, y + 1, z},
			Side{x, y, z + 1, x + 1, y + 1, z + 1},
		}
		for _, side := range sides {
			if seen.Contains(side) {
				seen.Remove(side)
			} else {
				seen.Add(side)
			}
		}
	}
	return seen.Size()
}
