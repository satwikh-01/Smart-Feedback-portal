# Fixing the Railway Deployment

There are several issues that could be causing the 404 and 308 errors. Follow these steps carefully to fix the deployment.

## 1. Server Configuration

### 1.1. Root Directory

In the Railway dashboard for your **`server`** service, go to the **Settings** tab and find the **Build** section. The **Root Directory** must be set to exactly `./server`.

### 1.2. Port

You do not need to set a `PORT` environment variable. The `Dockerfile` is now configured to use the port that Railway provides.

### 1.3. Docker Configuration

The `server/Dockerfile` now starts the application directly, so the `run.sh` script has been removed.

## 2. Client Configuration

### 2.1. Root Directory

In the Railway dashboard for your **`client`** service, go to the **Settings** tab and find the **Build** section. The **Root Directory** must be set to exactly `./client`.

### 2.2. Environment Variable

In the Railway dashboard for your **`client`** service, go to the **Variables** tab. You must have an environment variable named `NEXT_PUBLIC_API_URL`. The value of this variable must be the public URL of your **`server`** service (e.g., `https://my-server-service.up.railway.app`).

## 3. Final Checklist

- [ ] `server` service Root Directory is set to `./server`.
- [ ] `client` service Root Directory is set to `./client`.
- [ ] `client` service has a `NEXT_PUBLIC_API_URL` environment variable pointing to the `server`'s public URL.
- [ ] You have **not** set a `PORT` environment variable in your `server` service.

### 1.4. Environment Variables (The Most Likely Cause of the 502 Error)

The `server` application will crash if it's missing required environment variables. This is the most likely reason you are seeing a **502 Bad Gateway** error.

Go to the **Variables** tab for your `server` service in the Railway dashboard and ensure that **all** of the following variables are present and have a value:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `GEMINI_API_KEY`

If you have followed all of these steps and are still having issues, please provide screenshots of the **Build** and **Variables** sections for both your `client` and `server` services.
