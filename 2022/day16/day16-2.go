package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/emirpasic/gods/queues/arrayqueue"
	"io"
	"log"
	"os"
	"sort"
	"strings"
	"sync"
)

const rootName = "AA"
const timeLeft = 30

type Valve struct {
	Name     string
	Rate     int
	children map[string]*Valve
	Pathlen  map[string]int
}

func (valve *Valve) String() string {
	return fmt.Sprintf("%s-%d", valve.Name, valve.Rate)
	//return valve.Name + strconv.Itoa(valve.Rate)
}

func main() {
	file, err := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var name, childPath string
	var rate int
	valves := make(map[string]*Valve)
	childrenNames := make(map[string][]string)
	// scan input
	for scanner.Scan() {
		row := bytes.NewReader(scanner.Bytes())
		_, err = fmt.Fscanf(row, "Valve %s has flow rate=%d; tunnels lead to valves ", &name, &rate)
		if err == nil {
			buf := new(strings.Builder)
			_, _ = io.Copy(buf, row)
			childrenNames[name] = strings.Split(buf.String(), ", ")
			valves[name] = &Valve{Name: name, Rate: rate}
		} else {
			_, err = fmt.Fscanf(
				bytes.NewReader(scanner.Bytes()), "Valve %s has flow rate=%d; tunnel leads to valve %s\n", &name, &rate,
				&childPath,
			)
			childrenNames[name] = []string{childPath}
			valves[name] = &Valve{Name: name, Rate: rate}
		}
	}

	// organize children links
	for _, valve := range valves {
		valve.Pathlen = make(map[string]int, len(valves))
		valve.children = make(map[string]*Valve, len(childrenNames[valve.Name]))

		for _, childName := range childrenNames[valve.Name] {
			valve.children[childName] = valves[childName]
		}
	}

	// separate out valves with positive rate
	positiveRate := make(map[string]*Valve)
	for name, valve := range valves {
		if valve.Rate > 0 {
			positiveRate[name] = valve
		}
	}

	// bfs for path from each positive rate valve to other positive rate valves
	root := valves[rootName]
	positiveRate[rootName] = root
	for _, startValve := range positiveRate {
		depths := make(map[string]int, len(positiveRate))
		visited := make(map[string]bool, len(positiveRate))
		queue := arrayqueue.New()
		queue.Enqueue(startValve)
		visited[startValve.Name] = true
		for !queue.Empty() {
			qnode, _ := queue.Dequeue()
			node := qnode.(*Valve)
			startValve.Pathlen[node.Name] = depths[node.Name]
			for _, child := range node.children {
				if !visited[child.Name] {
					visited[child.Name] = true
					queue.Enqueue(child)
					depths[child.Name] = depths[node.Name] + 1
				}
			}
		}
	}

	// enumerate valve names effectively mapping string names to consecutive ids
	nameToId := make(map[string]int, len(positiveRate))
	idToValve := make(map[int]*Valve, len(positiveRate))
	prGraph := make([][]int, len(positiveRate))
	rates := make([]int, len(positiveRate))

	for i := range prGraph {
		prGraph[i] = make([]int, len(positiveRate))
	}

	const rootId = 0
	idx := 0
	idToValve[rootId] = root
	delete(positiveRate, rootName)
	for _, valve := range positiveRate {
		idx++
		idToValve[idx] = valve
	}
	for id, valve := range idToValve {
		nameToId[valve.Name] = id
		rates[id] = valve.Rate
	}

	//nameToId[rootName], idToValve[rootId], nameToId[idToValve[rootId].Name], idToValve[nameToId[idToValve[rootId].Name]] = rootId, root, nameToId[idToValve[rootId].Name], idToValve[rootId]

	for id, valve := range idToValve {
		for child, pathlen := range valve.Pathlen {
			if _, ok := valves[child]; ok {
				prGraph[id][nameToId[child]] = pathlen
			}
		}
	}

	// prepare 4 different starting points for permutations
	valvesToPermute := len(prGraph) - 1
	ids := make([]int, valvesToPermute)
	for i := range ids {
		ids[i] = i + 1
	}

	start1 := make([]int, valvesToPermute)
	start2 := make([]int, valvesToPermute)
	start3 := make([]int, valvesToPermute)
	start4 := make([]int, valvesToPermute)
	copy(start1, ids)
	copy(start2, ids)
	copy(start3, ids)
	copy(start4, ids)

	// keep start1 as is, which is essentially also a random shuffle

	//// random shuffle
	//rand.Shuffle(
	//	valvesToPermute, func(i, j int) {
	//		start2[i], start2[j] = start2[j], start2[i]
	//	},
	//)

	// sort by rate
	sort.Slice(
		start3, func(i, j int) bool {
			return idToValve[start3[i]].Rate > idToValve[start3[i]].Rate
		},
	)

	//sort by distance from root
	sort.Slice(
		start4, func(i, j int) bool {
			iValve := idToValve[start4[i]]
			jValve := idToValve[start4[j]]
			return iValve.Pathlen[rootName] < jValve.Pathlen[rootName]
		},
	)

	var formatValveIdx = func(pos []int) string {
		valves := make([]*Valve, 0, len(pos)+1)
		valves = append(valves, root)
		for _, idx := range pos {
			valves = append(valves, idToValve[idx])
		}
		return fmt.Sprint(valves)
	}

	var wg sync.WaitGroup
	wg.Add(3)
	var prCount = len(positiveRate)
	var bruh = func(taskId int, valveIds []int) {
		var maxProfit int
		permutation := make(Permutation, len(valveIds))
		log.Println(taskId, "Starting permutation", valveIds)

		var iterations uint64
		for iterations = 0; permutation.Next(); iterations++ {
			permutation.Get(valveIds)
			profit := 0
			prevMe := rootId
			prevEl := rootId
			timeMe := timeLeft
			timeEl := timeLeft
			var curMe, curEl int
			for i := 0; i < prCount; i += 2 {
				curMe = valveIds[i]
				timeMe -= prGraph[prevMe][curMe] + 1
				if timeMe > 0 {
					profit += timeMe * rates[curMe]
					prevMe = curMe
				}
				curEl = valveIds[i]
				timeEl -= prGraph[prevEl][curEl] + 1
				if timeEl > 0 {
					profit += timeEl * rates[curEl]
					prevEl = curEl
				}
				if profit > maxProfit {
					go log.Println(taskId, "iteration", iterations, "profit", profit, formatValveIdx(valveIds))
					maxProfit = profit
				}
			}
		}
		wg.Done()
		log.Println(taskId, "Ready", maxProfit)
	}
	go bruh(1, start1)
	//go bruh(2, start2)
	go bruh(3, start3)
	go bruh(4, start4)
	wg.Wait()
}

// Permutation implementation of https://stackoverflow.com/a/30230552
type Permutation []int // slice holds intermediate state as offsets in a Fisher-Yates shuffle algorithm

func (diffs Permutation) Next() (exists bool) {
	for i := len(diffs) - 1; i >= 0; i-- {
		if i == 0 || diffs[i] < len(diffs)-i-1 {
			diffs[i]++
			break
		}
		diffs[i] = 0
	}
	if diffs[0] >= len(diffs) {
		return
	}
	return true
}
func (diffs Permutation) Get(container []int) {
	for i, v := range diffs {
		container[i], container[i+v] = container[i+v], container[i]
	}
}
