from .text_processing import prefix_func

# symbol outside of search text alphabet
DELIMITER = "#"


def KnuthMorrisPrattSearch(pattern: str, text: str) -> int:
    """
    Returns index of leftmost occurrence of pattern in text
    """
    pattern_prefix = prefix_func(pattern + DELIMITER)
    pattern_len = len(pattern)

    # length of previously found prefix
    previous_pfunc = 0
    for i in range(len(text)):
        if text[i] == pattern[previous_pfunc]:
            previous_pfunc += 1
            if previous_pfunc == pattern_len:
                # pattern found
                return i - pattern_len + 1
        else:
            # recalc prefix function
            while previous_pfunc > 0 and text[i] != pattern[previous_pfunc]:
                previous_pfunc = pattern_prefix[previous_pfunc]
            if text[i] == pattern[previous_pfunc]:
                previous_pfunc += 1
    return -1
