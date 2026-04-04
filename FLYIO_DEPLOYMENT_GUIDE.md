# Fly.io Deployment Guide with PostgreSQL

Your repository is now configured for Fly.io deployment. Follow these steps to get your Online Judge live!

## Prerequisites
- A [Fly.io](https://fly.io/) account (free tier available, but requires a credit card for verification)
- The `flyctl` CLI installed on your machine

### Install flyctl
```powershell
# Windows (PowerShell)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```
After installation, log in:
```powershell
flyctl auth login
```

---

## Step 1: Create the App on Fly.io
From the `oj_backend` directory (where `fly.toml` lives):
```powershell
flyctl launch --no-deploy
```
- When asked if you want to copy the existing config, say **Yes**.
- Choose a unique app name (or accept the default).
- Select a region close to you (the config defaults to `sin` — Singapore).
- Say **No** to setting up a PostgreSQL database through Fly (we'll use Supabase instead).

---

## Step 2: Set Your Environment Variables (Secrets)
You already have your Supabase `DATABASE_URL`. Now set it as a Fly.io secret along with your other keys:

```powershell
flyctl secrets set DATABASE_URL="postgresql://postgres.kbiglqcofwenylfaesbl:YOUR_PASSWORD@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"
flyctl secrets set GEMINI_API_KEY="your-gemini-api-key-here"
flyctl secrets set SECRET_KEY="generate-a-strong-random-string-here"
```
> **Note**: Replace `YOUR_PASSWORD` with your actual Supabase database password.

---

## Step 3: Deploy!
```powershell
flyctl deploy
```
This will build your Docker image remotely on Fly.io's servers and deploy it. Wait for it to finish — it may take 3-5 minutes on the first deploy.

---

## Step 4: Run Migrations
Once the deploy is complete, open a remote console into your running app:
```powershell
flyctl ssh console
```
Then inside the console, run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Step 5: Open Your App!
```powershell
flyctl open
```
This opens your live app in the browser at `https://your-app-name.fly.dev` 🎉

---

## Useful Commands
| Command | Description |
|---|---|
| `flyctl status` | Check app status |
| `flyctl logs` | View live logs |
| `flyctl ssh console` | SSH into the running container |
| `flyctl secrets list` | List all configured secrets |
| `flyctl deploy` | Redeploy after code changes |
