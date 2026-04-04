# Railway Deployment Guide

Deploy your Online Judge on Railway with your Supabase PostgreSQL database.

## Step 1: Sign Up on Railway
1. Go to [railway.app](https://railway.app/) and sign up with **GitHub** (no credit card needed).
2. You get **$5 free trial credit** — enough for a few weeks of a small Django app.

---

## Step 2: Create a New Project
1. In the Railway dashboard, click **New Project** → **Deploy from GitHub Repo**.
2. Connect your GitHub and select `OJ_Project_AlgoUniversity`.
3. Railway will auto-detect your `Dockerfile` inside `oj_backend/`.
4. If Railway asks for the root directory, set it to `oj_backend`.

---

## Step 3: Add Environment Variables
Go to your service → **Variables** tab and add:

| Variable | Value |
|---|---|
| `DATABASE_URL` | `postgresql://postgres.kbiglqcofwenylfaesbl:YOUR_PASSWORD@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres` |
| `GEMINI_API_KEY` | Your Google API key |
| `SECRET_KEY` | Any long random string |
| `IS_PRODUCTION` | `True` |
| `PORT` | `8000` |

> Replace `YOUR_PASSWORD` with your Supabase database password.

---

## Step 4: Generate a Public URL
1. Go to your service → **Settings** tab.
2. Under **Networking**, click **Generate Domain**.
3. Railway gives you a free `*.up.railway.app` URL.

---

## Step 5: Verify
- Visit your generated URL — your Online Judge should be live!
- Migrations run automatically on every deploy (configured in Dockerfile).
- To create a superuser, use Railway's terminal: Service → **Shell** tab → `python manage.py createsuperuser`.

---

## Useful Info
- **Auto-deploy**: Pushes to GitHub automatically trigger redeploys
- **Logs**: Available in the **Deployments** tab
- **Free credit**: Monitor usage at railway.app → **Usage** tab
- **Sleep**: Railway does NOT sleep your app (unlike Render), so credit is used continuously
