# AAD User Token Fetcher App
This is a simple flask application with one endpoint that takes the user to the organization's AAD SSO page, and upon a succesful login displays the user access token.

## Development
.devcontainer folder is included, but needs the corporate ca-bundle.crt file. Copy this from your local machine to .devcontainer/ca-bundle.crt

## AD App registration
The app needs to be registered on Azure Active Directory (AAD). To run this app the tenant and client IDs must be available as environment variables (see .env.template). The redirect endpoint needs to be registered in AAD App Registration (default http://localhost:$PORT/redirect)

## Running locally
Run 
```bash
cp .env.template .env
```
, and fill the created .env file with tenant and client ID from AD- 

Run with 
```bash
docker compose up
```

Visit localhost:3000 in your browser