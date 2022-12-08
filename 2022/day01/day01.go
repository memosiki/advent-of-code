package main

import (
	"bufio"
	"fmt"
	"golang.org/x/exp/constraints"
	"os"
	"sort"
	"strconv"
)

func main() {
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var curCalories, maxCalories int
	var elfes []int
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			maxCalories = max(maxCalories, curCalories)
			elfes = append(elfes, curCalories)
			curCalories = 0
		} else {
			calories, _ := strconv.Atoi(line)
			curCalories += calories
		}
	}
	sort.Sort(sort.Reverse(sort.IntSlice(elfes)))
	fmt.Println(sum(elfes[:3]))
	fmt.Println(elfes[:3])

}

func max[T constraints.Ordered](a, b T) T {
	if a > b {
		return a
	}
	return b
}

func sum[T []G, G constraints.Ordered](container T) G {
	var rollingSum G
	for _, elem := range container {
		rollingSum += elem
	}
	return rollingSum
}
