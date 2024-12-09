from sortedcontainers import SortedList
from tqdm import tqdm

if __name__ == "__main__":
    text = input()
    disk = [int(x) for x in text]
    assert len(disk) % 2

    blocks = SortedList()  # empty memory blocks

    memorymap = []
    fileid = 1
    files = [((0, disk[0]), 0)]

    pos = disk[0]
    for i in range(1, len(disk), 2):
        if disk[i]:
            blocks.add((pos, pos + disk[i]))
        pos += disk[i]
        files.append(((pos, pos + disk[i + 1]), fileid))
        pos += disk[i + 1]
        fileid += 1

    for (filestart, fileend), fileid in tqdm(reversed(files)):
        filelen = fileend - filestart
        bisect = blocks.bisect_left((filestart, 0))
        for blockstart, blockend in blocks.islice(stop=bisect):
            blocklen = blockend - blockstart
            if filelen <= blocklen:
                blocks.remove((blockstart, blockend))
                memorymap.append(((blockstart, blockstart + filelen), fileid))
                if filelen < blocklen:
                    blocks.add((blockstart + filelen, blockend))
                break
        else:
            memorymap.append(((filestart, fileend), fileid))

    checksum = 0
    for (filestart, fileend), fileid in memorymap:
        for pos in range(filestart, fileend):
            checksum += fileid * pos
    print("Checksum", checksum)
