# Resource scheduling module

The resource scheduling module keeps track of resource levels over time, based on a set of schedules for each resource:

```{kroki}
:type: plantuml

@startuml schedule
clock "8-4 daily" as S1 with period 24 pulse 8 offset 8
clock "10-6 daily" as S2 with period 24 pulse 8 offset 10
clock "Mon-Fri weekly" as S3 with period 168 pulse 120

@0
@24
@48
@72
@96
@120
@144
@168

title Resource schedules
caption Hours
@enduml
```

A resource allocation specification looks like the following:

```{kroki}
:type: plantuml
:caption: Right-click on the diagram to open in full size.

@startjson
{
    "name": "My resource allocations",
    "created_by": "Admin_11",
    "time_unit": "h",
    "schedules": {
        "8-4 daily": [
            {"duration": 8, "state": false},
            {"duration": 8, "state": true},
            {"duration": 8, "state": false}
        ],
        "10-6 daily": [
            {"duration": 10, "state": false},
            {"duration": 8, "state": true},
            {"duration": 6, "state": false}
        ],
        "Mon-Fri weekly": [
            {"duration": 120, "state": true},
            {"duration": 48, "state": false}
        ],
        "etc.": ""
    },
    "resources": {
        "\"Staff A\"": [
            {
                "schedules": ["\"8-4 daily\"", "\"Mon-Fri weekly\""],
                "amount": 4
            },
            {
                "schedules": ["\"10-6 daily\"", "\"Mon-Fri weekly\""],
                "amount": 2
            }
        ],
        "Staff B": "",
        "etc.": ""
    }
}
@endjson
```
This results in the following resource levels for Staff A:

```{kroki}
:type: plantuml

@startuml resource
scale 24 as 40 pixels

robust "Staff A" as R
R has 6,5,4,3,2,1,0

@R
0 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+48 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+8 is 4
+2 is 6
+6 is 2
+2 is 0
+6 is 0

+48 is {hidden}

title Resource allocations
caption Hours
@enduml
```

## Simulation module connection

The Simulation module can apply a given resource allocation to control its staff and machine resource levels. However, consideration is required regarding the alignment of periodic schedules to the start date/time of the simulation model.