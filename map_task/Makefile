CC = g++
CFLAGS = -std=c++11 -Wall
SOURCES = map_test.cpp
PYTHON = py

ifeq ($(OS),Windows_NT)
	TARGET := map_test.exe
	RM := del
	BG := start /b
	
	mkdir = $(shell if not exist $(subst /,\,$(1)) mkdir $(subst /,\,$(1)))
	rmdir = $(shell if exist $(subst /,\,$(1)) rmdir /Q /S $(subst /,\,$(1)))
else
	TARGET := map_test
	RM := rm
	BG := nohup

	mkdir = mkdir -p $(1)
	rmdir = rmdir $(1) > /dev/null 2>&1 || true
endif

run: all
	./$(TARGET)
	$(PYTHON) map_test.py
	$(BG) $(PYTHON) plotter.py "data/mem_cpp.txt" "data/mem_py.txt" "Memory bytes"
	$(BG) $(PYTHON) plotter.py "data/time_cpp.txt" "data/time_py.txt" "Time ms"


data_folder:
	$(call mkdir,data)


all: map_test.o data_folder
	$(CC) $(CFLAGS) -o $(TARGET) map_test.o


map_test.o: map_test.cpp
	$(CC) -c map_test.cpp


clean:
	$(RM) $(TARGET) *.o
	$(call rmdir,data)