# Render Deployment Guide with PostgreSQL

Congratulations! Your repository is now set up to be deployed on Render using a robust PostgreSQL database. Follow these instructions step-by-step.

## Step 1: Create a PostgreSQL Database
Because Render's free tier has ephemeral disk storage, any state inside `db.sqlite3` will wipe when the instance sleeps. We will use a free managed Postgres database.

1. Go to [Neon.tech](https://neon.tech/) or [Supabase](https://supabase.com/) and create a free account.
2. Spin up a new database in their free tier.
3. Find your **Connection String (URI)**. It should look something like:
   `postgresql://username:password@hostname/dbname?sslmode=require`
4. Copy this string; you'll need it later.

---

## Step 2: Deploy to Render
We have added a `render.yaml` configuration file to your repository which tells Render exactly how to build and host your Django app using Docker.

1. Create an account on [Render.com](https://render.com/).
2. Push the latest code to your GitHub repository (including `render.yaml` and our changes to `settings.py` and `requirements.txt`).
3. Inside the Render Dashboard, click **New +** and select **Blueprint**.
4. Connect your GitHub account and select your `OJ_Project_AlgoUniversity` repository.
5. Render will automatically detect the `render.yaml` blueprint. Click **Apply**.
6. Wait for the Service to appear on your dashboard. When prompted for environment variables, enter them.

---

## Step 3: Add the Database URL in Render
1. Navigate to your new Web Service on Render.
2. Go to the **Environment** tab on the left-side menu.
3. Find the field named `DATABASE_URL` (it will be empty because we left `sync: false` in `render.yaml`).
4. Paste the connection string you got from Neon / Supabase in Step 1.
5. Ensure your `GEMINI_API_KEY` is also set correctly in the environment variables.
6. Click **Save Changes**. This will trigger a re-deploy of your app.

---

## Step 4: Run Migrations
When deploying with Render + Docker, our database is entirely empty initially! You need to populate the tables.

Wait for the deployment to finish successfully.
Render provides a "Shell" tab. Go to your Web Service -> **Shell** and run:
```bash
python manage.py migrate
python manage.py createsuperuser
```
Done! Your Online Judge is now live on Render with a persistent PostgreSQL database!
