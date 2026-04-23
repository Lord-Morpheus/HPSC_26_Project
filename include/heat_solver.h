#ifndef HEAT_SOLVER_H
#define HEAT_SOLVER_H

#include <vector>
#include <chrono>
#include <string>

class HeatSolver {
public:
    HeatSolver(int nx, int ny, double alpha, double dt, double dx, double dy);
    ~HeatSolver();
    
    // Initialize the grid with boundary conditions
    void initializeGrid();
    
    // Perform one time step (serial version)
    void stepSerialVersion();
    
    // Perform one time step (parallel version with OpenMP)
    void stepParallelVersion();
    
    // Run simulation for num_steps timesteps
    void runSimulation(int num_steps, bool parallel = false);
    
    // Save current grid state to file
    void saveGridToFile(const std::string& filename) const;
    
    // Load grid state from file
    void loadGridFromFile(const std::string& filename);
    
    // Get execution time from last run
    double getExecutionTime() const { return execution_time_ms; }
    
    // Get grid dimensions
    int getNx() const { return nx; }
    int getNy() const { return ny; }
    
    // Get temperature at specific location
    double getTemperature(int i, int j) const;
    
    // Get entire grid
    const std::vector<std::vector<double>>& getGrid() const { return grid; }
    
private:
    int nx, ny;                              // Grid dimensions
    double alpha;                             // Thermal diffusivity
    double dt;                                // Time step
    double dx, dy;                            // Spatial steps
    std::vector<std::vector<double>> grid;    // Current temperature grid
    std::vector<std::vector<double>> grid_new; // Next temperature grid
    double execution_time_ms;                // Execution time in milliseconds
    
    // Compute the Laplacian term for interior points
    double computeLaplacian(int i, int j) const;
    
    // Swap grids after update
    void swapGrids();
};

#endif // HEAT_SOLVER_H
