# BIM module

*FastAPI Swagger documentation*

This module updates the running time information of the histopathology department model whenever a new `.ifc` (Industry Foundation Classes) file is uploaded. The computed information constitues a graph representation of the histopathology department, with nodes representing locations within the histopathology lab and edges representing the path segments between them. The path segment information contains:

- The time required to complete the segment
- The transport assets required to complete the segment (e.g., a lift)

:::{error}
Since the running time computation can take a few minutes, we use a [background task](https://fastapi.tiangolo.com/tutorial/background-tasks/) to run the update; however, this is currently broken. (Todo: set up a proper task scheduler for this task.)
:::