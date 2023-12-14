# make file=19a.asm
.PHONY: all
src := $(basename $(file))

# https://stackoverflow.com/q/76190992


all:
	nasm -f elf64 -w-label-orphan $(src).asm -o $(src).o
	#ld -m elf_x86_64 -no-pie $(src).o -o $(src).out -lc
	gcc -no-pie	$(src).o -o $(src).out

clean:
	rm -f $(src).o $(src).out
