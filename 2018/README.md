## Advent of code 2018

I've decided to revisit 2018 since it is regarded by many as the hardest year overall. For the language, I went with good old Python which is I believe the best for the rich selection of puzzles this challenge presents. Oh, and the fact that I'm well-versed in it.

### Notable days
#### Day 6
Puzzle asked for an algorithm which was essentially a Voronoi diagram in a bottle. 

#### Day 12, 18
Cycle detection. Simple as that. Not the hare and turtle kind of way but the whole system is iterative in these examples. Cycle detection appears a fair amount in Advent of Code and is a neat concept overall. I've enjoyed implementing those tasks but never failed to fail diving two numbers right in the final answer n-n. Good practice though.

#### Days 16, 19 and 21
All three were basically the same puzzle. Here's a set of peculiar machine instructions, go get a hang of what they are doing. At first, I wanted to actually transpile them to real ASM but ultimately it didn't help me much since the program they were representing would take an age of the universe to halt. 
It all came down to pinpointing which registers were holding what and what overall state would lead the program to halt. 
Yet I'm still really happy to get acquainted with NASM but the whole experience definitely was more on the _being miserable hacking on a black box_ side.

#### Day 22
All about Dijksta and traversing the graph of states. Honestly, this problem helped me get a hang of how states of things can be represented as a graph. I am never looking the same way on graph traversal now. 
Also, I gave numpy a fair try with these sorts of problems and it's incredibly good for 3d and more dimensional arrays. So now I wouldn't be shy to pull it up whenever a problem asks for such structures. 

#### Day 23
Insanely complex optimization problem that I've ultimately decided (after a reasonable amount of bashing my head against the wall) to feed into the actual scientific solver Z3. Compiling from source, interacting, and writing code for it was an experience of its own but in the end way too much reminiscent of the similar project I've worked with before -- sage.

#### Conclusion
Overall year felt a bit cumbersome. Plenty of challenges came down to _parse complex input and simulate the described system to the word_. Which can be a daunting task sometimes but it wasn't really the complexity I was looking for. 
Finishing the whole year was a fun undertaking nevertheless.
