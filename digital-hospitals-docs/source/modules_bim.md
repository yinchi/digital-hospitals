# BIM module

*FastAPI Swagger documentation*

This module updates the running time information of the histopathology department model whenever a new `.ifc` (Industry Foundation Classes) file is uploaded. The computed information constitues a graph representation of the histopathology department, with nodes representing locations within the histopathology lab and edges representing the path segments between them. The path segment information contains:

- The time required to complete the segment
- The transport assets required to complete the segment (e.g., a lift)

:::{error}
Since the running time computation can take a few minutes, we use a [background task](https://fastapi.tiangolo.com/tutorial/background-tasks/) to run the update; however, this is currently broken. (Todo: set up a proper task scheduler for this task.)
:::

Each running time computation request is associated with the following JSON data:
```{kroki}
:type: plantuml

@startjson
{
"_id": "(assigned by MongoDB)",
"requested": "float (timestamp)",
"requested_by": "str",
"status": "Literal[\"Running\", \"OK\", \"Error\"]",
"result": "dict | None",
"err_msg": "str | None"
}
@endjson
```
with the condition that `result` or `err_msg` should be set if and only if `status` is `"OK"` or `"Error"`, respectively.

:::{note}
All requests are stored in a MongoDB collection, with the latest successful update stored in a special single-document collection for quick retrieval.  Since all updates are stored, it should be possible to run a simulation based on the past BIM state of the lab.
:::

## Module connections

The BIM data can be combined with data from the [Asset status module](modules_asset) to determine the runner times for any timepoint in the past or future (using past or planned outage data for transport assets such as lifts).  This information can in turn be used by the Simulation module to predict the turnaround time of specimens.