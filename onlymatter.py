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

print("Step 2: Initializing Voids and Superclusters data")

VOIDS = [
    {"name": "Boötes Void", "diameter": 250, "distance": 700, "coords": (14.83, 46.00)},
    {"name": "Eridanus Void", "diameter": 300, "distance": 1200, "coords": (4.50, -30.00)},
    {"name": "Canes Venatici Void", "diameter": 60, "distance": 200, "coords": (13.00, 45.00)},
    {"name": "Scorpius-Centaurus Void", "diameter": 900, "distance": 900, "coords": (16.00, -40.00)},
    {"name": "Aquarius Void", "diameter": 300, "distance": 1700, "coords": (22.00, -15.00)},
    {"name": "Sagittarius Void", "diameter": 500, "distance": 1600, "coords": (19.50, -25.00)},
    {"name": "Fornax Void", "diameter": 200, "distance": 1400, "coords": (3.00, -37.00)},
    {"name": "Pisces-Cetus Supercluster Complex", "diameter": 1300, "distance": 1000, "coords": (1.00, 0.00)},
]

SUPERCLUSTERS = [
    {"name": "Virgo Supercluster", "diameter": 33, "distance": 16.5, "coords": (12.00, 12.00)},
    {"name": "Perseus-Pisces Supercluster", "diameter": 180, "distance": 70, "coords": (2.00, 25.00)},
    {"name": "Laniakea Supercluster", "diameter": 160, "distance": 250, "coords": (6.00, -30.00)},
    {"name": "Shapley Supercluster", "diameter": 370, "distance": 650, "coords": (13.00, -30.00)},
    {"name": "Horologium-Reticulum Supercluster", "diameter": 250, "distance": 800, "coords": (3.00, -58.00)},
    {"name": "Leo Supercluster", "diameter": 100, "distance": 290, "coords": (10.00, 15.00)},
]

print("Step 3: Initializing matter density array")

matter_density = np.zeros((SIZE, SIZE, SIZE))

print("Step 4: Initializing vectors for gravity calculation")

VECTORS = [
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
    (1, 1, 1), (-1, 1, 1),
    (1, -1, 1), (1, 1, -1),
    (-1, -1, 1), (-1, 1, -1),
    (1, -1, -1), (-1, -1, -1)
]

print("Step 5: Generating random particles")

def generate_particles(num_particles):
    particles = []
    for _ in range(num_particles):
        x = random.randint(0, SIZE-1)
        y = random.randint(0, SIZE-1)
        z = random.randint(0, SIZE-1)
        particles.append((x, y, z))
    return particles

print("Step 6: Calculating gravitational force")

def calculate_gravity(m1, m2, r):
    if r == 0:
        return 0
    force = G * m1 * m2 / r**2
    return force

print("Step 7: Applying gravitational forces to matter density")

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

print("Step 8: Generating initial matter density")

particles = generate_particles(NUM_PARTICLES)

for x, y, z in particles:
    matter_density[x][y][z] += 1

print("Step 9: Simulation loop")

for t in range(TIME_STEPS):
    matter_density = apply_gravity(matter_density)

    print(f"Step 10.{t+1}: Calculating expansion rate for Voids")
    for void in VOIDS:
        expansion_rate = 1 + t * 0.01
        x, y = void["coords"]
        distance_from_milky_way = void["distance"] * expansion_rate
        void["expansion_rate"] = expansion_rate
        void["distance_from_milky_way"] = distance_from_milky_way

    print(f"Step 11.{t+1}: Calculating expansion rate for Superclusters")
    for supercluster in SUPERCLUSTERS:
        expansion_rate = 1 + t * 0.01
        x, y = supercluster["coords"]
        distance_from_milky_way = supercluster["distance"] * expansion_rate
        supercluster["expansion_rate"] = expansion_rate
        supercluster["distance_from_milky_way"] = distance_from_milky_way

print("Step 12: Converting data to DataFrames")

voids_df = pd.DataFrame(VOIDS)
superclusters_df = pd.DataFrame(SUPERCLUSTERS)

print("Step 13: Exporting data to CSV")

voids_df.to_csv('voids_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
superclusters_df.to_csv('superclusters_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

matter_particles = pd.DataFrame(particles, columns=["x", "y", "z"])

matter_particles.to_csv('matter_particles.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Step 14: Printing first 10 rows of Voids and Superclusters DataFrames")

print("Voids Data:")
print(voids_df.head(10))
print("\nSuperclusters Data:")
print(superclusters_df.head(10))

print("Step 15: Visualizing matter density distribution")

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
