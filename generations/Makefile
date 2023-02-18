CC = g++
CFLAGS = -std=c++11 -Wall
SOURCES = main.cpp

ifeq ($(OS),Windows_NT)
	ANGLES_GENERATOR_TARGET := angles_generator.exe
	ANGLES_READER_TARGET := angles_reader.exe
	RM := del
else
	ANGLES_GENERATOR_TARGET := angles_generator
	ANGLES_READER_TARGET := angles_reader
	RM := rm
endif

ANGLES_SETS_COUNT = 5
ANGLES_SETS_FILENAME = "angles.txt"

compileAndRun: all run


all: angles_generator.o angles_reader.o
	$(CC) $(CFLAGS) -o $(ANGLES_GENERATOR_TARGET) angles_generator.o
	$(CC) $(CFLAGS) -o $(ANGLES_READER_TARGET) angles_reader.o

angles_generator.o: angles_generator.cpp
	$(CC) -c angles_generator.cpp

angles_reader.o: angles_reader.cpp
	$(CC) -c angles_reader.cpp

run:
	./$(ANGLES_GENERATOR_TARGET) $(c) $(o)
	./$(ANGLES_READER_TARGET) $(o)


clean:
	$(RM) $(ANGLES_GENERATOR_TARGET) *.o
	$(RM) $(ANGLES_READER_TARGET) *.o