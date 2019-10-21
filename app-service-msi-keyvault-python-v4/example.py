from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

import os

from flask import Flask
app = Flask(__name__)


KEY_VAULT_URI = None  # Replace by something like "https://xxxxxxxxx.vault.azure.net/"


def run_example():
    """MSI Authentication example."""

    # Get credentials
    credentials = DefaultAzureCredential()

    key_vault_uri = os.environ.get("KEY_VAULT_URI", KEY_VAULT_URI)
    
    # Create a secret client
    secret_client = SecretClient(
        key_vault_uri,  # Your KeyVault URL
        credentials
    )

    secret = secret_client.get_secret(
        "secret",    # Name of your secret. If you followed the README 'secret' should exists
        ""           # The version of the secret. Empty string for latest
    )
    return "My secret value is {}".format(secret.value)


@app.route('/')
def hello_world():
    try:
        return run_example()
    except Exception as err:
        return str(err)


@app.route('/ping')
def ping():
    return "Hello world"


if __name__ == '__main__':
    app.run()
