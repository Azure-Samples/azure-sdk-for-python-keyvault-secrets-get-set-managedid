---
services: app-service, key-vault
platforms: python
author: lmazuel
---

# Use Key Vault from App Service with Managed Service Identity and Python

## Background
For Service-to-Azure-Service authentication, the approach so far involved creating an Azure AD application and associated credential, and using that credential to get a token. While this approach works well, there are two shortcomings:
1. The Azure AD application credentials are typically hard coded in source code. Developers tend to push the code to source repositories as-is, which leads to credentials in source.
2. The Azure AD application credentials expire, and so need to be renewed, else can lead to application downtime.

With [Managed Service Identity (MSI)](https://docs.microsoft.com/en-us/azure/app-service/app-service-managed-service-identity), both these problems are solved. This sample shows how a Web App can authenticate to Azure Key Vault without the need to explicitly create an Azure AD application or manage its credentials. 

>Here's another sample that how to use MSI from inside an Azure VM with a Managed Service Identity (MSI) - [https://github.com/Azure-Samples/resource-manager-python-manage-resources-with-msi](https://github.com/Azure-Samples/resource-manager-python-manage-resources-with-msi)

## Prerequisites
To run and deploy this sample, you need the following:
1. An Azure subscription to create an App Service and a Key Vault. 
2. [Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) to run the application on your local development machine.

### Step 1: Create an App Service with a Managed Service Identity (MSI)
<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fapp-service-msi-keyvault-python%2Fmaster%2Fazuredeploy.json" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
</a>

Use the "Deploy to Azure" button to deploy an ARM template to create the following resources:
1. App Service with MSI.
2. Key Vault with a secret, and an access policy that grants the App Service access to **Get Secrets**.
>Note: When filling out the template you will see a textbox labelled 'Key Vault Secret'. Enter a secret value there. A secret with the name 'secret' and value from what you entered will be created in the Key Vault.

Review the resources created using the Azure portal. You should see an App Service and a Key Vault. View the access policies of the Key Vault to see that the App Service has access to it. 

**IMPORTANT NOTE:**

>You CANNOT use the default Python version shipped with Azure WebApp to execute Azure SDK for Python code. You must install a WebApp extension for Python.
 This tutorial explains [how to update Python using an extension on Azure WebApp](https://docs.microsoft.com/visualstudio/python/managing-python-on-azure-app-service).
 The sample here works directly if you install the extension "Python 3.6.2 x86". Edit the `web.config` file if you wish to use another version of Python.

### Step 2: Grant yourself data plane access to the Key Vault
Using the Azure Portal, go to the Key Vault's access policies, and grant yourself **Secret Management** access to the Key Vault. This will allow you to run the application on your local development machine. 

1.	Search for your Key Vault in “Search Resources dialog box” in Azure Portal.
2.	Select "Overview", and click on Access policies
3.	Click on "Add New", select "Secret Management" from the dropdown for "Configure from template"
4.	Click on "Select Principal", add your account 
5.	Save the Access Policies

You can also create an Azure service principal either through
[Azure CLI](https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/),
[PowerShell](https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/)
or [the portal](https://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/)
and grant it the same access.


## Local dev installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7 and 3.5+

2.  We recommend that you use a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
    to run this example, but it's not required.
    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7):

    ```
    python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
    cd mytestenv
    source bin/activate      # Linux shell (Bash, ZSH, etc.) only
    ./scripts/activate       # PowerShell only
    ./scripts/activate.bat   # Windows CMD only
    ```

1.  Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/app-service-msi-keyvault-python.git
    ```

2.  Install the dependencies using pip.

    ```
    cd app-service-msi-keyvault-python-v4
    pip install -r requirements.txt
    ```

3.  Set up the environment variable `KEY_VAULT_URL` with your KeyVault URL or replace the variable in the example file.

1. Export these environment variables into your current shell or update the credentials in the example file.

    ```
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    ```

1. Run the sample.

    ```
    python example.py
    ```

1. This sample exposes two endpoints:
  
   - `/ping` : This just answers "hello world" and is a good way to test if your packages are installed correctly without testing Azure itself.
   - `/` : The MSI sample itself

## Installation on Azure

1. Set the `KEY_VAULT_URL` environment variable using the "Application Settings" of your WebApp.

1. Connect to the [Kudu console](https://github.com/projectkudu/kudu/wiki/Kudu-console) and install the dependencies. If you installed the Python 3.6.2x86 extension, the command line will be:

```shell
D:\home\python362x86\python.exe -m pip install -r D:\home\site\wwwroot\requirements.txt
```

> For automation purpose, you might use the [Kudu RestAPI](https://github.com/projectkudu/kudu/wiki/REST-API#command)

3. This repo is ready to be deployed using local git. Read this tutorial to get more information on [how to push using local git with CLI 2.0](https://docs.microsoft.com/azure/app-service/app-service-web-get-started-python#push-to-azure-from-git)

## At a glance

A default credential capable of handling most Azure SDK authentication scenarios.When environment variable configuration is present, it authenticates as a service principal. Then, the code is simply:

```python    
    credentials = DefaultAzureCredential()
    key_vault_client = KeyVaultClient(
        credentials
    )

    key_vault_uri = os.environ.get("KEY_VAULT_URI")
    secret_client = SecretClient(
        key_vault_uri,  # Your KeyVault URL
        credentials
    )
    secret = secret_client.get_secret(
        "secret",    # Name of your secret. If you followed the README 'secret' should exists
        ""           # The version of the secret. Empty string for latest
    )
```

## Summary

The web app was successfully able to get a secret at runtime from Azure Key Vault using your developer account during development, You do not have to worry about to authenticate.

## Azure Functions

Azure Functions being powered by Azure WebApp. Just copy the content of `run_example` into your Azure Functions with the right import.

## Troubleshooting

### Common issues when deployed to Azure App Service:

1. I see "The page cannot be displayed because an internal server error has occurred.", even on the "ping" endpoint

Make sure you have installed a Python extension for WebApp (see Step 1). If not, this tutorial explains [how to update Python using an extension on Azure WebApp](https://docs.microsoft.com/visualstudio/python/managing-python-on-azure-app-service).
 The sample here works directly if you install the extension "Python 3.6.2 x86". Edit the `web.config` file if you wish to use another version of Python.

1. Environment variables not setup on the System.

Check the environment variables exist. If these environment variables do not exist, they will be wrong.Note that after add environment variables, you need to restart your WebApp.

### Common issues across environments:

1. Access denied

The principal used does not have access to the Key Vault. The principal used in show on the web page. Grant that user (in case of developer context) or application "Get secret" access to the Key Vault.
