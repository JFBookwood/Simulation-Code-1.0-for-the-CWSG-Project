import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

G = 6.67430e-11
dark_matter_factor = 10

def read_csv(file_path, is_dark_matter=False):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    positions = df[['x', 'y', 'z']].values.astype(np.float64)
    masses = np.ones(len(positions), dtype=np.float64)
    velocities = np.zeros_like(positions)
    
    if is_dark_matter:
        masses *= dark_matter_factor
    
    return masses, positions, velocities

def compute_forces_in_blocks(masses, positions, block_size=500):
    n = len(masses)
    forces = np.zeros_like(positions)

    print(f"Total number of particles: {n}")
    
    for i in range(0, n, block_size):
        print(f"Processing block {i // block_size + 1}/{(n // block_size) + 1}")
        for j in range(i, n, block_size):
            block_forces = np.zeros((min(block_size, n - i), 3))
            for k in range(i, min(i + block_size, n)):
                for l in range(j, min(j + block_size, n)):
                    if k != l:
                        r = positions[l] - positions[k]
                        dist = np.linalg.norm(r)
                        if dist > 0:
                            force = G * masses[k] * masses[l] / dist**2 * r / dist
                            block_forces[k - i] += force
            forces[i:min(i + block_size, n)] += block_forces
    
    return forces

def update_positions(masses, positions, velocities, dt):
    forces = compute_forces_in_blocks(masses, positions)
    velocities += forces / masses[:, np.newaxis] * dt
    positions += velocities * dt
    return positions, velocities

def simulate(matter_file_path, dark_matter_file_path, dt=1e-3, num_steps=10):
    print("Starting simulation...")
    matter_masses, matter_positions, matter_velocities = read_csv(matter_file_path)
    dark_matter_masses, dark_matter_positions, dark_matter_velocities = read_csv(dark_matter_file_path, is_dark_matter=True)

    print(f"Reading data from: {matter_file_path}")
    print(f"Reading data from: {dark_matter_file_path}")

    print("Combining matter and dark matter data...")
    masses = np.concatenate([matter_masses, dark_matter_masses])
    positions = np.concatenate([matter_positions, dark_matter_positions])
    velocities = np.concatenate([matter_velocities, dark_matter_velocities])

    print("Running simulation...")
    for step in range(num_steps):
        print(f"Simulation step {step + 1}/{num_steps}")
        positions, velocities = update_positions(masses, positions, velocities, dt)

    print("Simulation complete. Saving results...")

    result_df = pd.DataFrame(positions, columns=['x', 'y', 'z'])
    result_df['vx'] = velocities[:, 0]
    result_df['vy'] = velocities[:, 1]
    result_df['vz'] = velocities[:, 2]
    result_df.to_csv('simulation_results.csv', index=False)

    plt.figure(figsize=(8, 8))
    plt.scatter(positions[:, 0], positions[:, 1], c='blue', s=1)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Partikelpositionen nach Simulation')
    plt.show()

if __name__ == "__main__":
    matter_file_path = r'/path/to/your/matter_particles.csv'
    dark_matter_file_path = r'/path/to/your/dark_matter_particles.csv'
    simulate(matter_file_path, dark_matter_file_path)

print("Done...")
