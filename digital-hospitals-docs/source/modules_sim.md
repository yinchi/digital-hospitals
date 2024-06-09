# Simulation module

## Sequence diagram

```{kroki}
:type: plantuml

@startuml

participant User
participant "API server" as API
database DB
participant Orchestrator

User -> API: Simulation request
API -> DB: New simulation
DB --> API: OK; Initial simulation state
note right: State info from other services;\nmay include estimated future states

API --> User: 202 Accepted
API -> Orchestrator: New simulation

Orchestrator -> Worker ** : Job
activate Worker #77FF77
note right: One worker per\nsimulation replication

loop status check
User -> API: Simulation query
API -> DB: Fetch simulation status
DB --> API: Simulation status (running)
API --> User: Simulation status (running)
end

Worker --> DB --: Result
destroy Worker

==All workers completed==

User -> API: Simulation query
API -> DB: Fetch simulation status
DB --> API: Simulation status (finished)
API --> User: Simulation status (finished)

@enduml
```
1. User requests a new simulation.
1. Based on user input, the API server gathers additional simulation parameters from the database, and also adds a new simulation entry to the database.
1. The database returns the requested simulation parameters and acknowledges the new simulation job entry.
1. The API server acknowledges the new simulation request from the user.
1. The API server tells the job orchestrator to start a new simulation, passing along all the simulation parameters.
1. The job orchestrator sets up a number of workers to perform the simulation.
1. Each worker runs one simulation replication, writes the result to the database, and then self-destructs.
1. The user queries for the status of the simulation. The API fetches the result from the database and returns it to the user.

Note that the above diagram also shows a loop for checking the simulation status while it is still running.

## Integration with other modules

The simulation module can fetch data from the other modules to bootstrap the histopathology lab's state at the start of the simulation. The state of certain assets (e.g. lifts, staff, lab equipment) at other points during the simulation may also be defined.

* **Asset module**: The state of the transport assets (currently, just the lift) during the lifetime of the simulation is computed from the list of outages, including planned outages.
* **BIM module**: The runner times between locations can be obtained from the BIM module's results, and combined with the lift state to obtain the overall runner times between stages.
* **Resource module**: The resource allocation schedule for each resource can be obtained from this module.
* **Stock module**: The simulation can incorporate stock inventory tracking and block processes if the right type of consumable resource is not available.  The simulation module will start simulation based on the stock levels at the specified time, and report the estimated stock levels at the end of the simulation period.

## Items to report

- Turnaround times of specimens: mean, distribution (percentage completed within N days)
    - Mean time spent in each stage
- Resource utilisation (mean busy / mean allocated)
- Estimated final stock levels
- Other?