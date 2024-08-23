```markdown
# Cosmological Simulation and Blender Visualization

This project involves running a cosmological simulation using SWIFT and visualizing the output in Blender. The simulation data includes properties like position, density, energy, and expansion of particles over time.

## Prerequisites

1. **SWIFT**: Ensure SWIFT cosmological simulation code is installed. You can get it from the official [SWIFT GitHub repository](https://github.com/SWIFTSIM/swiftsim).
2. **Blender**: Download and install Blender from [blender.org](https://www.blender.org/download/).
3. **Python**: Blender comes with its own Python installation.

## Running the SWIFT Simulation

### SWIFT Configuration

Ensure SWIFT is configured with the necessary options:
- Enable light cone output with `--enable-lightcone`.
- Include the HEALPix C library if making HEALPix maps.
- Use parallel HDF5 if running in MPI mode.

### SWIFT Parameter File

Create a parameter file for the simulation. Here is a simplified example:

```ini
[Cosmology]
Omega_b = 0.049
Omega_m = 0.315
Omega_L = 0.685
h = 0.673

[Simulation]
box_size = 100.0
num_particles = 1000000
end_time = 1.0
output_frequency = 10

[Lightcone0]
observer_position = 50.0, 50.0, 50.0
output_directory = ./lightcone_output/
```

### Running the Simulation

Execute the SWIFT simulation with the light cone flag:

```sh
swift --lightcone -p parameter_file.yml
```

The simulation will generate HDF5 files in the specified output directory. Each file contains particle data at different time steps.

## Preparing Data for Blender

### Converting HDF5 to CSV

Use a Python script to convert HDF5 files to CSV format. Here is a simple example:

```python
import h5py
import csv
import os

input_dir = "./lightcone_output/"
output_dir = "./csv_output/"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".hdf5"):
        with h5py.File(os.path.join(input_dir, filename), 'r') as hdf_file:
            particles = hdf['PartType1']
            output_file = os.path.join(output_dir, filename.replace(".hdf5", ".csv"))
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['x', 'y', 'z', 'density', 'energy'])
                for i in range(len(particles['Coordinates'])):
                    writer.writerow([particles['Coordinates'][i][0],
                                     particles['Coordinates'][i][1],
                                     particles['Coordinates'][i][2],
                                     particles['Density'][i],
                                     particles['InternalEnergy'][i]])
```

### Importing CSV into Blender

In Blender, you can use the following script to import the CSV data and create keyframes for animation:

```python
import bpy
import csv

input_dir = "./csv_output/"

def create_particles(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header
        for row in reader:
            x, y, z, density, energy = map(float, row)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=density*0.01, location=(x, y, z))

# Import CSV files
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        create_particles(os.path.join(input_dir, filename))
        bpy.context.scene.frame_set(int(filename.split('_')[1].split('.')[0]))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
```

## Usage

1. Configure SWIFT with `--enable-lightcone`.
2. Create a parameter file and run the SWIFT simulation.
3. Convert HDF5 output to CSV format using the provided Python script.
4. Import CSV data into Blender and create animations using the provided Blender script.

## Note

This project assumes familiarity with SWIFT and Blender. Adjust the scripts and configurations as needed for your specific use case and system setup.
```
