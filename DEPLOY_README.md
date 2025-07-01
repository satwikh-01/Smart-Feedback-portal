# Railway Deployment Guide

This guide will walk you through deploying your Next.js and Python monorepo to Railway.

## 1. Project Structure

Your project is a monorepo with the following structure:

- `/client`: Contains the Next.js frontend application.
- `/server`: Contains the Python (FastAPI) backend application.
- `/railway.toml`: The configuration file for the server.
- `/client/railway.toml`: The configuration file for the client.

## 2. Railway Configuration

We have two `railway.toml` files, one for the server and one for the client.

### Server `railway.toml`

```toml
[build]
  dockerfilePath = "server/Dockerfile"

[deploy]
restartPolicy = "on-failure"
```

### Client `railway.toml`

```toml
[build]
  dockerfilePath = "client/Dockerfile"

[deploy]
restartPolicy = "on-failure"
```

## 3. Environment Variables

You must set the following environment variables in your Railway project settings.

### Server (`smart-feedback-portal-server`)

Go to your server application's "Variables" page on Railway and add the following:

-   `SUPABASE_URL`: The URL of your Supabase project.
-   `SUPABASE_KEY`: The `anon` key for your Supabase project.
-   `SECRET_KEY`: A strong, randomly generated secret key for signing JWTs.
-   `ALGORITHM`: The algorithm to use for JWT signing (e.g., `HS256`).
-   `ACCESS_TOKEN_EXPIRE_MINUTES`: The expiry time for access tokens in minutes (e.g., `30`).
-   `GEMINI_API_KEY`: Your API key for the Gemini service.

### Client (`smart-feedback-portal-client`)

Go to your client application's "Variables" page on Railway and add the following:

-   `NEXT_PUBLIC_API_URL`: The public URL of your deployed server application on Railway.

## 4. Deployment Steps

1.  **Install Railway CLI:** Follow the instructions on the [Railway website](https://docs.railway.app/cli/installation) to install the `railway` CLI.

2.  **Login to Railway:**
    ```bash
    railway login
    ```

3.  **Create a Railway Project:**
    ```bash
    railway init
    ```

4.  **Link Services:**
    - In your Railway project, you will need to create two services, one for the client and one for the server.
    - For each service, you will need to link it to the appropriate directory in your monorepo.

5.  **Add Environment Variables:**
    - In your Railway project settings, go to the "Variables" section for each service.
    - **Crucially, add all the required environment variables listed above.**

6.  **Deploy:**
    - Once your services are linked and your environment variables are set, Railway will automatically deploy your application.

If you follow these steps, your application should deploy successfully to Railway.
