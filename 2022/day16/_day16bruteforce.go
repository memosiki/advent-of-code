package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/emirpasic/gods/queues/arrayqueue"
	"io"
	"sort"
	"strconv"
	"strings"
	"sync"
)

const rootValveName = "AA"
const timeLeft = 30

type Valve struct {
	Name     string
	Rate     int
	children map[string]*Valve
	Pathlen  map[string]int
}

func (valve *Valve) String() string {
	//return fmt.Sprintf("%s %v\n", valve.Name, valve.Pathlen)
	return valve.Name + strconv.Itoa(valve.Rate)
}

const input = `Valve AW has flow rate=0; tunnels lead to valves DS, AA
Valve NT has flow rate=4; tunnels lead to valves AO, IT, AM, VZ
Valve FI has flow rate=0; tunnels lead to valves NK, RH
Valve NK has flow rate=13; tunnels lead to valves VZ, QE, FI
Valve ZB has flow rate=0; tunnels lead to valves IC, TX
Valve DS has flow rate=3; tunnels lead to valves ME, JY, OV, RA, AW
Valve JT has flow rate=0; tunnels lead to valves RA, OE
Valve OH has flow rate=0; tunnels lead to valves KT, AK
Valve OE has flow rate=9; tunnels lead to valves SH, MR, JT, QI
Valve CT has flow rate=0; tunnels lead to valves JH, NA
Valve CB has flow rate=0; tunnels lead to valves XC, JH
Valve EK has flow rate=0; tunnels lead to valves GB, ZZ
Valve NA has flow rate=0; tunnels lead to valves GL, CT
Valve JY has flow rate=0; tunnels lead to valves DS, IH
Valve RA has flow rate=0; tunnels lead to valves JT, DS
Valve QT has flow rate=0; tunnels lead to valves ZG, KM
Valve SM has flow rate=0; tunnels lead to valves AK, AM
Valve XC has flow rate=11; tunnel leads to valve CB
Valve BF has flow rate=10; tunnels lead to valves BU, MR
Valve OV has flow rate=0; tunnels lead to valves BV, DS
Valve GB has flow rate=25; tunnel leads to valve EK
Valve SD has flow rate=0; tunnels lead to valves JF, CN
Valve IH has flow rate=0; tunnels lead to valves JY, KM
Valve DF has flow rate=0; tunnels lead to valves ON, IC
Valve BV has flow rate=6; tunnels lead to valves OV, JN, ZG, UF
Valve PO has flow rate=0; tunnels lead to valves AK, QE
Valve JH has flow rate=12; tunnels lead to valves CB, MI, CT
Valve CN has flow rate=22; tunnel leads to valve SD
Valve JF has flow rate=0; tunnels lead to valves KM, SD
Valve QI has flow rate=0; tunnels lead to valves MI, OE
Valve JN has flow rate=0; tunnels lead to valves BV, BS
Valve TX has flow rate=0; tunnels lead to valves KM, ZB
Valve ME has flow rate=0; tunnels lead to valves VG, DS
Valve ON has flow rate=0; tunnels lead to valves DF, AA
Valve GL has flow rate=20; tunnel leads to valve NA
Valve AA has flow rate=0; tunnels lead to valves ON, UF, WR, ML, AW
Valve BS has flow rate=0; tunnels lead to valves JN, IC
Valve RH has flow rate=0; tunnels lead to valves FI, KT
Valve BU has flow rate=0; tunnels lead to valves BF, BG
Valve IT has flow rate=0; tunnels lead to valves NT, KT
Valve MR has flow rate=0; tunnels lead to valves OE, BF
Valve AO has flow rate=0; tunnels lead to valves ML, NT
Valve KM has flow rate=16; tunnels lead to valves WR, IH, QT, TX, JF
Valve ML has flow rate=0; tunnels lead to valves AO, AA
Valve VG has flow rate=0; tunnels lead to valves ME, IC
Valve MI has flow rate=0; tunnels lead to valves QI, JH
Valve AM has flow rate=0; tunnels lead to valves NT, SM
Valve KT has flow rate=23; tunnels lead to valves BG, OH, RH, SH, IT
Valve AK has flow rate=14; tunnels lead to valves SM, PO, OH
Valve BG has flow rate=0; tunnels lead to valves KT, BU
Valve QE has flow rate=0; tunnels lead to valves NK, PO
Valve IC has flow rate=17; tunnels lead to valves VG, ZZ, BS, ZB, DF
Valve UF has flow rate=0; tunnels lead to valves BV, AA
Valve SH has flow rate=0; tunnels lead to valves KT, OE
Valve WR has flow rate=0; tunnels lead to valves AA, KM
Valve ZZ has flow rate=0; tunnels lead to valves IC, EK
Valve ZG has flow rate=0; tunnels lead to valves BV, QT
Valve VZ has flow rate=0; tunnels lead to valves NK, NT
`

func main() {
	//file, err := os.Open("input")
	//defer file.Close()
	var err error
	scanner := bufio.NewScanner(strings.NewReader(input))
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
			_, err = fmt.Fscanf(bytes.NewReader(scanner.Bytes()), "Valve %s has flow rate=%d; tunnel leads to valve %s\n", &name, &rate, &childPath)
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
	positiveRateValves := make(map[string]*Valve)
	for name, valve := range valves {
		if valve.Rate > 0 {
			positiveRateValves[name] = valve
		}
	}

	root := valves[rootValveName]
	positiveRateValves[rootValveName] = root
	// bfs for path from each positive rate valve to other positive rate valves
	for _, startValve := range positiveRateValves {
		depths := make(map[string]int, len(positiveRateValves))
		visited := make(map[string]bool, len(positiveRateValves))
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
	delete(positiveRateValves, rootValveName)
	fmt.Println("READ", positiveRateValves)
	// bruteforce
	// 3hours
	// Answer: 1559 [NT KT KT AK CN BV DS KM OE IC BF NK GB JH XC]
	// starting pattern [NT KM NK GL BV JH OE DS XC AK BF CN KT IC GB]
	positiveRateValvesList := make([]*Valve, 0, len(positiveRateValves))
	positiveRateValvesList1 := make([]*Valve, len(positiveRateValves), len(positiveRateValves))
	positiveRateValvesList2 := make([]*Valve, len(positiveRateValves), len(positiveRateValves))
	positiveRateValvesList3 := make([]*Valve, len(positiveRateValves), len(positiveRateValves))
	for _, valve := range positiveRateValves {
		positiveRateValvesList = append(positiveRateValvesList, valve)
	}
	copy(positiveRateValvesList1, positiveRateValvesList)
	copy(positiveRateValvesList2, positiveRateValvesList)
	copy(positiveRateValvesList3, positiveRateValvesList)

	sort.Slice(positiveRateValvesList1, func(i, j int) bool {
		return positiveRateValvesList1[i].Rate > positiveRateValvesList1[j].Rate
	})
	sort.Slice(positiveRateValvesList2, func(i, j int) bool {
		return positiveRateValvesList2[i].Pathlen[positiveRateValvesList2[i].Name] < positiveRateValvesList2[j].Pathlen[positiveRateValvesList2[j].Name]
	})
	sort.Slice(positiveRateValvesList3, func(i, j int) bool {
		return positiveRateValvesList3[i].Rate/(positiveRateValvesList3[i].Pathlen[positiveRateValvesList3[i].Name]+1) > positiveRateValvesList1[j].Rate/(positiveRateValvesList3[j].Pathlen[positiveRateValvesList3[j].Name]+1)
	})

	var wg sync.WaitGroup
	wg.Add(4)
	var bruh = func(container []*Valve) {
		var maxProfit int
		fmt.Println("Start Pos", container)
		// bruteforce all valve opening sequences
		for _ = range permutations(container) {
			profit := 0
			prev := root
			time := timeLeft
			for _, valve := range container {
				time -= prev.Pathlen[valve.Name] + 1
				profit += time * valve.Rate
				prev = valve
				if profit > maxProfit {
					fmt.Println(profit, container)
					maxProfit = profit
				}
			}
		}
		wg.Done()
		fmt.Println("Max Profit", maxProfit)
	}
	go bruh(positiveRateValvesList)
	go bruh(positiveRateValvesList1)
	go bruh(positiveRateValvesList2)
	go bruh(positiveRateValvesList3)
	wg.Wait()
}

type Element = *Valve
type none = struct{}

func permutations(container []int) <-chan none {
	next := make(chan none)
	p := make([]int, len(container))
	go func() {
		defer close(next)
		for p[0] < len(p) {
			// get permutation
			for i, v := range p {
				container[i], container[i+v] = container[i+v], container[i]
			}
			next <- none{}
			// next permutation
			for i := len(p) - 1; i >= 0; i-- {
				if i == 0 || p[i] < len(p)-i-1 {
					p[i]++
					break
				}
				p[i] = 0
			}
		}
	}()
	return next
}

func Max2(a, b int) int {
	if a > b {
		return a
	}
	return b
}
