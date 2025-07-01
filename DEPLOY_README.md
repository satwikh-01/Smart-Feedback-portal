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

In your client service on Railway, you will need to set the following environment variable:

-   `NEXT_PUBLIC_API_URL`: The URL of your deployed backend service on Railway.

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
    - In your Railway project settings, go to the "Variables" section.
    - Add any environment variables that your application needs (e.g., database connection strings, API keys).
    - **Crucially, set the `NEXT_PUBLIC_API_URL` on the client service.**

6.  **Deploy:**
    - Once your services are linked and your environment variables are set, Railway will automatically deploy your application.

If you follow these steps, your application should deploy successfully to Railway.
