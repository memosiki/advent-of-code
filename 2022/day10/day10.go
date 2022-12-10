package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const ScreenWidth = 40

func main() {
	file, _ := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var (
		register  = 1
		tickCur   = 1
		increment int
	)
	var tick = func() {
		// if shown
		if register-1 <= tickCur%ScreenWidth && tickCur%ScreenWidth <= register+1 {
			fmt.Print("#")
		} else {
			fmt.Print(".")
		}
		if tickCur%ScreenWidth == 0 {
			fmt.Println()
		}
		tickCur++
	}
	for scanner.Scan() {
		command := scanner.Text()
		if command == "noop" {
			tick()
		} else {
			_, _ = fmt.Fscan(strings.NewReader(command), &command, &increment)
			tick()
			register += increment
			tick()
		}
	}
}
