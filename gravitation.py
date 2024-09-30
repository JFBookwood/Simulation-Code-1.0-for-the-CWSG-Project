import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

G = 6.67430e-11  # Gravitational constant
DARK_MATTER_FACTOR = 10  # Factor for dark matter mass increase

def read_csv(file_path, is_dark_matter=False):
    """Reads particle data from a CSV file and returns masses, positions, and velocities."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Strip whitespace from column names
        positions = df[['x', 'y', 'z']].values.astype(np.float64)
        masses = np.ones(len(positions), dtype=np.float64)

        if is_dark_matter:
            masses *= DARK_MATTER_FACTOR
        
        velocities = np.zeros_like(positions)  # Initialize velocities
        return masses, positions, velocities
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None

def compute_forces_in_blocks(masses, positions, block_size=500):
    """Calculates gravitational forces acting on particles in blocks to optimize performance."""
    n = len(masses)
    forces = np.zeros_like(positions)
    print(f"Total number of particles: {n}")

    # Iterate through blocks of particles
    for i in range(0, n, block_size):
        print(f"Processing block {i // block_size + 1}/{(n // block_size) + 1}")
        block_indices = np.arange(i, min(i + block_size, n))

        for j in range(i, n, block_size):
            # Calculate forces for current block against another block
            block_j_indices = np.arange(j, min(j + block_size, n))
            r_vectors = positions[block_j_indices][:, np.newaxis, :] - positions[block_indices]
            distances = np.linalg.norm(r_vectors, axis=-1)

            # Avoid self-interaction and apply force calculation
            valid_indices = distances > 0
            forces[block_indices] += (G * masses[block_indices][:, np.newaxis] * 
                                       masses[block_j_indices][valid_indices] / 
                                       distances[valid_indices]**2[:, np.newaxis] * 
                                       (r_vectors[valid_indices] / distances[valid_indices][:, np.newaxis]))

    return forces

def update_positions(masses, positions, velocities, dt):
    """Updates particle positions and velocities based on gravitational forces."""
    forces = compute_forces_in_blocks(masses, positions)
    velocities += forces / masses[:, np.newaxis] * dt
    positions += velocities * dt
    return positions, velocities

def simulate(matter_file_path, dark_matter_file_path, dt=1e-3, num_steps=10):
    """Runs the simulation of particle movement under gravitational forces."""
    print("Starting simulation...")
    matter_masses, matter_positions, matter_velocities = read_csv(matter_file_path)
    dark_matter_masses, dark_matter_positions, dark_matter_velocities = read_csv(dark_matter_file_path, is_dark_matter=True)

    if matter_positions is None or dark_matter_positions is None:
        return  # Exit if there's an error in reading data

    print(f"Combining matter and dark matter data...")
    masses = np.concatenate([matter_masses, dark_matter_masses])
    positions = np.concatenate([matter_positions, dark_matter_positions])
    velocities = np.concatenate([matter_velocities, dark_matter_velocities])

    print("Running simulation...")
    for step in range(num_steps):
        print(f"Simulation step {step + 1}/{num_steps}")
        positions, velocities = update_positions(masses, positions, velocities, dt)

    print("Simulation complete. Saving results...")
    result_df = pd.DataFrame(positions, columns=['x', 'y', 'z'])
    result_df[['vx', 'vy', 'vz']] = velocities  # Using DataFrame to handle velocity columns
    result_df.to_csv('simulation_results.csv', index=False)

    plt.figure(figsize=(8, 8))
    plt.scatter(positions[:, 0], positions[:, 1], c='blue', s=1)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Particle Positions After Simulation')
    plt.show()

if __name__ == "__main__":
    matter_file_path = r'/path/to/your/matter_particles.csv'
    dark_matter_file_path = r'/path/to/your/dark_matter_particles.csv'
    simulate(matter_file_path, dark_matter_file_path)

print("Done...")
