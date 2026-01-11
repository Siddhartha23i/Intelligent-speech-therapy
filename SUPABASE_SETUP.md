# Supabase Setup Guide

This guide will help you set up Supabase for the AI Speech Therapy Platform.

## Prerequisites

- A Supabase account (sign up at https://supabase.com)
- Your Supabase project URL and API key

## Step 1: Create a Supabase Project

1. Go to https://supabase.com and sign in
2. Click "New Project"
3. Fill in the project details:
   - **Name**: Speech Therapy Platform
   - **Database Password**: Choose a strong password
   - **Region**: Select closest to your users
4. Click "Create new project"
5. Wait for the project to be set up (2-3 minutes)

## Step 2: Get Your Credentials

1. In your Supabase project dashboard, click on "Settings" (gear icon)
2. Navigate to "API" section
3. Copy the following:
   - **Project URL**: This is your `SUPABASE_URL`
   - **anon/public key**: This is your `SUPABASE_KEY`

## Step 3: Create Database Tables

1. In your Supabase project dashboard, click on "SQL Editor" from the left sidebar
2. Click "New Query"
3. Copy and paste the entire contents from `SUPABASE_SCHEMA.txt` file
4. Click "Run" to execute the SQL commands
5. Verify that tables were created:
   - Go to "Table Editor" from left sidebar
   - You should see: `user_profiles`, `sessions`, `phoneme_scores`, `user_weak_phonemes`

## Step 4: Configure Environment Variables

1. In your project directory, create a file named `.env`
2. Add your Supabase credentials:

```bash
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
APP_SECRET_KEY=your-random-secret-key
```

3. Replace the placeholders with your actual credentials from Step 2
4. For `APP_SECRET_KEY`, you can generate a random string (e.g., use Python):
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

## Step 5: Disable Supabase Auth (Using Custom Auth)

Since we're using custom username/password authentication:

1. Go to "Authentication" → "Providers" in Supabase dashboard
2. Disable Email provider (we're not using Supabase Auth)
3. Our custom authentication is handled via the `user_profiles` table

## Step 6: Test Database Connection

Run this command to test your Supabase connection:

```bash
python -c "from utils.supabase_client import test_connection; test_connection()"
```

You should see: `✅ Supabase connection successful!`

## Step 7: Create Your First Admin Account

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Click "Sign Up"
3. Fill in the registration form:
   - **Full Name**: Your name
   - **Username**: Choose a username
   - **Password**: Choose a strong password
   - **Account Type**: Select "Administrator"
4. Click "Create Account"
5. Login with your new credentials

## Troubleshooting

### Connection Error

If you get a connection error:
- Verify your `.env` file contains the correct credentials
- Check that your Supabase project is active
- Ensure your API key is the **anon/public** key, not the service_role key

### Table Creation Errors

If tables aren't created:
- Make sure you ran the entire `SUPABASE_SCHEMA.txt` SQL script
- Check for error messages in the SQL Editor
- Try running each section separately if needed

### Row Level Security (RLS) Issues

If you can't see data after logging in:
- Verify RLS policies were created (check in "Authentication" → "Policies")
- Ensure you're logged in with the correct user
- Check that the user_id in session_state matches the database

## Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use strong passwords** for admin accounts
3. **Rotate API keys** periodically in production
4. **Enable Supabase's built-in security features**:
   - Rate limiting
   - IP allowlisting (for production)
   - SSL enforcement

## Database Backup

To backup your data:
1. Go to "Database" → "Backups" in Supabase dashboard
2. Enable automatic backups (recommended for production)
3. You can also export data manually from "Table Editor"

## Next Steps

- Create user accounts via the signup page
- Start practicing and test the platform
- Monitor usage in the Admin Dashboard
- Check Supabase dashboard for database metrics

## Support

- Supabase Documentation: https://supabase.com/docs
- Supabase Community: https://github.com/supabase/supabase/discussions
- Project Issues: Create an issue in your repository

---

**Important**: Keep your `.env` file secure and never share your API keys publicly!
