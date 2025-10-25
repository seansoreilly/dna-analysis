-- Supabase SQL Setup for DNA Analysis App
-- Run this in your Supabase dashboard: https://app.supabase.com/project/{project-id}/sql/new
--
-- This creates a table to store persistent DNA profiles with GUIDs

-- Create the dna_profiles table
CREATE TABLE IF NOT EXISTS dna_profiles (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    guid UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    user_snps JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_dna_profiles_guid ON dna_profiles(guid);
CREATE INDEX IF NOT EXISTS idx_dna_profiles_created_at ON dna_profiles(created_at);
CREATE INDEX IF NOT EXISTS idx_dna_profiles_accessed_at ON dna_profiles(accessed_at);

-- Enable RLS (Row Level Security) for privacy
ALTER TABLE dna_profiles ENABLE ROW LEVEL SECURITY;

-- Allow all users to read any DNA profile (they have a GUID)
CREATE POLICY "Allow all users to read DNA profiles by GUID" ON dna_profiles
    FOR SELECT USING (true);

-- Allow anyone to insert new DNA profiles
CREATE POLICY "Allow inserting new DNA profiles" ON dna_profiles
    FOR INSERT WITH CHECK (true);

-- Allow updating accessed_at timestamp
CREATE POLICY "Allow updating accessed_at" ON dna_profiles
    FOR UPDATE USING (true) WITH CHECK (true);

-- Optional: Create a function to clean up old profiles (older than 30 days)
-- Uncomment if you want automatic cleanup
-- CREATE OR REPLACE FUNCTION cleanup_old_dna_profiles()
-- RETURNS void AS $$
-- BEGIN
--   DELETE FROM dna_profiles
--   WHERE created_at < NOW() - INTERVAL '30 days'
--   AND accessed_at < NOW() - INTERVAL '30 days';
-- END;
-- $$ LANGUAGE plpgsql;
