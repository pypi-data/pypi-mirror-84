# Gumroad API Client

A Python API client for interacting with the Gumroad API (<https://gumroad.com/api>).  Comments, suggestions, and
improvements are always welcome. Be sure to follow [@opsdisk](https://twitter.com/opsdisk) on Twitter for the latest
updates.

```none
Note that not all of the endpoints and HTTP verbs supported by the Gumroad API have been added.
```

## Installation

```bash
pip install pygumroad
```

```bash
git clone https://github.com/opsdisk/pygumroad.git
cd pygumroad
virtualenv -p python3.7 .venv  # If using a virtual environment.
source .venv/bin/activate  # If using a virtual environment.
pip install -r requirements.txt
python setup.py install
```

## Update Credentials

If using a secrets file, create/update the `gumroad_secrets.json` file with the host and API key.  See the usage section
on how to pass a secrets dictionary.

```bash
cp gumroad_secrets_empty.json gumroad_secrets.json
```

```json
{
    "gumroad": {
        "host": "api.gumroad.com",
        "token": "7a4d...b388",
    }
}
```

## Usage

```python
import pygumroad

# Pass a secrets file.
full_path_to_secrets_file_location="/home/user/gumroad_secrets.json"
gumroad_client = pygumroad.GumroadClient(secrets_file_location=full_path_to_secrets_file_location)

# Pass a secrets dictionary.
secrets_dict = {
    "gumroad": {
        "host": "api.gumroad.com",
        "token": "7a4d...b388",
    }
}

gumroad_client = pygumroad.GumroadClient(secrets_dict=secrets_dict)
all_products = gumroad_client.retrieve_all_products()

for product in all_products:
    print(f"Product Name: {product['name']} - Product ID: {product['id']}")


all_sales = gumroad_client.retrieve_all_sales()

for sale in all_sales:
    print(f"Product: {sale['product_name']} was sold on {sale['created_at']}")

```
