#!/usr/bin/env python3
"""
Performance analysis script for 2D Heat Diffusion Solver.
Runs multiple simulations with different grid sizes and thread counts
to analyze speedup and scalability.
"""

import subprocess
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np

class PerformanceAnalyzer:
    def __init__(self, executable_path):
        self.executable = executable_path
        self.results = {
            'serial': [],
            'parallel': []
        }
        self.grid_sizes = []
    
    def run_simulation(self, nx, ny, timesteps, parallel=False, num_threads=None):
        """
        Run a single simulation and extract execution time.
        """
        cmd = [self.executable, str(nx), str(ny), str(timesteps)]
        
        if parallel:
            cmd.append("--parallel")
            if num_threads:
                cmd.extend(["--threads", str(num_threads)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Extract execution time from output
            match = re.search(r'Total Execution Time: ([\d.]+) ms', result.stdout)
            if match:
                exec_time = float(match.group(1))
                return exec_time
            else:
                print(f"Could not parse execution time from output:")
                print(result.stdout)
                return None
        except subprocess.TimeoutExpired:
            print(f"Simulation timed out for grid {nx}x{ny}")
            return None
        except Exception as e:
            print(f"Error running simulation: {e}")
            return None
    
    def analyze_grid_scaling(self, grid_configs, timesteps=100):
        """
        Analyze performance scaling with grid size.
        grid_configs: list of (nx, ny) tuples
        """
        print("\n" + "="*70)
        print("GRID SIZE SCALING ANALYSIS")
        print("="*70)
        print(f"{'Grid Size':<15} {'Serial (ms)':<15} {'Parallel (ms)':<15} {'Speedup':<10}")
        print("-"*70)
        
        serial_times = []
        parallel_times = []
        grid_labels = []
        
        for nx, ny in grid_configs:
            grid_size_str = f"{nx}x{ny}"
            grid_labels.append(grid_size_str)
            
            # Run serial version
            serial_time = self.run_simulation(nx, ny, timesteps, parallel=False)
            if serial_time is None:
                continue
            serial_times.append(serial_time)
            
            # Run parallel version
            parallel_time = self.run_simulation(nx, ny, timesteps, parallel=True, num_threads=None)
            if parallel_time is None:
                continue
            parallel_times.append(parallel_time)
            
            speedup = serial_time / parallel_time
            
            print(f"{grid_size_str:<15} {serial_time:<15.3f} {parallel_time:<15.3f} {speedup:<10.2f}x")
        
        self.grid_sizes = grid_labels
        self.results['serial'] = serial_times
        self.results['parallel'] = parallel_times
        
        return serial_times, parallel_times
    
    def analyze_thread_scaling(self, nx, ny, timesteps=100, max_threads=8):
        """
        Analyze performance scaling with number of threads.
        """
        print("\n" + "="*70)
        print(f"THREAD SCALING ANALYSIS (Grid Size: {nx}x{ny})")
        print("="*70)
        print(f"{'Threads':<10} {'Time (ms)':<15} {'Speedup vs 1':<15} {'Efficiency':<10}")
        print("-"*70)
        
        thread_times = []
        speedups = []
        efficiencies = []
        
        # Run serial version as baseline
        baseline = self.run_simulation(nx, ny, timesteps, parallel=False)
        if baseline is None:
            print("Failed to run baseline serial version")
            return
        
        for num_threads in range(1, max_threads + 1):
            parallel_time = self.run_simulation(nx, ny, timesteps, parallel=True, num_threads=num_threads)
            if parallel_time is None:
                continue
            
            thread_times.append(parallel_time)
            speedup = baseline / parallel_time
            efficiency = speedup / num_threads * 100
            
            speedups.append(speedup)
            efficiencies.append(efficiency)
            
            print(f"{num_threads:<10} {parallel_time:<15.3f} {speedup:<15.2f}x {efficiency:<10.1f}%")
        
        return thread_times, speedups, efficiencies
    
    def plot_grid_scaling(self, filename="output/grid_scaling.png"):
        """
        Plot grid size scaling results.
        """
        if not self.results['serial'] or not self.grid_sizes:
            print("No data to plot")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        x_pos = np.arange(len(self.grid_sizes))
        width = 0.35
        
        # Execution time comparison
        axes[0].bar(x_pos - width/2, self.results['serial'], width, label='Serial', alpha=0.8)
        axes[0].bar(x_pos + width/2, self.results['parallel'], width, label='Parallel', alpha=0.8)
        axes[0].set_xlabel('Grid Size')
        axes[0].set_ylabel('Execution Time (ms)')
        axes[0].set_title('Execution Time vs Grid Size')
        axes[0].set_xticks(x_pos)
        axes[0].set_xticklabels(self.grid_sizes, rotation=45)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Speedup
        speedups = [s/p for s, p in zip(self.results['serial'], self.results['parallel'])]
        axes[1].plot(self.grid_sizes, speedups, 'o-', linewidth=2, markersize=8, label='Actual Speedup')
        axes[1].set_xlabel('Grid Size')
        axes[1].set_ylabel('Speedup')
        axes[1].set_title('Speedup vs Grid Size')
        axes[1].set_xticklabels(self.grid_sizes, rotation=45)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {filename}")
        plt.close()
    
    def plot_thread_scaling(self, thread_times, speedups, efficiencies, filename="output/thread_scaling.png"):
        """
        Plot thread scaling results.
        """
        fig, axes = plt.subplots(1, 3, figsize=(16, 4))
        
        num_threads = np.arange(1, len(thread_times) + 1)
        
        # Execution time
        axes[0].plot(num_threads, thread_times, 'o-', linewidth=2, markersize=8)
        axes[0].set_xlabel('Number of Threads')
        axes[0].set_ylabel('Execution Time (ms)')
        axes[0].set_title('Execution Time vs Number of Threads')
        axes[0].grid(True, alpha=0.3)
        
        # Speedup
        axes[1].plot(num_threads, speedups, 'o-', linewidth=2, markersize=8, label='Actual Speedup')
        axes[1].plot(num_threads, num_threads, '--', linewidth=2, label='Ideal (Linear)')
        axes[1].set_xlabel('Number of Threads')
        axes[1].set_ylabel('Speedup')
        axes[1].set_title('Speedup vs Number of Threads')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Efficiency
        axes[2].plot(num_threads, efficiencies, 'o-', linewidth=2, markersize=8)
        axes[2].axhline(y=100, color='r', linestyle='--', label='Perfect Efficiency (100%)')
        axes[2].set_xlabel('Number of Threads')
        axes[2].set_ylabel('Efficiency (%)')
        axes[2].set_title('Parallel Efficiency vs Number of Threads')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        axes[2].set_ylim([0, 150])
        
        plt.tight_layout()
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {filename}")
        plt.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_performance.py <executable_path> [analysis_type]")
        print("  analysis_type: 'grid' (default), 'threads', or 'both'")
        sys.exit(1)
    
    executable = sys.argv[1]
    analysis_type = sys.argv[2] if len(sys.argv) > 2 else 'both'
    
    if not os.path.exists(executable):
        print(f"Error: Executable '{executable}' not found")
        sys.exit(1)
    
    analyzer = PerformanceAnalyzer(executable)
    os.makedirs("output", exist_ok=True)
    
    if analysis_type in ['grid', 'both']:
        # Grid scaling analysis
        grid_configs = [
            (64, 64),
            (128, 128),
            (256, 256),
            (512, 512)
        ]
        analyzer.analyze_grid_scaling(grid_configs, timesteps=50)
        analyzer.plot_grid_scaling()
    
    if analysis_type in ['threads', 'both']:
        # Thread scaling analysis
        print("\n\nNote: Thread scaling analysis uses a fixed grid size of 512x512")
        thread_times, speedups, efficiencies = analyzer.analyze_thread_scaling(512, 512, timesteps=50, max_threads=8)
        if thread_times:
            analyzer.plot_thread_scaling(thread_times, speedups, efficiencies)

if __name__ == "__main__":
    main()
