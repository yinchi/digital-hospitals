# Stock management module

The stock management module tracks the level of consumable resources in the histopathology lab. The stock level can be changed via *transactions*, while *checkpoints* are used to capture the stock level of **all** consumable resources in the lab at a given point in time.

The [MongoDB](https://www.mongodb.com/) instance contains the following four collections relating to stock management:

```{kroki}
:type: plantuml
:caption: Right-click on the diagram to open in full size.

@startjson
{
  "transactions": [
    {
      "timestamp": "float (timestamp)",
      "change": "int",
      "updated_by": "str"
    },
    " ", " "
  ],
  "checkpoints": [
    {
      "timestamp": "float (timestamp)",
      "resources": [
          {
            "resource": "str",
            "level": "unsigned int"
          },
          " ", " "
      ]
    },
    " ", " "
  ],
  "orders": [
              {
                "resource": "str",
                "amount": "unsigned int",
                "placed_by": "str",
                "supplier": "str",
                "status": "Literal[\"Delivered\", \"Pending\", \"Cancelled\"]",
                "expected": "float (timestamp) | None",
                "delivered": "float (timestamp) | None"
              },
              " ", " "
            ],
  "policy": [
              {
                "resource": "str",
                "min_treshold": "unsigned int"
              },
              " ", " "
            ]
}
@endjson
```

Each JSON object in the middle column above corresponds to a MongoDB document. In the `policy` collection, `min_treshold` denotes the stock level for a resource below which a warning should be produced (by the frontend application).

:::{note}
An automatic ordering system for items in low stock can potentially be attached to this module.
:::

## Simulation module connection

The Simulation module can use the current stock status in order to bootstrap its starting state. (Using a past stock status may be possible by applying or rewinding a set of individual transactions from the closest checkpoint &mdash; functionality not currently planned.)