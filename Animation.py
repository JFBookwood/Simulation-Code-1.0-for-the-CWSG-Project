import bpy
import csv

csv_folder_path = "/path/to/your/csv/files/"

csv_files = ["output_0.00.csv", "output_0.01.csv", "output_0.02.csv"]

frame_number = 0

for csv_file in csv_files:
    full_path = csv_folder_path + csv_file
    with open(full_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            x, y, z = float(row["x"]), float(row["y"]), float(row["z"])
            density, energy, time = float(row["density"]), float(row["energy"]), float(row["time"])

            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05
