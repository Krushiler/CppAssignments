CC = g++
CFLAGS = -std=c++11 -Wall
SOURCES = main.cpp

ifeq ($(OS),Windows_NT)
	TARGET := main.exe
	RM := del
else
	TARGET := main
	RM := rm
endif

all: main.o lib.o
	$(CC) $(CFLAGS) -o $(TARGET) main.o lib.o

main.o: main.cpp
	$(CC) -c main.cpp

lib.o: lib.h lib.cpp
	$(CC) -c lib.cpp

clean:
	$(RM) $(TARGET) *.o