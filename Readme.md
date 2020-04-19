### TimerViewer

#### Config

```json
{
    "map": {
        // 格式   "显示字段": "json中对应字段"
        "Class": "class",
        "Times": "times",
        "ms": "ms"
    },
    // 子
    "child": "child"
}
```

#### TestData

```json
{
    "times": 0,
    "class": "com.mirakyux.gdparent",
    "ms": "20001",
    "child" : [
        {
            "times": 1,
            "class": "com.mirakyux.parento",
            "ms": "5001"
        },
        {
            "times": 2,
            "class": "com.mirakyux.parenttw",
            "ms": "5000"
        },
        {
            "times": 3,
            "class": "com.mirakyux.parentth",
            "ms": "10000",
            "child": [
                {
                    "times": 4,
                    "class": "com.mirakyux.son",
                    "ms": "10000"
                }
            ]
        }
    ]
}
```