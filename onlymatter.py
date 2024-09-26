import numpy as np
import pandas as pd
import random
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("Step 1: Initializing constants")

SIZE = 100  # Size of the simulation cube in Mpc
NUM_PARTICLES = 100000  # Number of particles (representing matter density)
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
TIME_STEPS = 100  # Number of time steps for simulation

print("Step 2: Initializing matter density array")

matter_density = np.zeros((SIZE, SIZE, SIZE))

print("Step 3: Initializing vectors for gravity calculation")

VECTORS = [
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
    (1, 1, 1), (-1, 1, 1),
    (1, -1, 1), (1, 1, -1),
    (-1, -1, 1), (-1, 1, -1),
    (1, -1, -1), (-1, -1, -1)
]

print("Step 4: Generating random particles")

def generate_particles(num_particles):
    particles = []
    for _ in range(num_particles):
        x = random.randint(0, SIZE-1)
        y = random.randint(0, SIZE-1)
        z = random.randint(0, SIZE-1)
        particles.append((x, y, z))
    return particles

print("Step 5: Calculating gravitational force")

def calculate_gravity(m1, m2, r):
    if r == 0:
        return 0
    force = G * m1 * m2 / r**2
    return force

print("Step 6: Applying gravitational forces to matter density")

def apply_gravity(matter_density):
    new_density = np.zeros_like(matter_density)
    for x in range(SIZE):
        for y in range(SIZE):
            for z in range(SIZE):
                total_force = 0
                for vx, vy, vz in VECTORS:
                    nx, ny, nz = x + vx, y + vy, z + vz
                    if 0 <= nx < SIZE and 0 <= ny < SIZE and 0 <= nz < SIZE:
                        total_force += calculate_gravity(matter_density[x][y][z], matter_density[nx][ny][nz], 1)
                new_density[x][y][z] = total_force
    return new_density

print("Step 7: Generating initial matter density")

particles = generate_particles(NUM_PARTICLES)

for x, y, z in particles:
    matter_density[x][y][z] += 1

print("Step 8: Simulation loop")

for t in range(TIME_STEPS):
    matter_density = apply_gravity(matter_density)
    print(f"Step {t+1} of {TIME_STEPS}: Simulation progress...")

print("Step 9: Exporting data to CSV")

matter_particles = pd.DataFrame(particles, columns=["x", "y", "z"])
matter_particles.to_csv('simulation_only_matter.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Step 10: Printing first 10 rows of Matter Particles DataFrame")

print(matter_particles.head(10))

print("Step 11: Visualizing matter density distribution")

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

x, y, z = np.nonzero(matter_density)
ax.scatter(x, y, z, c=matter_density[x, y, z], cmap='viridis', marker='o', s=10)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.title('Matter Density Distribution')
plt.show()

print("Finish")
