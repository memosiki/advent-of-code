def main():
    tree = list(map(int, input().split()))
    # value of nodes
    value = [0] * len(tree)

    def DFS(node: int) -> int:
        offset = 2
        children_count = tree[node]
        metadata_count = tree[node + 1]
        children = []
        for child in range(children_count):
            children.append(node + offset)
            offset += DFS(node + offset)
        nonlocal value
        if children:
            for metadata_pos in range(node + offset, node + offset + metadata_count):
                child_idx = tree[metadata_pos] - 1
                if 0 <= child_idx < len(children):
                    value[node] += value[children[child_idx]]
        else:
            value[node] = sum(tree[node + offset : node + offset + metadata_count])
        return offset + metadata_count

    DFS(0)
    print(value[0])


if __name__ == "__main__":
    main()
