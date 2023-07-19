# Vending Machine

![Vending Machine](docs/vending_machine.png)

## How to run the project:
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `python manage.py runserver`

## How to insert data
1. Create a super user: `python manage.py createsuperuser`
2. Add a product: `http://localhost:8000/admin/vending/product/add/`
3. Add a vending machine slot: `http://localhost:8000/admin/vending/vendingmachineslot/add/`


## This app allows to:

### Manage slots, products, users and authentication via the Django Admin interface:
![Admin interface](docs/admin_interface.png)
### Register new users:
  Request:
  ```bash
    curl --location 'http://localhost:8000/auth/register/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "first_name": "Carlos",
      "last_name": "Hurtado",
      "username": "carlos.hurtado",
      "email": "carlos.hurtado@.gmail.com",
      "password": "Carlos123!"
    }'
  ```
  Response: 
  ```
    {
     "error" : false,
     "message" : "User created successfully"
    }
  ```
### Login:
  Request:
  ```bash
    curl --location 'http://localhost:8000/auth/login/' \
    --header 'Content-Type: application/json' \
    --data '{
      "username": "carlos.hurtado",
      "password": "Abacum"
    }'
  ```
  Response:
  ```
    {
     "email" : "carlos.hurtado@abacum.io",
     "first_name" : "",
     "last_name" : "",
     "token" : "e9cc3e99b8c009f0707e22d9a8336516f3d15450"
    }
  ```
### Logout:
  Request:
  ```bash
    curl --location --request POST 'http://localhost:8000/auth/logout/' \
    --header 'Authorization: Token e9cc3e99b8c009f0707e22d9a8336516f3d15450'
  ```
  Response:
  This will return a `200` status for a sucessful logout or a `401` if the given token was not found.
### Query the vending machine slots:
  Request:
  ```bash
    curl --location 'http://localhost:8000/slots/' \
    --header 'Authorization: Token e9cc3e99b8c009f0707e22d9a8336516f3d15450'
  ```
  Response:
  ```
    [
       {
          "coordinates" : list[
             1,
             1
          ],
          "id" : "c5642e1b-e373-4dfe-be7e-48189112abb2",
          "product" : {
             "id" : "8d91122c-2e16-4be9-87ed-45c796f0659c",
             "name" : "Chips",
             "price" : "1.50"
          },
          "quantity" : 1
       },
       {
          "coordinates" : [
             2,
             1
          ],
          "id" : "03163620-d823-49e8-bc27-aa5295b91492",
          "product" : {
             "id" : "0c3b1d08-e145-4290-bc30-d961ed8efa87",
             "name" : "Sandwich",
             "price" : "3.50"
          },
          "quantity" : 7
       }
    ]
  ```
### Get balance for your personal wallet:
```bash
  `curl --location 'http://localhost:8000/wallet' \
  --header 'Authorization: Token e9cc3e99b8c009f0707e22d9a8336516f3d15450'
```
### Topping up your wallet's balance:
  Request:
  ```bash
    curl --location 'http://localhost:8000/wallet/' \
    --header 'Authorization: Token e9cc3e99b8c009f0707e22d9a8336516f3d15450' \
    --header 'Content-Type: application/json' \
    --data '{
      "amount": 10.5
    }'
  ```
  Response:
  This will return a `200` status
### Place an order:
  Request:
  ```bash
  curl --location 'http://localhost:8000/order/' \
  --header 'Authorization: Token e5fbd781dc39635d7e0da5696de85e13b85f1029' \
  --header 'Content-Type: application/json' \
  --data '{
    "items": [
      {
        "id": "c5642e1be3734dfebe7e48189112abb2",
        "quantity": 1
      },
      {
        "id": "03163620-d823-49e8-bc27-aa5295b91492",
        "quantity": 2
      }
    ]
  }'
  ```
  Sucess response:
  ```
  {
    "error": false,
    "message": "order processed successfully. Enjoy your products!"
  }
  ```
  Not enough products response:
  ```
    {
      "error": true,
      "errors": [
        "There are only 7 Sandwich, and you are trying to buy 10",
        "There are only 1 Chips, and you are trying to buy 4"
      ]
    }
  ```
  Not enough money response:
  ```
    {
      "error": true,
      "errors": [
        "You don't have enough money to complete the order"
      ]
    }
  ```

## Pending improvements:

- Create separate app for Auth.
- Use a more robust mechanism for auth: JWT, OAuth.
- Create dedicated services and use cases for all operations.
- Create missing unit and integration tests.
- Define a more structured payload for success and error responses.
- Provide seed data and command to set up the app for the first time.
- Integrate formatter to Git hooks.