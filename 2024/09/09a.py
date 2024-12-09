if __name__ == "__main__":
    text = input()
    disk = [int(x) for x in text]
    assert len(disk) % 2
    empty_space = sum(disk[1::2])

    total = len(disk) // 2
    hashsum = 0

    fileid_right = total
    fileid_left = 0
    pos = 0
    segment_empty = 0

    lhs = 0
    rhs = len(disk) - 1
    filepart = disk[-1]

    while fileid_left < fileid_right:
        while not segment_empty:
            # empty segment ended, filling the leftmost file
            for i in range(disk[lhs]):
                hashsum += fileid_left * pos
                pos += 1
            segment_empty = disk[lhs + 1]
            fileid_left += 1
            lhs += 2

        if fileid_left >= fileid_right:
            break

        # rightside segment ended, looking for new one
        while not filepart:
            filepart = disk[rhs - 2]
            fileid_right -= 1
            rhs -= 2

        hashsum += fileid_right * pos
        segment_empty -= 1
        filepart -= 1
        pos += 1

    # remainder of the free space on disk
    if fileid_left == fileid_right:
        for i in range(filepart):
            hashsum += fileid_left * pos
            pos += 1

    print("Hashsum", hashsum)
