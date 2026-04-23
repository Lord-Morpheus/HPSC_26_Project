#include "heat_solver.h"
#include <iostream>
#include <iomanip>
#include <chrono>
#include <omp.h>

void printUsage(const char* program_name) {
    std::cout << "Usage: " << program_name << " <nx> <ny> <timesteps> [--parallel] [--threads N]" << std::endl;
    std::cout << "  nx:        Grid width in x-direction" << std::endl;
    std::cout << "  ny:        Grid height in y-direction" << std::endl;
    std::cout << "  timesteps: Number of simulation timesteps" << std::endl;
    std::cout << "  --parallel: Run parallel version (optional, default: serial)" << std::endl;
    std::cout << "  --threads N: Set number of OpenMP threads (optional)" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        printUsage(argv[0]);
        return 1;
    }
    
    // Parse command line arguments
    int nx = std::stoi(argv[1]);
    int ny = std::stoi(argv[2]);
    int timesteps = std::stoi(argv[3]);
    
    bool use_parallel = false;
    int num_threads = omp_get_max_threads();
    
    for (int i = 4; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--parallel") {
            use_parallel = true;
        } else if (arg == "--threads" && i + 1 < argc) {
            num_threads = std::stoi(argv[++i]);
        }
    }
    
    // Set number of threads
    omp_set_num_threads(num_threads);
    
    std::cout << "=" << std::string(60, '=') << std::endl;
    std::cout << "2D Heat Diffusion Solver" << std::endl;
    std::cout << "=" << std::string(60, '=') << std::endl;
    std::cout << "Grid Size (nx x ny): " << nx << " x " << ny << std::endl;
    std::cout << "Timesteps: " << timesteps << std::endl;
    std::cout << "Implementation: " << (use_parallel ? "PARALLEL (OpenMP)" : "SERIAL") << std::endl;
    std::cout << "Number of Threads: " << num_threads << std::endl;
    std::cout << "=" << std::string(60, '=') << std::endl;
    
    // Parameters for heat equation
    double alpha = 0.25;  // Thermal diffusivity
    double dt = 0.001;    // Time step
    double dx = 1.0;      // Spatial step in x
    double dy = 1.0;      // Spatial step in y
    
    // Create and initialize solver
    HeatSolver solver(nx, ny, alpha, dt, dx, dy);
    solver.initializeGrid();
    
    std::cout << "\nInitialization complete." << std::endl;
    std::cout << "Starting simulation..." << std::endl << std::endl;
    
    // Run simulation
    solver.runSimulation(timesteps, use_parallel);
    
    // Report results
    double exec_time = solver.getExecutionTime();
    double total_cells = static_cast<double>(nx) * ny;
    double total_updates = total_cells * timesteps;
    double throughput = total_updates / (exec_time / 1000.0) / 1e6;  // Million updates per second
    
    std::cout << "\n" << std::string(60, '=') << std::endl;
    std::cout << "SIMULATION RESULTS" << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    std::cout << "Total Execution Time: " << std::fixed << std::setprecision(3) 
              << exec_time << " ms" << std::endl;
    std::cout << "Total Grid Updates: " << static_cast<long long>(total_updates) << std::endl;
    std::cout << "Throughput: " << std::fixed << std::setprecision(2) 
              << throughput << " Million updates/sec" << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    
    // Save final grid state
    std::string output_file = "output/final_grid.txt";
    solver.saveGridToFile(output_file);
    
    return 0;
}
