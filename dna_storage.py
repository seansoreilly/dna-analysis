"""
Persistent DNA storage using Supabase
Allows users to get a shareable GUID-based URL for their DNA data
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class DNAStorage:
    """Handles persistent DNA storage using Supabase."""

    def __init__(self):
        """Initialize Supabase client."""
        if not SUPABASE_AVAILABLE:
            self.client = None
            return

        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if self.url and self.key:
            self.client = create_client(self.url, self.key)
        else:
            self.client = None

    def is_available(self) -> bool:
        """Check if Supabase is configured."""
        return self.client is not None

    def save_dna(self, user_snps: Dict[str, str], health_snps: Dict) -> Optional[str]:
        """
        Save DNA data to Supabase and return GUID.

        Args:
            user_snps: Dict of {rsid: genotype}
            health_snps: Dict of health SNP information

        Returns:
            GUID string if successful, None if failed
        """
        if not self.is_available():
            return None

        try:
            # Generate GUID
            guid = str(uuid.uuid4())

            # Prepare data
            dna_data = {
                "guid": guid,
                "user_snps": json.dumps(user_snps),
                "created_at": datetime.utcnow().isoformat(),
                "accessed_at": datetime.utcnow().isoformat(),
            }

            # Store in Supabase
            result = self.client.table("dna_profiles").insert(dna_data).execute()

            if result.data:
                return guid
            return None

        except Exception as e:
            print(f"Error saving DNA: {str(e)}")
            return None

    def load_dna(self, guid: str) -> Optional[Dict[str, str]]:
        """
        Load DNA data from Supabase by GUID.

        Args:
            guid: The GUID to load

        Returns:
            Dict of {rsid: genotype} if found, None if not
        """
        if not self.is_available():
            return None

        try:
            result = (
                self.client.table("dna_profiles")
                .select("user_snps, accessed_at")
                .eq("guid", guid)
                .execute()
            )

            if result.data and len(result.data) > 0:
                # Update accessed_at timestamp
                self.client.table("dna_profiles").update(
                    {"accessed_at": datetime.utcnow().isoformat()}
                ).eq("guid", guid).execute()

                # Parse and return DNA data
                user_snps = json.loads(result.data[0]["user_snps"])
                return user_snps

            return None

        except Exception as e:
            print(f"Error loading DNA: {str(e)}")
            return None

    def get_dna_url(self, guid: str, base_url: str = None) -> str:
        """
        Get the URL for accessing DNA by GUID.

        Args:
            guid: The GUID
            base_url: Base URL (if None, uses default)

        Returns:
            Full URL string
        """
        if base_url is None:
            base_url = "https://dna-analysis-do6hppy26tunpqdb2ezcdp.streamlit.app"

        return f"{base_url}?dna_guid={guid}"
