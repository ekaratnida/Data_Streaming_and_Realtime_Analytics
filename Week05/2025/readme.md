### 1. Document
https://docs.google.com/document/d/1R7SqaHRGVkOy_ctLv-IdqYqNDChFF5zMPOZayR7KCaM/edit?tab=t.0

### 2. Example of timestamp
```
{
    "type" : "record",
    "name" : "schema",
    "fields" : [{
        "name" : "entryDate",
        "type" : ["null", {
            "type" : `**"string"**`,
            "logicalType" : "timestamp-micros"
        }],
        "default" : null
    }]
}
```
