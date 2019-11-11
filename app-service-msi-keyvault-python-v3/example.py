from msrestazure.azure_active_directory import MSIAuthentication, ServicePrincipalCredentials
from azure.keyvault import KeyVaultClient
import os

from flask import Flask
app = Flask(__name__)


def get_key_vault_credentials():
    """This tries to get a token using MSI, or fallback to SP env variables.
    """
    if "APPSETTING_WEBSITE_SITE_NAME" in os.environ:
        return MSIAuthentication(
            resource='https://vault.azure.net'
        )
    else:
        return ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID'],
            resource='https://vault.azure.net'
        )


def run_example():
    """MSI Authentication example."""

    # Get credentials
    credentials = get_key_vault_credentials()

    # Create a KeyVault client
    key_vault_client = KeyVaultClient(
        credentials
    )

    key_vault_uri = os.environ.get("KEY_VAULT_URI")

    secret = key_vault_client.get_secret(
        key_vault_uri,  # Your KeyVault URL
        "secret",       # Name of your secret. If you followed the README 'secret' should exists
        ""              # The version of the secret. Empty string for latest
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
