# Railway Deployment Guide

This guide will walk you through deploying your Next.js and Python monorepo to Railway by linking your GitHub repository.

## 1. Project Structure

Your project is a monorepo with the following structure, which is now fully configured for Railway:

- `/client`: Contains the Next.js frontend application.
- `/server`: Contains the Python (FastAPI) backend application.
- `/server/railway.toml`: The configuration file for the server.
- `/client/railway.toml`: The configuration file for the client.
- `/server/Dockerfile` & `/client/Dockerfile`: Define how to build each service.
- `/server/run.sh`: A robust startup script for the server.

## 2. Railway Configuration

The `railway.toml` files are the key to telling Railway how to build your services. Their configuration is now correct.

### Server (`server/railway.toml`)

```toml
[build]
  dockerfilePath = "Dockerfile"

[deploy]
restartPolicy = "on-failure"
```

### Client (`client/railway.toml`)

```toml
[build]
  dockerfilePath = "Dockerfile"

[deploy]
restartPolicy = "on-failure"
```

## 3. Deployment Steps

The process is now very straightforward and does not require using the command line.

### Step 1: Create a New Project from GitHub

1.  Go to your [Railway Dashboard](https://railway.app/dashboard) and click **"New Project"**.
2.  Select **"Deploy from GitHub repo"**.
3.  Choose your repository (`smart-feedback-portal`).

### Step 2: Configure the Services

1.  **For the Server:**
    -   Add a new service.
    -   In the service's **Settings** tab, set the **Root Directory** to `./server`. Railway will automatically find and use the `railway.toml` and `Dockerfile` in this directory.

2.  **For the Client:**
    -   Add another service.
    -   In its **Settings** tab, set the **Root Directory** to `./client`. Railway will automatically find and use the configuration files here as well.

### Step 3: Add Environment Variables

This is the most important step. The application will not run without these secrets.

1.  **For the Server (`server` service):**
    -   Go to the service's **Variables** tab.
    -   Add the following secrets:
        -   `SUPABASE_URL`: The URL of your Supabase project.
        -   `SUPABASE_KEY`: The `anon` key for your Supabase project.
        -   `SECRET_KEY`: A strong, randomly generated secret key.
        -   `ALGORITHM`: The algorithm for JWTs (e.g., `HS256`).
        -   `ACCESS_TOKEN_EXPIRE_MINUTES`: e.g., `30`.
        -   `GEMINI_API_KEY`: Your API key for the Gemini service.

2.  **For the Client (`client` service):**
    -   Go to its **Variables** tab.
    -   Add the following variable:
        -   `NEXT_PUBLIC_API_URL`: This is the public URL of your deployed server. You can get this from the **Settings** tab of your `server` service on Railway (it will look like `https://your-server-name.up.railway.app`).

### Step 4: Deploy

Once the services are configured and the variables are set, Railway will automatically build and deploy your application. Any new push to your GitHub repository will trigger a new deployment.

That's it! The project is now set up for a simple, automated deployment workflow.
