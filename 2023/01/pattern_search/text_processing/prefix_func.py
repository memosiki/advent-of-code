def prefix_func(line: str) -> list[int]:
    n = len(line)
    p = [0] * n

    for i in range(1, n):
        # i       -- last char index on suffix side
        # p[i]-1  -- last char index on prefix side

        if line[i] == line[p[i - 1]]:
            # p[i] <= p[i-1] + 1 is guaranteed with prefix function
            p[i] = p[i - 1] + 1
        else:
            # considering prefix-suffix of smaller length k.
            # k is a measurement of length therefore line[k] is the char following the current suffix with length k
            k = p[i - 1]
            while k > 0 and line[k] != line[i]:
                k = p[k - 1]
            if k > 0:
                # such a suffix found
                p[i] = k + 1
            elif line[i] == line[0]:
                # trivial suffix length of 1
                p[i] = 1
            else:
                p[i] = 0
    return p
