import bpy
import csv
import os

csv_folder_path = "/path/to/your/csv/files/"

csv_files = sorted([f for f in os.listdir(csv_folder_path) if f.endswith(".csv")])

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

particles = {}

for frame_number, csv_file in enumerate(csv_files):
    full_path = os.path.join(csv_folder_path, csv_file)
    with open(full_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            x, y, z = float(row["x"]), float(row["y"]), float(row["z"])
            density, energy, time = float(row["density"]), float(row["energy"]), float(row["time"])
            particle_id = (x, y, z)

            if particle_id not in particles:
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(x, y, z))
                obj = bpy.context.object
                obj.name = f"Particle_{x:.2f}_{y:.2f}_{z:.2f}"
                particles[particle_id] = obj

                obj["density"] = density
                obj["energy"] = energy
                obj["time"] = time
            else:
                obj = particles[particle_id]

            obj.location = (x, y, z)
            obj.keyframe_insert(data_path="location", frame=frame_number)

            obj["density"] = density
            obj.keyframe_insert(data_path='["density"]', frame=frame_number)

            obj["energy"] = energy
            obj.keyframe_insert(data_path='["energy"]', frame=frame_number)

bpy.context.scene.frame_end = len(csv_files)

print("Import and animation setup completed.")
