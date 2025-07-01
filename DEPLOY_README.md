# Vercel Deployment Guide

This guide will walk you through deploying your Next.js and Python monorepo to Vercel.

## 1. Project Structure

Your project is a monorepo with the following structure:

- `/client`: Contains the Next.js frontend application.
- `/server`: Contains the Python (FastAPI) backend application.
- `/vercel.json`: The configuration file for Vercel.

## 2. Vercel Configuration (`vercel.json`)

The `vercel.json` file is the most important part of the deployment process. It tells Vercel how to build and route your application. Here is the correct configuration for your project:

```json
{
    "version": 2,
    "builds": [
        {
            "src": "client/next.config.ts",
            "use": "@vercel/next"
        },
        {
            "src": "server/app/main.py",
            "use": "@vercel/python"
        }
    ],
    "rewrites": [
        {
            "source": "/api/(.*)",
            "destination": "/server/app/main.py"
        },
        {
            "source": "/(.*)",
            "destination": "/client"
        }
    ]
}
```

**Explanation:**

- **`builds`**: This section tells Vercel how to build each part of your application.
  - The first build configuration tells Vercel to build the Next.js application located in the `client` directory.
  - The second build configuration tells Vercel to build the Python application located in the `server` directory.
- **`rewrites`**: This section tells Vercel how to route incoming requests.
  - The first rewrite rule routes all requests starting with `/api/` to the Python backend.
  - The second rewrite rule routes all other requests to the Next.js frontend.

## 3. Deployment Steps

1.  **Push to Git:** Make sure your code is pushed to a Git repository (GitHub, GitLab, or Bitbucket).

2.  **Create a Vercel Project:**
    - Go to your Vercel dashboard and click "Add New... -> Project".
    - Import your Git repository.

3.  **Configure Project Settings:**
    - **Framework Preset:** Vercel should automatically detect that you are using Next.js.
    - **Root Directory:** Make sure the root directory is set to the root of your project (not `/client` or `/server`).

4.  **Add Environment Variables:**
    - In your Vercel project settings, go to the "Environment Variables" section.
    - Add any environment variables that your application needs (e.g., database connection strings, API keys).

5.  **Deploy:**
    - Click the "Deploy" button.
    - Vercel will now build and deploy your application.

If you follow these steps, your application should deploy successfully to Vercel. The login page will be the first page that users see, as configured in your Next.js application.
