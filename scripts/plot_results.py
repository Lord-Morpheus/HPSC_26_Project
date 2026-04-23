#!/usr/bin/env python3
"""
Visualization script for 2D Heat Diffusion Solver results.
Reads grid data from output files and creates heatmaps.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize
import sys
import os

def read_grid_file(filename):
    """
    Read grid data from a text file.
    
    File format:
    nx ny
    T[0,0] T[0,1] ... T[0,ny-1]
    T[1,0] T[1,1] ... T[1,ny-1]
    ...
    T[nx-1,0] T[nx-1,1] ... T[nx-1,ny-1]
    """
    try:
        with open(filename, 'r') as f:
            # Read dimensions
            dimensions = f.readline().strip().split()
            nx, ny = int(dimensions[0]), int(dimensions[1])
            
            # Read grid data
            grid = []
            for i in range(nx):
                row = list(map(float, f.readline().strip().split()))
                grid.append(row)
            
            return np.array(grid), (nx, ny)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

def plot_heatmap(grid, title="Heat Distribution", filename=None):
    """
    Create and display/save a heatmap of the grid.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    im = ax.imshow(grid.T, origin='lower', cmap='hot', aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, label='Temperature')
    
    # Labels and title
    ax.set_xlabel('X (grid points)')
    ax.set_ylabel('Y (grid points)')
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Add grid
    ax.grid(False)
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Figure saved to {filename}")
    else:
        plt.show()
    
    plt.close()

def plot_cross_section(grid, title="Temperature Cross-Section", filename=None):
    """
    Plot temperature profile along a cross-section through the center.
    """
    nx, ny = grid.shape
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Horizontal cross-section at center
    center_x = nx // 2
    axes[0].plot(grid[center_x, :], 'b-', linewidth=2)
    axes[0].set_xlabel('Y (grid points)')
    axes[0].set_ylabel('Temperature')
    axes[0].set_title(f'Horizontal Profile (X={center_x})')
    axes[0].grid(True, alpha=0.3)
    
    # Vertical cross-section at center
    center_y = ny // 2
    axes[1].plot(grid[:, center_y], 'r-', linewidth=2)
    axes[1].set_xlabel('X (grid points)')
    axes[1].set_ylabel('Temperature')
    axes[1].set_title(f'Vertical Profile (Y={center_y})')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Figure saved to {filename}")
    else:
        plt.show()
    
    plt.close()

def print_grid_statistics(grid):
    """
    Print statistics about the grid.
    """
    print("\n" + "="*60)
    print("GRID STATISTICS")
    print("="*60)
    print(f"Grid dimensions: {grid.shape[0]} x {grid.shape[1]}")
    print(f"Minimum temperature: {np.min(grid):.4f}")
    print(f"Maximum temperature: {np.max(grid):.4f}")
    print(f"Mean temperature: {np.mean(grid):.4f}")
    print(f"Std deviation: {np.std(grid):.4f}")
    print("="*60 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_results.py <grid_file> [output_dir]")
        print("  grid_file: Path to the grid output file (e.g., output/final_grid.txt)")
        print("  output_dir: Directory to save plots (optional, default: output/)")
        sys.exit(1)
    
    grid_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read grid data
    print(f"Reading grid data from {grid_file}...")
    grid, dimensions = read_grid_file(grid_file)
    
    if grid is None:
        sys.exit(1)
    
    # Print statistics
    print_grid_statistics(grid)
    
    # Create visualizations
    print("Creating visualizations...")
    
    # Main heatmap
    heatmap_file = os.path.join(output_dir, "heatmap.png")
    plot_heatmap(grid, title="Final Temperature Distribution", filename=heatmap_file)
    
    # Cross-section profile
    profile_file = os.path.join(output_dir, "cross_section.png")
    plot_cross_section(grid, title="Temperature Cross-Section", filename=profile_file)
    
    print("\nVisualization complete!")

if __name__ == "__main__":
    main()
