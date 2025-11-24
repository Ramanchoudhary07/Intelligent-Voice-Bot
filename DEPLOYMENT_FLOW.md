# Deployment Flow for Render

This guide outlines the steps to deploy the Intelligent Voice Bot backend to Render.

## Prerequisites

1.  **Render Account**: Create an account at [render.com](https://render.com).
2.  **GitHub Repository**: Ensure this code is pushed to a GitHub repository.
3.  **API Keys**: You will need the following API keys:
    *   `GEMINI_API_KEY` (Google Gemini)
    *   `AWS_ACCESS_KEY_ID` (Amazon Polly)
    *   `AWS_SECRET_ACCESS_KEY` (Amazon Polly)

## Deployment Steps

### 1. Connect to Render

1.  Log in to your Render dashboard.
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub account if you haven't already.
4.  Select the repository containing this code.

### 2. Configure the Blueprint

Render will automatically detect the `render.yaml` file in the root directory.

**IMPORTANT:** Ensure you are creating a **Blueprint** (Infrastructure as Code) and not just a "Web Service". If you create a "Web Service" manually, Render might default to the **Python** runtime, which will fail because it cannot install system dependencies like FFmpeg.

**If you must create a Web Service manually:**
*   Select **Docker** as the Runtime/Environment.
*   Do **NOT** select "Python".

1.  **Service Name**: `intelligent-voice-bot-api` (defined in `render.yaml`).
2.  **Region**: Oregon (defined in `render.yaml`, change if needed).
3.  **Environment Variables**:
    Render will ask you to provide values for the environment variables marked as `sync: false` in `render.yaml`.
    *   `GEMINI_API_KEY`: Paste your Google Gemini API key.
    *   `AWS_ACCESS_KEY_ID`: Paste your AWS Access Key ID.
    *   `AWS_SECRET_ACCESS_KEY`: Paste your AWS Secret Access Key.

    *Note: `DATABASE_URL` and `DATABASE_TYPE` are automatically configured by the Blueprint.*

### 3. Deploy

1.  Click **Apply** or **Create Resources**.
2.  Render will:
    *   Provision a PostgreSQL database (`voice-bot-db`).
    *   Build the Docker image using the `Dockerfile`.
    *   Deploy the web service.

### 4. Verify Deployment

1.  Once the deployment is live, Render will provide a URL (e.g., `https://intelligent-voice-bot-api.onrender.com`).
2.  Visit the URL in your browser. You should see the dashboard or a 404 (since the root route `/` renders `index.html` which might expect frontend assets).
3.  Test the API:
    *   Endpoint: `/api/analytics` (Requires JWT, so might be hard to test directly in browser without login).
    *   Check the **Logs** tab in Render dashboard to ensure the server started correctly and connected to the database.

## Post-Deployment

### Database Initialization
The application is designed to initialize the database tables automatically on the first connection. However, you can also run the initialization script manually if needed via the Render Shell (SSH):
```bash
python init_db.py
```

### Frontend Connection
If you are deploying the frontend separately (e.g., on Vercel):
1.  Update your frontend's API URL configuration to point to your new Render backend URL.
2.  Re-deploy the frontend.
