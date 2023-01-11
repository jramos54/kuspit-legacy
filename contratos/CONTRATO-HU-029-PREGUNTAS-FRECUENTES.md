
## 1. Listar preguntas frecuentes

### URL:
```
user/frequent_questions/
```

### METHOD:
#### GET

### PARAMS:
```
```

### BODY:
```
```

### RESPONSE 200:
```
{
    "count": integer,
    "next": string,
    "previous": string,
    "results": [
        {
            "question": integer,
            "answer": integer,
            "status": boolean
        },
        ...
    ]
}
```

### RESPONSE 40X:
```
{
    "detail": string
}
```

## 2. Update/Delete question

### URL:
```
user/frequent_questions/
```

### METHOD:
#### PUT

### PARAMS:
```
# TODO: revisar si esto es necesario
?question_id=1 **administrator** 
```

### BODY:
```
{
            "question": integer,
            "answer": integer,
            "status": boolean
}
```


### RESPONSE 202:
```
{
            "customer_id": integer,
            "persona_fisica": boolean,
            "persona_moral": boolean,
}
```

### RESPONSE 40X:
```
{
    "detail": string
}
```