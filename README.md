# Simple currency server

#### Run
```bash
docker-compose up
```

#### Fill with data
`POST /database?merge=1` with body:
```json
{
    "new_data": [
        {
            "source": "USD",
            "dest": "RUR",
            "price": 33
        },
        {
            "source": "AMD",
            "dest": "RUR",
            "price": 4
        }
    ]
}
```

#### Check availability
`GET /convert?from=AMD&to=RUR&amount=42`
```json
{
    "from": "AMD",
    "to": "RUR",
    "amount": 42,
    "result": 168.0
}
```