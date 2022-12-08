package main

import (
	"bufio"
	"fmt"
	"gopkg.in/yaml.v2"
	"os"
	"strings"
)

type Node struct {
	Children map[string]*Node
	parent   *Node
	IsFolder bool
	Size     int
}

func (node *Node) String() string {
	aYAML, _ := yaml.Marshal(node)
	return string(aYAML)
}

func NewNode(isFolder bool, parent *Node) *Node {
	children := make(map[string]*Node)
	return &Node{IsFolder: isFolder, parent: parent, Children: children}
}

func DFS(node *Node) int {
	for _, child := range node.Children {
		node.Size += DFS(child)
	}
	return node.Size
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()
	var err error

	var (
		root     *Node = NewNode(true, nil)
		curDir   *Node
		nodeName string
		size     int
	)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		row := scanner.Text()
		line := func() *strings.Reader {
			return strings.NewReader(row)
		}

		_, err = fmt.Fscanf(line(), "$ cd /\n")
		if err == nil {
			curDir = root
			continue
		}
		_, err = fmt.Fscanf(line(), "$ cd ..\n")
		if err == nil {
			curDir = curDir.parent
			continue
		}
		_, err = fmt.Fscanf(line(), "$ cd %s\n", &nodeName)
		if err == nil {
			curDir = curDir.Children[nodeName]
			continue
		}
		_, err = fmt.Fscanf(line(), "$ ls\n")
		if err == nil {
			continue
		}
		_, err = fmt.Fscanf(line(), "dir %s\n", &nodeName)
		if err == nil {
			curDir.Children[nodeName] = NewNode(true, curDir)
			continue
		}
		_, err = fmt.Fscanf(line(), "%d %s\n", &size, &nodeName)
		if err == nil {
			curDir.Children[nodeName] = NewNode(false, curDir)
			curDir.Children[nodeName].Size = size
			continue
		}
		break
	}
	DFS(root)
	//	var dfsDir func(*Node)
	//	var smallDirs []*Node
	//	dfsDir = func(node *Node) {
	//		if node.IsFolder && node.Size <= 100_000 {
	//			smallDirs = append(smallDirs, node)
	//		}
	//		for _, child := range node.Children {
	//			dfsDir(child)
	//		}
	//	}
	//	dfsDir(root)
	//	var sumSmallDirs int
	//	for _, node := range smallDirs {
	//		sumSmallDirs += node.Size
	//	}
	//	fmt.Println(root)
	//	fmt.Println(sumSmallDirs)

	const (
		totalSpace    = 70_000_000
		requiredSpace = 30_000_000
	)

	var neededSpace = requiredSpace - totalSpace + root.Size
	var dfsDir func(*Node)
	var smallestDir *Node = root
	dfsDir = func(node *Node) {
		if node.IsFolder && node.Size > neededSpace && node.Size < smallestDir.Size {
			smallestDir = node
		}
		for _, child := range node.Children {
			dfsDir(child)
		}
	}
	dfsDir(root)
	fmt.Println(root)
	fmt.Println(smallestDir.Size)

}
