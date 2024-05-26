import Foundation

// Define a structure to represent the data
struct SimulationResult: Codable {
    let time: Double
    let density: Double
    let energy: Double
    let expansion: Double
    let gravitation: Double
}

// Read the JSON file and decode it into an array of SimulationResult objects
func loadSimulationResults(from file: URL) -> [SimulationResult]? {
    do {
        let data = try Data(contentsOf: file)
        let decoder = JSONDecoder()
        let results = try decoder.decode([SimulationResult].self, from: data)
        return results
    } catch {
        print("Error loading simulation results:", error)
        return nil
    }
}

// Use the function to load the simulation results
if let fileURL = Bundle.main.url(forResource: "simulation_results", withExtension: "json") {
    if let simulationResults = loadSimulationResults(from: fileURL) {
        // Successfully loaded simulation results
        for result in simulationResults {
            print("Time: \(result.time), Density: \(result.density), Energy: \(result.energy), Expansion: \(result.expansion), Gravitation: \(result.gravitation)")
        }
    } else {
        print("Failed to load simulation results.")
    }
} else {
    print("Simulation results JSON file not found.")
}
