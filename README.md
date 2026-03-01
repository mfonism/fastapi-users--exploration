# Explore

In which I explore `fastapi-users`

## Start server

`uv run fastapi dev src/explore/app.py`

## Auth route examples

Login:

`curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=alice@example.com&password=strongpass123"`

Register:

`curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"email":"alice@example.com","password":"strongpass123"}'`
