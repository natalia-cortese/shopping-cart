# How to run this project

Download the repository files, inside the repository folder run:

```
python3 -m venv .venv
. .venv/bin/activate
pip3 install requirements.txt
```

These command are going to activate the virtual environment and install the requirements.
Once this process is finished, run:

> flask run

This command will run the app and leave it available under the URL:
http://127.0.0.1:5000/

To Test the API Endpoints follow the following for access the Workspace on Postman:
[Collection](https://api.postman.com/collections/5361303-8abf1ef1-d9cc-4439-9f9c-bf9b67f0287f?access_key=PMAT-01GW4ZZ1KWCREED7435AKAB373)
You can import these collections inside your postman account using the URL.

# How to run the requests

This requests has an order that you should follow:
  - Any post inside the API Rest should had a Bearer Token. So you should run the following to get your token

```
curl --location 'http://127.0.0.1:5000
/login' \
--data '{
	"username": <username>,
	"password": <password>
}'
```
That endpoint requires to generate a User, you can run:
```
curl --location 'http://127.0.0.1:5000
/user/' \
--data '{
	"username": "Natalia",
	"password": "qwerty1234"
}'
```
After that you can run a Post, for example:
```
/products/martillo' \
--header 'Authorization: bearer <token>' \
--data '{
    "price": 15.50,
    "quantity": 50,
    "category": "Equipment"
}'
```
