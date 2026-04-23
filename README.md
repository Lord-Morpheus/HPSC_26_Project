# Parallel 2D Heat Diffusion Solver using OpenMP

A high-performance C++ implementation of a 2D heat diffusion equation solver with OpenMP parallelization and Python visualization tools.

## Project Overview

This project implements a numerical solver for the **2D heat diffusion equation** using the finite difference method:

$$\frac{\partial T}{\partial t} = \alpha \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} \right)$$

Where:
- **T(x,y,t)** is the temperature field
- **α** is the thermal diffusivity constant
- The discretized update equation uses finite differences for spatial derivatives

## Key Features

✅ **Serial and Parallel Implementations**
- Serial CPU implementation for baseline comparison
- Parallel implementation using OpenMP for multi-threaded execution

✅ **High Performance**
- Optimized C++11 code with compiler optimizations
- Efficient memory layout and cache usage
- Minimal synchronization overhead

✅ **Scalability Analysis**
- Performance benchmarking tools
- Grid size scaling analysis
- Thread count scaling analysis

✅ **Visualization**
- Python scripts for heatmap visualization
- Temperature profile cross-sections
- Performance comparison plots

## Project Structure

```
hpsc/
├── src/
│   ├── main.cpp                 # Main program entry point
│   ├── heat_solver.cpp          # Core solver implementation
│   └── solver.cpp               # (empty, for your reference)
├── include/
│   └── heat_solver.h            # Solver class definition
├── scripts/
│   ├── plot_results.py          # Visualization script
│   └── analyze_performance.py   # Performance analysis script
├── data/                        # Input data directory
├── output/                      # Output results directory
├── build/                       # Build output directory
├── Makefile                     # Build configuration
├── README.md                    # This file
└── .gitignore                  # Git ignore patterns
```

## Building the Project

### Prerequisites

- **C++11** compatible compiler (GCC, Clang, or MSVC)
- **OpenMP** support
- **GNU Make** (or compatible make tool)
- **Python** 3.6+ (for visualization scripts)

### Build Instructions

```bash
# Navigate to project directory
cd hpsc

# Build the project
make

# Executable will be in build/bin/heat_solver
```

**For Windows with MSVC**: Edit the Makefile and uncomment the MSVC compiler lines, then use `nmake` instead of `make`.

### Useful Make Targets

```bash
# Clean build artifacts
make clean

# Clean everything including outputs
make clean-all

# Show all available targets
make help
```

## Running Simulations

### Basic Usage

```bash
# Run serial version
./build/bin/heat_solver 256 256 100

# Run parallel version with default threads
./build/bin/heat_solver 256 256 100 --parallel

# Run with specific number of threads
./build/bin/heat_solver 256 256 100 --parallel --threads 4
```

Or use Makefile targets for convenience:

```bash
# Build and run serial version
make run-serial

# Build and run parallel version
make run-parallel

# Build and run with 4 threads
make run-parallel-threads

# Run all test simulations
make test-all
```

### Command Line Arguments

```
heat_solver <nx> <ny> <timesteps> [--parallel] [--threads N]

  nx:         Grid width in x-direction (e.g., 256)
  ny:         Grid height in y-direction (e.g., 256)
  timesteps:  Number of simulation timesteps (e.g., 100)
  --parallel: Enable OpenMP parallelization (optional)
  --threads N: Set number of OpenMP threads (optional)
```

### Example Runs

```bash
# Small grid, serial, baseline
./build/bin/heat_solver 64 64 50

# Medium grid, parallel
./build/bin/heat_solver 256 256 100 --parallel

# Large grid, parallel with 8 threads
./build/bin/heat_solver 512 512 200 --parallel --threads 8
```

## Visualization

### Plot Simulation Results

After running a simulation, visualize the results:

```bash
python scripts/plot_results.py output/final_grid.txt output/
```

This generates:
- **heatmap.png** - 2D temperature distribution heatmap
- **cross_section.png** - Temperature profiles along center lines

### Performance Analysis

Run comprehensive performance benchmarks:

```bash
# Grid scaling analysis (different grid sizes)
python scripts/analyze_performance.py ./build/bin/heat_solver grid

# Thread scaling analysis (different thread counts)
python scripts/analyze_performance.py ./build/bin/heat_solver threads

# Both analyses
python scripts/analyze_performance.py ./build/bin/heat_solver both
```

This generates performance plots showing:
- Execution time vs grid size
- Speedup vs grid size
- Execution time vs thread count
- Speedup vs thread count
- Parallel efficiency

## Algorithm Details

### Finite Difference Discretization

The 2D heat equation is discretized using central differences:

$$T_{i,j}^{n+1} = T_{i,j}^n + \alpha \Delta t \left( \frac{T_{i+1,j}^n - 2T_{i,j}^n + T_{i-1,j}^n}{\Delta x^2} + \frac{T_{i,j+1}^n - 2T_{i,j}^n + T_{i,j-1}^n}{\Delta y^2} \right)$$

### Parallelization Strategy

- **Outer loops** (x and y dimensions) are parallelized using `#pragma omp parallel for`
- **Loop collapse** directive combines nested loops for better work distribution
- **No race conditions** - each cell update depends only on previous timestep values
- **Minimal synchronization** - only at timestep boundaries

### Boundary Conditions

- **Dirichlet boundary conditions** - temperature at boundaries = 0
- Simple to implement and physically meaningful for diffusion problems

## Performance Characteristics

### Time Complexity
- **Serial**: O(N × M × T) where N×M is grid size, T is timesteps
- **Parallel**: O((N × M × T) / P) with P processors, assuming perfect load distribution

### Scalability
- **Strong scaling**: How speedup changes with thread count on fixed problem size
- **Weak scaling**: How performance scales when problem size increases proportionally with threads

### Expected Outcomes
- **Linear speedup** for moderate thread counts (2-8 threads)
- **Efficiency degradation** beyond 8-16 threads due to synchronization overhead
- **Consistent speedup** across different grid sizes

## Dependencies

### C++ Requirements
- Standard Library (C++11)
- OpenMP 2.0+

### Python Requirements
```bash
pip install numpy matplotlib
```

## Python Modules

### plot_results.py
- `read_grid_file()` - Read grid data from text format
- `plot_heatmap()` - Create and save heatmap visualization
- `plot_cross_section()` - Plot temperature profiles
- `print_grid_statistics()` - Print statistical information about grid

### analyze_performance.py
- `PerformanceAnalyzer` - Main analysis class
- `analyze_grid_scaling()` - Test different grid sizes
- `analyze_thread_scaling()` - Test different thread counts
- `plot_grid_scaling()` - Visualize grid scaling results
- `plot_thread_scaling()` - Visualize thread scaling results

## Output Formats

### Grid Data File (final_grid.txt)
```
256 256
T[0,0] T[0,1] ... T[0,255]
T[1,0] T[1,1] ... T[1,255]
...
T[255,0] T[255,1] ... T[255,255]
```

### Performance Report
The program outputs:
- Grid configuration
- Implementation type (serial/parallel)
- Number of threads
- Total execution time (ms)
- Grid update throughput (Million updates/sec)

## Configuration Parameters

In `src/heat_solver.cpp`, adjust these parameters:

```cpp
double alpha = 0.25;  // Thermal diffusivity
double dt = 0.001;    // Time step
double dx = 1.0;      // Spatial step in x
double dy = 1.0;      // Spatial step in y
```

**Note**: For numerical stability, ensure:
$$\frac{\alpha \Delta t}{\Delta x^2} < 0.25$$

## Tips for Best Performance

1. **Use the Makefile build**: Run `make` to build with optimization flags (-O3)
2. **Set appropriate thread count**: Match your system's core count
3. **Large grids**: Larger grids (512×512 or more) show better parallel efficiency
4. **Minimize file I/O**: Avoid frequent disk writes during simulation
5. **Compiler optimization**: The Makefile is configured with `-O3` by default

## Future Enhancements

- [ ] 3D heat diffusion solver
- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Advanced time integration schemes (RK4, implicit methods)
- [ ] Adaptive mesh refinement
- [ ] MPI support for distributed computing
- [ ] Real-time visualization
- [ ] Domain-specific boundary conditions

## References

- Heat Equation Theory: https://en.wikipedia.org/wiki/Heat_equation
- Finite Difference Methods: https://en.wikipedia.org/wiki/Finite_difference_method
- OpenMP Documentation: https://www.openmp.org/
- GNU Make Documentation: https://www.gnu.org/software/make/manual/

## License

This project is open source and available for educational purposes.

## Author

Tarun Srivastava

## Support

For issues, questions, or suggestions, please open an issue in the repository.
