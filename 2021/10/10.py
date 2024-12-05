import sys


LHS = {"(", "[", "{", "<"}
RHS = {")", "]", "}", ">"}
mapping = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
syntax_error_scoring_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
autocomplete_scoring_table = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

if __name__ == "__main__":
    syntax_error_score = 0
    autocomplete_scores = []
    for line in sys.stdin:
        text = line.strip()
        stack = []
        for char in text:
            # print(char, "#", *stack)
            if char in LHS:
                stack.append(char)
            elif char in RHS:
                opening = mapping[stack.pop()]
                if char != opening:
                    # print(text, f"Expected {opening} but found {char}")
                    syntax_error_score += syntax_error_scoring_table[char]
                    break
        else:
            # print(text, "Incomplete")
            score = 0
            for char in reversed(stack):
                score *= 5
                score += autocomplete_scoring_table[char]
            autocomplete_scores.append(score)
    autocomplete_score = sorted(autocomplete_scores)[len(autocomplete_scores) // 2]
    print("Syntax Error Score", syntax_error_score)
    print("Autocomplete Score", autocomplete_score)
