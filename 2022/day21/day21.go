package main

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os"
	"strings"
)

type Expr struct {
	dep1, op, dep2 string
}

// type int = int64
func do(a int, op string, b int) (ans int) {
	defer func() { fmt.Println("solved", ans) }()
	switch op {
	case "+":
		return a + b
	case "-":
		return a - b
	case "*":
		return a * b
	case "/":
		return a / b
	default:
		log.Panicln(a, op, b)
	}
	return 0
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var name, dep1, op, dep2 string
	var num int
	var err error
	var deps = make(map[string][]string)
	var monkeys = make(map[string]Expr)
	var ready = make(map[string]int)
	var try, resolve func(name string)
	// try resolving all deps of monkey
	resolve = func(name string) {
		//fmt.Println("resolving", name)
		for _, monkey := range deps[name] {
			try(monkey)
		}
	}
	// try solving for monkey
	try = func(name string) {
		expr, ok := monkeys[name]
		if !ok {
			return
		}
		dep1, ok1 := ready[expr.dep1]
		dep2, ok2 := ready[expr.dep2]
		if ok1 && ok2 {
			//fmt.Println("solving", name)
			ready[name] = do(dep1, expr.op, dep2)
			delete(monkeys, name)
			resolve(name)
		}
	}
	for scanner.Scan() {
		_, err = fmt.Fscanf(bytes.NewBuffer(scanner.Bytes()), "%s %s %s %s", &name, &dep1, &op, &dep2)
		if err == nil {
			name = strings.TrimSuffix(name, ":")
			monkeys[name] = Expr{dep1, op, dep2}
			deps[dep1] = append(deps[dep1], name)
			deps[dep2] = append(deps[dep2], name)
		} else {
			_, _ = fmt.Fscanf(bytes.NewBuffer(scanner.Bytes()), "%s %d", &name, &num)
			name = strings.TrimSuffix(name, ":")
			ready[name] = num
			resolve(name)
		}
	}
	for len(monkeys) != 0 {
		for name := range monkeys {
			try(name)
		}
	}
	const MainMonkeyName = "root"
	fmt.Println("Answer: ", ready[MainMonkeyName])
}
