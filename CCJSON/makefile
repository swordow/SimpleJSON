CC=g++
CFLAGS=
CCFLAGS=
LD_LIBRARY_PATH=./
libjson.a:ccjson.cc ccjson.h
	$(CC) -c $< -o $@

main.o:main.cc
	$(CC) -c $< -o $@

test:main.o
	$(CC) -v $< -L$(LD_LIBRARY_PATH) -ljson -o $@
