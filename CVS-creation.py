import csv

# Define your simulation data (time, density, energy, expansion, gravitation)
simulation_data = [
    [0.0, 1.0, 1.0, 1.0, 1.0],
    [0.01, 0.9, 1.1, 1.01, 0.99],
    [0.02, 0.81, 1.21, 1.0301, 0.9801],
    # Add more data rows as needed
]

# Define the file path for the CSV file
csv_file_path = "simulation_data.csv"

# Write simulation data to CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header row
    writer.writerow(['Time', 'Density', 'Energy', 'Expansion', 'Gravitation'])
    
    # Write data rows
    for row in simulation_data:
        writer.writerow(row)

print("Data exported to:", csv_file_path)
