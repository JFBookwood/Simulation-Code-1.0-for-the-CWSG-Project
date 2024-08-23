import bpy
import csv


def load_csv(filepath):
    data = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            data.append([float(row[0]), float(row[1]), float(row[2])])
    return data


def load_data_main():
    # Your Path
    csv_files = [
'Path'
    ]

    
    all_data = []
    for filepath in csv_files:
        data = load_csv(filepath)
        all_data.extend(data)

    return all_data


def create_particles(data):
    bpy.ops.object.select_all(action='DESELECT')

    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0, 0))
    particle_template = bpy.context.object

   
    for idx, pos in enumerate(data):
        new_particle = particle_template.copy()
        new_particle.location = pos
        new_particle.name = f'Particle_{idx}'
        bpy.context.collection.objects.link(new_particle)


def create_particles_main():
    
    all_data = load_data_main()

    
    create_particles(all_data)


create_particles_main()
