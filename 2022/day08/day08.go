package main

import (
	"bufio"
	"fmt"
	"golang.org/x/exp/constraints"
	"os"
)

func abs[T constraints.Integer](a T) T {
	var zero T
	if a < zero {
		return -a
	}
	return a
}
func max[T constraints.Ordered](a ...T) (ans T) {
	ans = a[0]
	for _, elem := range a {
		if elem > ans {
			ans = elem
		}
	}
	return
}
func mul[T constraints.Integer](a ...T) (product T) {
	product = 1
	for _, elem := range a {
		product *= elem
	}
	return
}

func isCovered(a, b byte) int {
	if b >= a {
		return 1
	}
	return 0
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var forest [][]byte
	for scanner.Scan() {
		scanline := scanner.Bytes()
		row := make([]byte, len(scanline))
		copy(row, scanline)
		forest = append(forest, row)
	}
	n := len(forest)
	m := len(forest[0])
	covers := make([][]int, n)
	for i := range covers {
		covers[i] = make([]int, m)
	}
	type incFunc = func(int, int) (int, int)
	lookup := func(i0, j0 int, incInner, incOuter incFunc) {
		i, j := i0, j0
		for i >= 0 && i < n && j >= 0 && j < m {
			var maxH byte = 0
			for i >= 0 && i < n && j >= 0 && j < m {
				forest[i][j] = forest[i][j] - '0'
				covers[i][j] += isCovered(forest[i][j], maxH)
				maxH = max(maxH, forest[i][j])
				i, j = incInner(i, j)
			}
			i, j = incOuter(i, j)
		}
	}
	dist := func(a, b int) int {
		if a > b {
			return a - b
		}
		return b - a
	}
	_ = `
     ____             _
    | __ ) _ __ _   _| |__
    |  _ \| '__| | | | '_ \
    | |_) | |  | |_| | | | |
    |____/|_|   \__,_|_| |_|

    `
	traverse := func(i0, j0 int, inc incFunc) int {
		i, j := i0, j0
		tree := forest[i][j]
		i, j = inc(i, j)
		for ; i > 0 && i < n-1 && j > 0 && j < m-1 && forest[i][j] < tree; i, j = inc(i, j) {
		}
		//        dir1, dir2 := inc(0,0)
		//        fmt.Println(i0, j0, "get->",i, j, "dir", dir1, dir2, "ans", max(abs(i0-i), abs(j0-j))) + 1
		ans := max(dist(i0, i), dist(j0, j))
		return ans

	}

	lookup(0, 0, func(i, j int) (int, int) { return i, j + 1 }, func(i, j int) (int, int) { return i + 1, 0 })
	//	lookup(0, m-1, func(i, j int) (int, int) { return i, j - 1 }, func(i, j int) (int, int) { return i + 1, m - 1 })
	//	lookup(0, 0, func(i, j int) (int, int) { return i + 1, j }, func(i, j int) (int, int) { return 0, j + 1 })
	//	lookup(n-1, 0, func(i, j int) (int, int) { return i - 1, j }, func(i, j int) (int, int) { return n - 1, j + 1 })
	fmt.Println(forest)

	//	var overall int = n*m
	var maxView int
	for i := 1; i < n-1; i++ {
		for j := 1; j < m-1; j++ {
			curView := mul(
				traverse(i, j, func(i, j int) (int, int) { return i, j + 1 }),
				traverse(i, j, func(i, j int) (int, int) { return i, j - 1 }),
				traverse(i, j, func(i, j int) (int, int) { return i + 1, j }),
				traverse(i, j, func(i, j int) (int, int) { return i - 1, j }),
			)
			maxView = max(maxView, curView)
			fmt.Println(i, j, curView)
		}
	}
	fmt.Println(maxView)

}
