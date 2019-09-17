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

## Folders introduction
Two folders are referred to different version of Azure SDK.
* app-service-msi-keyvault-python-v3 referenced to following packages:
  * [azure-keyvault]
* app-service-msi-keyvault-python-v4 referenced to following packages:
  * [azure-keyvault-secrets]
  * [azure-identity]
