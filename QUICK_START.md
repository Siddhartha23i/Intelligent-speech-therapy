# Quick Start Guide - Authentication Setup

## 🚀 Quick Setup (5 Steps)

### Step 1: Install Dependencies

```bash
pip install supabase python-dotenv
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Create .env File

Create a file named `.env` in the project root directory with the following content:

```
SUPABASE_URL=your-supabase-url-here
SUPABASE_KEY=your-anon-key-here
APP_SECRET_KEY=any-random-string
```

**Replace the placeholders** with your actual Supabase credentials (see Step 3).

### Step 3: Get Supabase Credentials

1. Go to your Supabase project dashboard
2. Click **Settings** (gear icon) → **API**
3. Copy:
   - **Project URL** → Use as `SUPABASE_URL`
   - **anon/public key** → Use as `SUPABASE_KEY`

### Step 4: Set Up Database Tables

1. In Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy the entire content from `SUPABASE_SCHEMA.txt`
4. Paste and click **Run**
5. Verify tables were created in **Table Editor**

### Step 5: Run the Application

```bash
streamlit run app.py
```

## 📝 First Time Usage

1. **Sign Up**: Click "Sign Up" button
   - Enter your details
   - Choose **Administrator** for first account
   - Click "Create Account"

2. **Login**: Use your credentials to login

3. **Start Practicing**: Go to Practice page and start using the platform!

## 🔑 Account Types

- **👤 Regular User**: Can practice and view own progress
- **👨‍💼 Administrator**: Can manage users + view platformstatistics

## 🎯 Features

### For All Users:
- ✅ Secure login/signup
- ✅ Practice pronunciation
- ✅ View personal dashboard
- ✅ Track progress over time
- ✅ Get personalized feedback

### For Admins:
- ✅ View all users
- ✅ Platform statistics
- ✅ User management
- ✅ Activity monitoring

## 🛠️ Troubleshooting

### "Supabase credentials not found"
- Make sure `.env` file exists in project root
- Check that values in `.env` are correct (no quotes needed)

### "Connection refused" or "Network error"
- Verify your Supabase URL is correct
- Check your internet connection
- Ensure Supabase project is active

### "Table does not exist"
- Run the SQL schema from `SUPABASE_SCHEMA.txt`
- Check tables exist in Supabase Table Editor

### Can't login after signup
- Verify password is correct (case-sensitive)
- Check username doesn't have extra spaces
- Try creating account again with different username

## 📚 Full Documentation

For detailed setup instructions, see:
- **SUPABASE_SETUP.md** - Complete Supabase configuration guide
- **README.md** - Full project documentation

## 💡 Tips

- **Keep `.env` secure** - Never commit it to git (it's already gitignored)
- **Use strong passwords** - Especially for admin accounts
- **Regular backups** - Enable auto-backups in Supabase dashboard
- **Monitor usage** - Check Admin Dashboard regularly

## 🆘 Need Help?

If you encounter issues:
1. Check the full `SUPABASE_SETUP.md` guide
2. Verify all steps were completed
3. Check Supabase dashboard for error logs
4. Review the console output for error messages

---

**Ready to go!** 🎉 Run `streamlit run app.py` and start practicing!
