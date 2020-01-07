---
page_type: sample
languages:
- python
products: 
- azure-app-service
- azure-key-vault
description: "How to set and get secrets from Azure Key Vault with Azure Managed Identities and Python."
urlFragment: get-set-keyvault-secrets-managed-id-python
---

# How to set and get secrets from Azure Key Vault with Azure Managed Identities and Python

## SDK Versions
In this sample, you will find the following folders:
* **v3** - references Key Vault SDK v3
* **v4** - references Key Vault SDK v4

## Background
For service to service authentication, the approach involved creating an Azure AD application and associated credential, and using that credential to get a token. While this approach works well, there are two shortcomings:
1. The Azure AD application credentials are typically hard coded in source code. Developers tend to push the code to source repositories as-is, which leads to credentials in source.
2. The Azure AD application credentials expire, and so need to be renewed, else can lead to application downtime.

With [Azure Managed Identities], both these problems are solved. This sample shows how a Web App can authenticate to Azure Key Vault without the need to explicitly create an Azure AD application or manage its credentials. 

>Here's another sample that demonstrates using an [Azure Managed Identities] from within an Azure VM. - [https://github.com/Azure-Samples/resource-manager-python-manage-resources-with-msi]

## Prerequisites
To run and deploy this sample, you need the following:
1. An Azure subscription to create an App Service and a Key Vault. 
2. [Azure CLI 2.0] to run the application on your local development machine.

### Step 1: Create an App Service with an Azure Managed Identity
<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fapp-service-msi-keyvault-python%2Fmaster%2Fazuredeploy.json" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
</a>

Use the "Deploy to Azure" button to deploy an ARM template to create the following resources:
1. App Service with [Azure Managed Identities].
2. Key Vault with a secret, and an access policy that grants the App Service access to **Get Secrets**.
>Note: When filling out the template you will see a textbox labeled 'Key Vault Secret'. Enter a secret value there. A secret with the name 'secret' and value from what you entered will be created in the Key Vault.

Review the resources created using the Azure portal. You should see an App Service and a Key Vault. View the access policies of the Key Vault to see that the App Service has access to it. 

**IMPORTANT NOTE:**

>You CANNOT use the default Python version shipped with Azure WebApp to execute Azure SDK for Python code. You must install a WebApp extension for Python.
 This tutorial explains [how to update Python using an extension on Azure WebApp].
 The sample here works directly if you install the extension "Python 3.6.2 x86". Edit the `web.config` file if you wish to use another version of Python.

### Step 2: Grant yourself data plane access to the Key Vault
Using the Azure Portal, go to the Key Vault's access policies, and grant yourself **Secret Management** access to the Key Vault. This will allow you to run the application on your local development machine. 

1.	Search for your Key Vault in “Search Resources dialog box” in Azure Portal.
2.	Select "Overview", and click on Access policies
3.	Click on "Add New", select "Secret Management" from the dropdown for "Configure from template"
4.	Click on "Select Principal", add your account 
5.	Save the Access Policies

You can also create an Azure service principal either through
[Azure CLI], [PowerShell] or [the portal] and grant it the same access.


## Local dev installation

1.  If you don't already have it, [install Python].

    This sample (and the SDK) is compatible with Python 2.7 and 3.5+.

2.  We recommend that you use a [virtual environment]
    to run this example, but it's not required.
    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install [virtualenv] for Python 2.7):

    ```
    python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
    cd mytestenv
    source bin/activate      # Linux shell (Bash, ZSH, etc.) only
    ./scripts/activate       # PowerShell only
    ./scripts/activate.bat   # Windows CMD only
    ```

3.  Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/azure-sdk-for-python-keyvault-secrets-get-set-managedid.git
    ```

4.  Run the following command to install dependencies for "SDK version 3" and "SDK version 4":

- SDK version 4

```
cd v4
pip install -r requirements.txt
```

- SDK version 3

```
cd v3
pip install -r requirements.txt
```

5.  Set up the environment variable `KEY_VAULT_URL` with your KeyVault URL or replace the variable in the example file.

6. Export these environment variables into your current shell or update the credentials in the example file.

    ```
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    ```

7. Run the sample.

    ```
    python example.py
    ```

8. This sample exposes two endpoints:
  
   - `/ping` : This just answers "hello world" and is a good way to test if your packages are installed correctly without testing Azure itself.
   - `/` : The MSI sample itself

## Deploying on Azure Web App

1. Set the `KEY_VAULT_URL` environment variable using the "Application Settings" of your Web App.

1. Connect to the [Kudu console] and install the dependencies. If you installed the Python 3.6.2x86 extension, the command line will be:

```shell
D:\home\python362x86\python.exe -m pip install -r D:\home\site\wwwroot\requirements.txt
```

> For automation purpose, you might use the [Kudu RestAPI]

3. This repo is ready to be deployed using local git. Read this tutorial to get more information on [how to push using local git with CLI 2.0]

## Summary

The web app was successfully able to get a secret at runtime from Azure Key Vault using your developer account during development, and using Azure Managed Identities when deployed to Azure, without any code change between local development environment and Azure. 
As a result, you did not have to explicitly handle a service principal credential to authenticate to Azure AD to get a token to call Key Vault. You do not have to worry about renewing the service principal credential either, since Azure Managed Identities takes care of that.

## Troubleshooting

### Common issues when deployed to Azure App Service:

1. I see "The page cannot be displayed because an internal server error has occurred.", even on the "ping" endpoint

Make sure you have installed a Python extension for WebApp (see Step 1). If not, this tutorial explains [how to update Python using an extension on Azure WebApp].
 The sample here works directly if you install the extension "Python 3.6.2 x86". Edit the `web.config` file if you wish to use another version of Python.

1. MSI is not setup on the App Service. 

Check the environment variables MSI_ENDPOINT and MSI_SECRET exist using [Kudu debug console]. If these environment variables do not exist, MSI is not enabled on the App Service. Note that after enabling MSI, you need to restart your WebApp.

### Common issues across environments:

1. Access denied

The principal used does not have access to the Key Vault. The principal used in show on the web page. Grant that user (in case of developer context) or application "Get secret" access to the Key Vault. 
  
## Contributing

This project has adopted the [Microsoft Open Source Code of Conduct]. For more information see the [Code of Conduct FAQ] or contact [opencode@microsoft.com] with any additional questions or comments.

<!-- LINKS -->
[Azure Managed Identities]: https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/
[https://github.com/Azure-Samples/resource-manager-python-manage-resources-with-msi]: https://github.com/Azure-Samples/resource-manager-python-manage-resources-with-msi
[Azure CLI 2.0]: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
[how to update Python using an extension on Azure WebApp]: https://docs.microsoft.com/visualstudio/python/managing-python-on-azure-app-service
[Azure CLI]: https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/
[PowerShell]: https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/
[the portal]: https://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/
[install Python]: https://www.python.org/downloads/
[virtual environment]: https://docs.python.org/3/tutorial/venv.html
[virtualenv]: https://pypi.python.org/pypi/virtualenv
[Kudu console]: https://github.com/projectkudu/kudu/wiki/Kudu-console
[Kudu RestAPI]: https://github.com/projectkudu/kudu/wiki/REST-API#command
[how to push using local git with CLI 2.0]: https://docs.microsoft.com/azure/app-service/app-service-web-get-started-python#push-to-azure-from-git
[how to update Python using an extension on Azure WebApp]: https://docs.microsoft.com/visualstudio/python/managing-python-on-azure-app-service
[Kudu debug console]: https://azure.microsoft.com/resources/videos/super-secret-kudu-debug-console-for-azure-web-sites/
[Microsoft Open Source Code of Conduct]: https://opensource.microsoft.com/codeofconduct/
[Code of Conduct FAQ]: https://opensource.microsoft.com/codeofconduct/faq/
[opencode@microsoft.com]: mailto:opencode@microsoft.com