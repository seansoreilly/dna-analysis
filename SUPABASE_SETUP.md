# Supabase Setup Guide

Enable persistent DNA storage so users don't have to reload their DNA files!

## Step 1: Get Your Supabase Credentials

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Open your project (`melbournecomputing`)
3. Go to **Settings** → **API**
4. Copy:
   - `Project URL` (SUPABASE_URL)
   - `anon public` key (SUPABASE_KEY)

## Step 2: Create the Database Table

1. In Supabase, go to **SQL Editor**
2. Click **+ New Query**
3. Copy the entire contents of `DATABASE_SETUP.sql`
4. Paste into the SQL editor
5. Click **Run**

This creates the `dna_profiles` table with RLS (Row Level Security) policies.

## Step 3: Add Environment Variables

Update your `.env` file with:

```
ANTHROPIC_API_KEY=your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key-here
```

## Step 4: Set Secrets in Streamlit Cloud

In your Streamlit Cloud app settings:

1. Click **⋮** → **Settings** → **Secrets**
2. Add:
   ```
   ANTHROPIC_API_KEY = "your-key"
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-anon-public-key"
   ```

## Step 5: Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

# Upload a DNA file and you should get a persistent URL!
```

## How It Works

### When a user uploads DNA:

1. App parses the DNA file (939K+ SNPs locally - privacy first)
2. Stores user_snps in Supabase with a unique GUID
3. Returns a persistent URL: `https://.../?dna_guid={GUID}`
4. User can share this URL

### When someone visits the GUID URL:

1. App detects GUID in URL parameter
2. Loads DNA data from Supabase
3. No need to re-upload!
4. Personalized health analysis available immediately

## Database Schema

```
dna_profiles table:
├── id (bigint, primary key)
├── guid (uuid, unique) - The shareable identifier
├── user_snps (jsonb) - All 939K+ SNPs in JSON format
├── created_at (timestamp)
├── accessed_at (timestamp)
└── created_by (text, optional)
```

## Security & Privacy

✅ Row Level Security (RLS) enabled
✅ All users can read any profile (they have the GUID, it's the "password")
✅ DNA data never leaves your Supabase
✅ Only DNA phenotypes sent to Claude
✅ Optionally set up auto-cleanup of old profiles (see DATABASE_SETUP.sql)

## Troubleshooting

### "Supabase is not available"

- Check SUPABASE_URL and SUPABASE_KEY are set
- Verify they're in `.env` (local) or Secrets (Streamlit Cloud)
- Check Supabase project is active

### "Error loading DNA"

- Make sure DATABASE_SETUP.sql was run
- Check table exists: Supabase → Table Editor → dna_profiles
- Verify RLS policies are enabled

### "GUID link not showing"

- Make sure Supabase credentials are configured
- Check Streamlit Cloud logs for errors
- Verify supabase library installed: `pip install supabase`

## Optional: Auto-Cleanup Old Data

Uncomment the cleanup function in DATABASE_SETUP.sql to automatically delete profiles older than 30 days. Run it via:

```sql
SELECT cleanup_old_dna_profiles();
```

Or set up a cron job in Supabase to run it daily.

---

**Questions?** Check your Supabase dashboard or the app logs in Streamlit Cloud.
