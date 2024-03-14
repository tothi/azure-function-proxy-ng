# Azure Function as a Reverse Proxy (for C2 ;) )

Using this project as a template for setting up C2 redirector as an Azure Function.

The folder [azurefunction](./azurefunction) contains the code for the Azure Function.

Configuration settings are in the beginning of [function_app.py](./azurefunction/function_app.py)
as Python vars.

Local testing (running from ./azurefunction folder) with the `func` command,
what is part of the
[Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools) suite:

```
func start
```

Pushing it to prod (function app should be created as <appname>):

```
func azure functionapp publish <appname>
```

Then the app can be accessed at <appname>[.]azurewebsites[.]net.

At target https[:]//TARGETHOST[:]TARGETPORT running an Nginx as local redirector
is recommended.

Here is a compatible nginx config provided in this repo: [nginx/redirector.conf](./nginx/redirector.conf).

The configured secret key restricts access of the C2 servers only from the
Azure Function endpoint.

