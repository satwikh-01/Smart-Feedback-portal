# Railway Deployment Guide

This guide provides the definitive, simplified instructions for deploying your monorepo to Railway. The project is now fully configured for a seamless deployment from GitHub.

**The key to success is setting the "Root Directory" for each service correctly in the Railway dashboard.**

## 1. Project Structure

Your project is a monorepo with the following structure:

- `/client`: Contains the Next.js frontend application and its `Dockerfile`.
- `/server`: Contains the Python (FastAPI) backend application, its `Dockerfile`, and a `run.sh` startup script.

We have removed the `railway.toml` files to simplify the process. Railway will now automatically use the `Dockerfile` it finds in the root directory of each service.

## 2. Deployment Steps

### Step 1: Create a New Project from GitHub

1.  Go to your [Railway Dashboard](https://railway.app/dashboard) and click **"New Project"**.
2.  Select **"Deploy from GitHub repo"**.
3.  Choose your repository (`smart-feedback-portal`).

### Step 2: Configure the Services (The Crucial Step)

You must tell Railway where each service lives.

1.  **For the Server:**
    -   Add a new service.
    -   In the service's **Settings** tab, set the **Root Directory** to `./server`.
    -   **This tells Railway to look inside the `/server` folder. It will find the `Dockerfile` there and use it to build the service.**

2.  **For the Client:**
    -   Add another service.
    -   In its **Settings** tab, set the **Root Directory** to `./client`.
    -   **This tells Railway to look inside the `/client` folder and use the `Dockerfile` it finds there.**

If you do not set the **Root Directory** correctly, Railway will use its default (Nixpacks) builder at the project root, which will fail.

### Step 3: Add Environment Variables

The application will not run without these secrets.

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

Once the services are configured with the correct **Root Directory** and the variables are set, Railway will automatically build and deploy your application using the correct Dockerfiles.

This is the most direct and reliable way to deploy your monorepo.
