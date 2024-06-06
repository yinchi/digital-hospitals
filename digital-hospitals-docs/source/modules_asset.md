# Asset status module

This module tracks the status of fixed assets, e.g. lifts. In the current model, there is only one tracked asset, the lift connecting the two floors of the histopathology lab.

:::{note}
For resources with schedule-based capacities, e.g. staff, use the Resource Scheduling module.
:::

Associated with each asset is a [MongoDB](https://www.mongodb.com/) collection of past, current and/or planned outages:

```{kroki}
:type: plantuml

@startuml
concise "Lift outages" as Lift
scale 36000 as 72 pixels

@0:00:00
Lift is "ended" #red

@10:00:00
Lift is {-}

@25:00:00
Lift is "current" #pink

@35:00:00
Lift is {-}

@60:00:00
Lift is "planned" #AliceBlue

@70:00:00
Lift is {-}

highlight 0 to 30:00:00 #lightgray;line:DimGrey
highlight 30:00:00 to 80:00:00 #white : Current time = 30

@enduml
```

Each past or planned service outage is represented in JSON as follows:

```{kroki}
:type: plantuml

@startjson
{
"_id": "(assigned by MongoDB)",
"start": "float (timestamp)",
"end ": "float (timestamp)",
"state": "Literal[\"ended\", \"current\", \"planned\", \"cancelled\"]",
"updated": "float (timestamp)",
"updated_by": "str"
}
@endjson
```

Timestamps beyond the `updated` value refer to planned events.

:::{note}
Entries must be updated via a database write whenever an outage is started/&#8203;completed/&#8203;cancelled, with the `state` field changed accordingly. The module will not assume that a planned event (start/stop of an outage) actually happened.

When guessing the state of an asset, a rule should be formed for how to handle outages that are marked as "current" or "planned", but with start times in the past (e.g. due to outdated outage data).
:::

## Module connections

The asset status data can be combined with [BIM data](modules_bim) to determine the runner times for any timepoint in the past or future.  This information can in turn be used by the Simulation module to predict the turnaround time of specimens.