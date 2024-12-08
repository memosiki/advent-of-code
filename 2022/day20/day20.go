package main

import (
	"bufio"
	"fmt"
	"github.com/sbwhitecap/tqdm"
	"os"
	"strconv"
)

// Node of a doubly linked list
type Node struct {
	next, prev *Node
	val        int
}

func (node *Node) String() string {
	//return fmt.Sprintf("<%d (%d) %d>", node.prev.val, node.val, node.next.val)
	return strconv.Itoa(node.val)
}
func (node *Node) PrintN(n int) {
	fmt.Println()

	for i := 0; i < n; i++ {
		fmt.Print(node, " ")
		node = node.next
	}
	fmt.Println()
}

//// Get -- n is positive
//func (node *Node) Get(n int) int {
//	for i := 0; i < n; i++ {
//		node = node.next
//	}
//	return node.val
//}

// Move moves node n positions to the front
// n accepts only non-negative values
func (node *Node) Move(n int) {
	//fmt.Println("moving", node, n, "places")
	var prevNode, nextNode, cur *Node
	if n == 0 {
		return
	}

	cur = node
	for i := 0; i < n; i++ {
		cur = cur.next
	}

	// cut out the node
	prevNode, nextNode = node.prev, node.next
	prevNode.next, nextNode.prev = nextNode, prevNode
	//fmt.Println("linking", prevNode, nextNode)

	// splice back
	prevNode, nextNode = cur, cur.next
	prevNode.next, nextNode.prev = node, node
	node.prev, node.next = prevNode, nextNode
	//fmt.Println("inserting", prevNode, node, nextNode)
}

const (
	//DecryptionKey = 811589153
	DecryptionKey = 1
	//TimesMixed    = 2
	TimesMixed    = 1
)

func main() {
	file, _ := os.Open("input")
	defer file.Close()
	scanner := bufio.NewScanner(file)

	// handle root
	scanner.Scan()
	num, _ := strconv.Atoi(scanner.Text())
	var prev, node, root *Node
	root = &Node{val: num * DecryptionKey}
	var nodes = []*Node{root}

	prev = root
	for scanner.Scan() {
		num, _ = strconv.Atoi(scanner.Text())
		node = &Node{val: num * DecryptionKey, prev: prev}
		nodes = append(nodes, node)
		prev.next, prev = node, node
	}
	// make it circular
	root.prev, node.next = node, root

	// mix
	n := len(nodes)
	root.PrintN(n)

	tqdm.R(
		0, TimesMixed, func(v interface{}) (brk bool) {
			for _, node = range nodes {
				root.PrintN(n)
				node.Move(bruhMod(node.val, n))
			}
			return false
		},
	)
	//for i := 0; i < TimesMixed; i++ {
	//
	//}

	// materialize list
	//const RootVal = 0
	//for root.val != RootVal {
	//	root = root.next
	//}
	//fmt.Println("found root")
	nodes[0] = root
	nodes = nodes[:1]
	node = root.next
	for ; node != root; node = node.next {
		nodes = append(nodes, node)
	}
	fmt.Println(nodes)
	answer := nodes[1000%n].val + nodes[2000%n].val + nodes[3000%n].val
	fmt.Println("Answer", answer)

}

// bruhMod -- divmod with a quirk.
// Provides true modulus since Go's _%_ computes the "remainder" as opposed to the "modulus".
func bruhMod(a, b int) (mod int) {
	mod = a
	for mod >= b || -mod >= b {
		mod = (mod%b + b) % b
		// Add -1/+1 for each cycle around N. Idk, got this empirically. However, it is
		// guaranteed by the input that values > |2n| or equal to -n+2, -n+1, -n, -n-1,
		// -n-2, n+2, n+1, n, n-1, n-2 is not present, so this works somehow.
		if mod < 0 {
			mod -= -mod/b + 1
		} else if mod > 0 {
			mod += mod / b
		}
	}
	return
}
