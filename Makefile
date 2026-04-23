# Makefile for Parallel 2D Heat Diffusion Solver
# Supports both Windows (with MSVC/MinGW) and Unix-like systems

# Compiler settings
CXX := g++
CXXFLAGS := -std=c++11 -O3 -Wall -Wextra -fopenmp
LDFLAGS := -fopenmp

# For MSVC on Windows, uncomment these:
# CXX := cl
# CXXFLAGS := /std:c++11 /O2 /W4 /openmp
# LDFLAGS := /openmp

# Directories
SRC_DIR := src
INCLUDE_DIR := include
BUILD_DIR := build
BIN_DIR := $(BUILD_DIR)/bin
OBJ_DIR := $(BUILD_DIR)/obj
OUTPUT_DIR := output
DATA_DIR := data

# Source files
SOURCES := $(SRC_DIR)/main.cpp $(SRC_DIR)/heat_solver.cpp
OBJECTS := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SOURCES))
TARGET := $(BIN_DIR)/heat_solver

# Default target
all: directories $(TARGET)

# Create necessary directories
directories:
	@mkdir -p $(BIN_DIR)
	@mkdir -p $(OBJ_DIR)
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(DATA_DIR)

# Build executable
$(TARGET): $(OBJECTS)
	@echo "Linking $@..."
	$(CXX) $(OBJECTS) -o $@ $(LDFLAGS)
	@echo "Build complete: $@"

# Compile object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "Compiling $<..."
	$(CXX) $(CXXFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@echo "Clean complete"

# Clean everything including output
clean-all: clean
	@echo "Cleaning output files..."
	@rm -rf $(OUTPUT_DIR)/*.txt
	@rm -rf $(OUTPUT_DIR)/*.png
	@echo "Full clean complete"

# Run serial version (small grid)
run-serial: all
	$(TARGET) 256 256 100

# Run parallel version (medium grid)
run-parallel: all
	$(TARGET) 256 256 100 --parallel

# Run parallel with specific thread count
run-parallel-threads: all
	$(TARGET) 512 512 100 --parallel --threads 4

# Run small test
test-small: all
	$(TARGET) 64 64 50

# Run medium test
test-medium: all
	$(TARGET) 256 256 100

# Run large test
test-large: all
	$(TARGET) 512 512 200 --parallel

# Run all tests
test-all: test-small test-medium test-large

# Visualize results
plot: all
	python3 scripts/plot_results.py output/final_grid.txt output/

# Performance analysis (grid scaling)
analyze-grid: all
	python3 scripts/analyze_performance.py $(TARGET) grid

# Performance analysis (thread scaling)
analyze-threads: all
	python3 scripts/analyze_performance.py $(TARGET) threads

# Full performance analysis
analyze-all: all
	python3 scripts/analyze_performance.py $(TARGET) both

# Help target
help:
	@echo "Makefile targets:"
	@echo "  all                 - Build the project (default)"
	@echo "  clean               - Remove build artifacts"
	@echo "  clean-all           - Remove build artifacts and output files"
	@echo ""
	@echo "  run-serial          - Run serial version (256x256, 100 timesteps)"
	@echo "  run-parallel        - Run parallel version (256x256, 100 timesteps)"
	@echo "  run-parallel-threads- Run parallel with 4 threads (512x512, 100 timesteps)"
	@echo ""
	@echo "  test-small          - Quick test (64x64, 50 timesteps)"
	@echo "  test-medium         - Medium test (256x256, 100 timesteps)"
	@echo "  test-large          - Large test (512x512, 200 timesteps, parallel)"
	@echo "  test-all            - Run all tests"
	@echo ""
	@echo "  plot                - Visualize results"
	@echo "  analyze-grid        - Grid size scaling analysis"
	@echo "  analyze-threads     - Thread count scaling analysis"
	@echo "  analyze-all         - Complete performance analysis"
	@echo ""
	@echo "  help                - Show this help message"

.PHONY: all directories clean clean-all run-serial run-parallel run-parallel-threads \
        test-small test-medium test-large test-all plot analyze-grid analyze-threads \
        analyze-all help
