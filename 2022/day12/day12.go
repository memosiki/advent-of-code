package main

import (
	"bufio"
	"fmt"
	"github.com/emirpasic/gods/queues/arrayqueue"
	"golang.org/x/exp/constraints"
	"os"
)

type Node struct {
	i, j int
}

func main() {
	file, err := os.Open("input")
	defer file.Close()
	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(file)
	var terrain [][]byte
	var n int
	for scanner.Scan() {
		terrain = append(terrain, make([]byte, len(scanner.Bytes())))
		copy(terrain[n], scanner.Bytes())
		n++
	}
	m := len(terrain[0])
	terrain[0][0] = 'a'
	var exit, entrance Node
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			if terrain[i][j] == 'E' {
				terrain[i][j] = 'z'
				exit = Node{i, j}
			}
			if terrain[i][j] == 'S' {
				terrain[i][j] = 'z'
				entrance = Node{i, j}
			}
		}
	}
	fmt.Println(entrance, exit)

	var BFS = func(start Node) int {
		queue := arrayqueue.New()
		queue.Enqueue(start)
		dist := make([]int, n*m)
		from := make([]Node, n*m)
		visited := make([]bool, n*m)
		visited[0] = true
		for !queue.Empty() {
			qnode, _ := queue.Dequeue()
			node := qnode.(Node)
			i, j := node.i, node.j

			depth := dist[i*m+j]
			if node == exit {
				return depth
			}
			if idx := i*m + m + j; i+1 < n && terrain[i+1][j] <= terrain[i][j]+1 && !visited[idx] {
				visited[idx] = true
				from[idx] = node
				dist[idx] = depth + 1
				queue.Enqueue(Node{i + 1, j})
			}
			if idx := i*m + j + 1; j+1 < m && terrain[i][j+1] <= terrain[i][j]+1 && !visited[idx] {
				visited[idx] = true
				from[idx] = node
				dist[idx] = depth + 1
				queue.Enqueue(Node{i, j + 1})
			}
			if idx := i*m - m + j; i-1 >= 0 && terrain[i-1][j] <= terrain[i][j]+1 && !visited[idx] {
				visited[idx] = true
				from[idx] = node
				dist[idx] = depth + 1
				queue.Enqueue(Node{i - 1, j})
			}
			if idx := i*m + j - 1; j-1 >= 0 && terrain[i][j-1] <= terrain[i][j]+1 && !visited[idx] {
				visited[idx] = true
				from[idx] = node
				dist[idx] = depth + 1
				queue.Enqueue(Node{i, j - 1})
			}
		}
		return -1
	}
	totalPath := BFS(entrance)
	fmt.Println(totalPath)

	var bestPath = totalPath
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			if terrain[i][j] == 'a' {
				// TODO: dijkstra
				path := BFS(Node{i, j})
				if 0 < path {
					bestPath = Min(bestPath, path)
				}
			}
		}
	}
	fmt.Println("best", bestPath)
	// reverse
	//idx := exit.i*m + exit.j
	//for from[idx] != entrance {
	//	node := from[idx]
	//	fmt.Println(node)
	//	idx = node.i*m + node.j
	//}
}

func Max[T constraints.Ordered](a, b T) T {
	if a > b {
		return a
	}
	return b
}

func Min[T constraints.Ordered](a, b T) T {
	if a < b {
		return a
	}
	return b
}
