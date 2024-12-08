def main():
    tree = list(map(int, input().split()))
    metadata_sum = 0

    def DFS(node: int) -> int:
        offset = 2
        children = tree[node]
        metadata = tree[node + 1]
        # print("Node at", node, "->", children, metadata)
        for child in range(children):
            offset += DFS(node + offset)

        nonlocal metadata_sum
        metadata_sum += sum(tree[node + offset : node + offset + metadata])
        return offset + metadata

    DFS(0)
    print(metadata_sum)


if __name__ == "__main__":
    main()
