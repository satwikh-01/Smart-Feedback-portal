# The Only Railway Deployment Guide You Need

The code in this repository is correct. The deployment is failing for one reason only: the **Root Directory** for your services is not set correctly in the Railway dashboard.

Follow these exact steps.

---

### **Step 1: Delete Existing Services**

-   Go to your Railway project.
-   Go to the **Settings** tab for both your `client` and `server` services and delete them. This ensures a clean start.

---

### **Step 2: Create the `server` Service**

1.  In your Railway project, click **"+ New"** and select **"GitHub Repo"**.
2.  Choose your repository. When prompted, select **"Add a new service"**.
3.  Name this service **`server`**.
4.  Go to the new `server` service's **Settings** tab.
5.  Find the **Build** section.
6.  In the **Root Directory** field, type exactly this: `./server`
7.  Click **"Save"**.

    ```
    ┌───────────────────────────────────┐
    │ ⚙️ Settings                       │
    │ ┌───────────────────────────────┐ │
    │ │ Build                         │ │
    │ │ Root Directory   [ ./server ] │ │  <--- TYPE THIS EXACTLY
    │ └───────────────────────────────┘ │
    └───────────────────────────────────┘
    ```

---

### **Step 3: Create the `client` Service**

1.  Go back to your project dashboard.
2.  Click **"+ New"** again and select your repository.
3.  Select **"Add a new service"**.
4.  Name this service **`client`**.
5.  Go to the new `client` service's **Settings** tab.
6.  Find the **Build** section.
7.  In the **Root Directory** field, type exactly this: `./client`
8.  Click **"Save"**.

---

### **Step 4: Add Environment Variables**

1.  **For the `server` service:**
    -   Go to its **Variables** tab and add all the required secrets (`SUPABASE_URL`, `SECRET_KEY`, etc.).

2.  **For the `client` service:**
    -   First, wait for the `server` service to deploy successfully.
    -   Go to the `server` service's **Settings** tab.
    -   Under the **Networking** section, you will see **"Public Networking"**. Click **"Generate Domain"**.
    -   Copy the URL that appears.
    -   Now, go to the `client` service's **Variables** tab.
    -   Create a new variable `NEXT_PUBLIC_API_URL` and paste the server's public URL as the value.

---

The build will now succeed because Railway will look inside the correct directories and find the `Dockerfile`s waiting for it.
