// Importing the Fortran modules
import cosmology_module
import Foundation

// Declaring variables to store the simulation results
var time: Double = 0.0
var density: Double = 1.0
var energy: Double = 1.0
var expansion: Double = 1.0
var gravitation: Double = 1.0

// Calling the Fortran subroutine to run the simulation
run_simulation(&time, &density, &energy, &expansion, &gravitation)

// Writing results to a CSV file
let data = "\(time),\(density),\(energy),\(expansion),\(gravitation)\n"
let fileURL = URL(fileURLWithPath: "simulation_results.csv")
try! data.write(to: fileURL, atomically: true, encoding: .utf8)
