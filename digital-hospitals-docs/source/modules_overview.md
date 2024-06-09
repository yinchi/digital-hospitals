# Modules overview

The DT consists of multiple modules as shown below.

```{kroki}
:type: plantuml

@startuml components
[Asset\nstatus\nmodule] as Asset
[BIM\nmodule] as BIM
[Simulation\nmodule] as DES
[Stock\nManagement\nmodule] as Stock
[Resource\nscheduling\nmodule] as Resource
database "Database server" as db

Asset <--> db
BIM <--> db
Resource <--> db
Stock <--> db
DES <--> db

DES <-- Asset : Fetch lift status
DES <-- BIM : Fetch runner times
DES <-- Resource : Fetch staff/resource\nallocation schedules
DES <-- Stock : Fetch stock levels\nfor consumables
@enduml
```

In the current implementation, the database is a [MongoDB](https://www.mongodb.com/) instance.
Each module uses its own database, which contains one or more collections.
A collection is a set of "documents" or JSON objects, each with an "_id" field set internally by MongoDB.

## FastAPI

Each module will have a FastAPI interface. To view the generated Swagger documentation for each interface, click [here](/dev){.external}.

Inputs to each interface shall be validated using [Pydantic](https://docs.pydantic.dev/latest/api/base_model/). Only the fields required to deliver the defined functionality should be included in the validation &mdash; Pydantic ignores additional fields by default. This allows for the API to be extended in the future without breaking previous versions; however, fields should *never* be removed.