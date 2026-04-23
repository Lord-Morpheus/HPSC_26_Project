# Quick Start Guide

## Building the Project (Quick)

### Using Make (Recommended)

```powershell
# From the project root directory
make
```

The executable will be at `build/bin/heat_solver.exe` (on Windows) or `build/bin/heat_solver` (on Unix).

### Viewing all available targets

```powershell
make help
```

## Running Basic Tests

### Test 1: Small Grid - Serial
```powershell
make test-small
```

### Test 2: Medium Grid - Parallel
```powershell
make test-medium
```

### Test 3: Large Grid - Parallel
```powershell
make test-large
```

### Run all tests
```powershell
make test-all
```

Or run manually:
```powershell
./build/bin/heat_solver 64 64 100
./build/bin/heat_solver 256 256 200 --parallel
./build/bin/heat_solver 512 512 100 --parallel --threads 4
```

## Visualization

### Plot the results
```powershell
make plot
```

Or manually:
```powershell
python scripts/plot_results.py output/final_grid.txt output/
```

This will create:
- `output/heatmap.png` - Temperature distribution
- `output/cross_section.png` - Temperature profiles

## Performance Analysis

### Grid scaling (different grid sizes)
```powershell
make analyze-grid
```

### Thread scaling (different thread counts)
```powershell
make analyze-threads
```

### Complete analysis (both grid and threads)
```powershell
make analyze-all
```

## Project Structure

```
hpsc/
├── src/
│   ├── main.cpp              # Program entry point
│   ├── heat_solver.cpp       # Core solver implementation
│   └── solver.cpp            # (For custom experiments)
├── include/
│   └── heat_solver.h         # Class definition
├── scripts/
│   ├── plot_results.py       # Visualization
│   └── analyze_performance.py # Benchmarking
├── build/                    # Build output
├── output/                   # Results and plots
├── Makefile                  # Build configuration
└── README.md                 # Full documentation
```

## Key Parameters

To modify simulation parameters, edit `src/heat_solver.cpp`:

```cpp
double alpha = 0.25;  // Thermal diffusivity - controls heat spread rate
double dt = 0.001;    // Time step - smaller = more stable
double dx = 1.0;      // Grid spacing in x
double dy = 1.0;      // Grid spacing in y
```

**Stability condition** (must satisfy):
$$\frac{\alpha \Delta t}{\Delta x^2} < 0.25$$

## Typical Grid Sizes to Try

| Grid Size | Serial Time | Best For |
|-----------|------------|----------|
| 64×64 | ~10-50 ms | Quick tests |
| 128×128 | ~50-200 ms | Baseline comparison |
| 256×256 | ~200-800 ms | Performance analysis |
| 512×512 | ~1-5 sec | Scaling studies |

## Expected Speedups

With OpenMP parallelization on a quad-core system:
- 2 threads: ~1.8-1.9x speedup
- 4 threads: ~3.5-3.8x speedup

On larger grids (512×512+), you'll see better parallel efficiency.

## Troubleshooting

**Problem**: Make not found
- **Solution**: Install GNU Make (usually included in build-essential packages)

**Problem**: OpenMP not available
- **Solution**: Use a compiler that supports OpenMP (GCC, Clang with `-fopenmp`, or MSVC with `/openmp`)

**Problem**: Python scripts fail
- **Solution**: Install matplotlib: `pip install matplotlib numpy`

**Problem**: Slow performance
- **Solution**: 
  1. Rebuild with optimizations: `make clean && make`
  2. Use larger grid sizes (512×512 or more)
  3. Reduce timesteps for quick tests
  4. Check that compilation used -O3 optimization flags

## Next Steps

1. Build the project: `make`
2. Run a test: `make test-medium` or `./build/bin/heat_solver 256 256 100 --parallel`
3. Visualize results: `make plot`
4. Run performance analysis: `make analyze-all`

Happy computing!
