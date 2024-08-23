import bpy
import json

# Load simulation results from JSON file
def load_simulation_results(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Create a Blender mesh to represent the simulation data
def create_mesh(data):
    vertices = [(index, result['density']) for index, result in enumerate(data)]
    edges = [(index, index + 1) for index in range(len(data) - 1)]
    
    mesh = bpy.data.meshes.new(name="SimulationMesh")
    mesh.from_pydata(vertices, edges, [])
    mesh.update()
    
    return mesh

# Create an empty object to hold the mesh
def create_object(mesh):
    obj = bpy.data.objects.new(name="SimulationObject", object_data=mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# Animate the simulation mesh
def animate_mesh(obj, data):
    for index, result in enumerate(data):
        obj.location = (result['time'], result['density'], 0)  # Adjust location based on simulation data
        obj.keyframe_insert(data_path="location", frame=index + 1)  # Insert keyframe for each data point

# Main function to run the visualization
def main(filepath):
    # Load simulation results
    simulation_data = load_simulation_results(filepath)
    
    # Create mesh and object
    mesh = create_mesh(simulation_data)
    obj = create_object(mesh)
    
    # Animate the object
    animate_mesh(obj, simulation_data)

# Call the main function with the path to the JSON file
if __name__ == "__main__":
    filepath = "/path/to/simulation_results.json"
    main(filepath)
