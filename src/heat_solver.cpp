#include "heat_solver.h"
#include <iostream>
#include <fstream>
#include <omp.h>
#include <cmath>
#include <iomanip>

HeatSolver::HeatSolver(int nx, int ny, double alpha, double dt, double dx, double dy)
    : nx(nx), ny(ny), alpha(alpha), dt(dt), dx(dx), dy(dy), execution_time_ms(0.0) {
    // Initialize grids with zeros
    grid.assign(nx, std::vector<double>(ny, 0.0));
    grid_new.assign(nx, std::vector<double>(ny, 0.0));
}

HeatSolver::~HeatSolver() {
    // Cleanup is automatic with std::vector
}

void HeatSolver::initializeGrid() {
    // Initialize with a heat source in the center
    int center_x = nx / 2;
    int center_y = ny / 2;
    int radius = std::min(nx, ny) / 8;
    
    // Create a circular heat source at the center
    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            double dx_dist = i - center_x;
            double dy_dist = j - center_y;
            double distance = std::sqrt(dx_dist * dx_dist + dy_dist * dy_dist);
            
            if (distance <= radius) {
                grid[i][j] = 100.0; // Hot region
            } else {
                grid[i][j] = 0.0;   // Cold region
            }
        }
    }
    
    // Copy to grid_new
    grid_new = grid;
}

double HeatSolver::computeLaplacian(int i, int j) const {
    double laplacian = (grid[i+1][j] - 2.0*grid[i][j] + grid[i-1][j]) / (dx * dx) +
                       (grid[i][j+1] - 2.0*grid[i][j] + grid[i][j-1]) / (dy * dy);
    return laplacian;
}

void HeatSolver::stepSerialVersion() {
    // Update interior points (serial)
    for (int i = 1; i < nx - 1; ++i) {
        for (int j = 1; j < ny - 1; ++j) {
            double laplacian = computeLaplacian(i, j);
            grid_new[i][j] = grid[i][j] + alpha * dt * laplacian;
        }
    }
    
    // Apply boundary conditions (Dirichlet: 0 at boundaries)
    for (int i = 0; i < nx; ++i) {
        grid_new[i][0] = 0.0;
        grid_new[i][ny-1] = 0.0;
    }
    for (int j = 0; j < ny; ++j) {
        grid_new[0][j] = 0.0;
        grid_new[nx-1][j] = 0.0;
    }
    
    swapGrids();
}

void HeatSolver::stepParallelVersion() {
    // Update interior points (parallel with OpenMP)
    #pragma omp parallel for collapse(2) default(none) shared(grid, grid_new)
    for (int i = 1; i < nx - 1; ++i) {
        for (int j = 1; j < ny - 1; ++j) {
            double laplacian = computeLaplacian(i, j);
            grid_new[i][j] = grid[i][j] + alpha * dt * laplacian;
        }
    }
    
    // Apply boundary conditions (Dirichlet: 0 at boundaries)
    #pragma omp parallel for default(none) shared(grid_new)
    for (int i = 0; i < nx; ++i) {
        grid_new[i][0] = 0.0;
        grid_new[i][ny-1] = 0.0;
    }
    
    #pragma omp parallel for default(none) shared(grid_new)
    for (int j = 0; j < ny; ++j) {
        grid_new[0][j] = 0.0;
        grid_new[nx-1][j] = 0.0;
    }
    
    swapGrids();
}

void HeatSolver::swapGrids() {
    std::swap(grid, grid_new);
}

void HeatSolver::runSimulation(int num_steps, bool parallel) {
    auto start_time = std::chrono::high_resolution_clock::now();
    
    for (int step = 0; step < num_steps; ++step) {
        if (parallel) {
            stepParallelVersion();
        } else {
            stepSerialVersion();
        }
        
        // Print progress every 100 steps
        if ((step + 1) % 100 == 0) {
            std::cout << "Completed timestep: " << (step + 1) << " / " << num_steps << std::endl;
        }
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    execution_time_ms = std::chrono::duration<double, std::milli>(end_time - start_time).count();
}

void HeatSolver::saveGridToFile(const std::string& filename) const {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << " for writing." << std::endl;
        return;
    }
    
    // Write grid dimensions
    file << nx << " " << ny << std::endl;
    
    // Write grid data
    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            file << grid[i][j];
            if (j < ny - 1) file << " ";
        }
        file << std::endl;
    }
    
    file.close();
    std::cout << "Grid saved to " << filename << std::endl;
}

void HeatSolver::loadGridFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << " for reading." << std::endl;
        return;
    }
    
    int read_nx, read_ny;
    file >> read_nx >> read_ny;
    
    if (read_nx != nx || read_ny != ny) {
        std::cerr << "Error: Grid dimensions mismatch." << std::endl;
        file.close();
        return;
    }
    
    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            file >> grid[i][j];
        }
    }
    
    grid_new = grid;
    file.close();
    std::cout << "Grid loaded from " << filename << std::endl;
}

double HeatSolver::getTemperature(int i, int j) const {
    if (i >= 0 && i < nx && j >= 0 && j < ny) {
        return grid[i][j];
    }
    return 0.0;
}
