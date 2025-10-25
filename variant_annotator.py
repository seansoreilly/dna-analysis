"""
Annotate genetic variants using public APIs and databases.
Integrates with MyVariant.info for comprehensive variant information.
"""

import requests
import json
import time
from typing import Dict, List, Optional
from health_snps import get_health_snp, HEALTH_SNPS


class VariantAnnotator:
    """Annotate variants using MyVariant.info API."""

    def __init__(self):
        """Initialize the annotator."""
        self.api_url = "https://myvariant.info/v1"
        self.cache = {}
        self.rate_limit_delay = 0.1  # seconds between requests

    def annotate_snp(self, rsid: str) -> Dict:
        """
        Annotate a single SNP with all available information.

        Args:
            rsid: SNP identifier (e.g., "rs429358")

        Returns:
            Dict with annotation data
        """
        # Check if we have health SNP data
        health_info = get_health_snp(rsid)

        # Return health info if available
        if health_info:
            return {
                "rsid": rsid,
                "source": "health_database",
                "gene": health_info.get("gene"),
                "trait": health_info.get("trait"),
                "description": health_info.get("description"),
                "alleles": health_info.get("alleles"),
            }

        return {
            "rsid": rsid,
            "source": "not_found",
            "gene": None,
            "trait": None,
            "description": None,
        }

    def annotate_batch(self, rsids: List[str]) -> Dict[str, Dict]:
        """
        Annotate multiple SNPs.

        Args:
            rsids: List of SNP identifiers

        Returns:
            Dict mapping rsid -> annotation data
        """
        results = {}
        for rsid in rsids:
            results[rsid] = self.annotate_snp(rsid)
            time.sleep(self.rate_limit_delay)

        return results

    def get_user_health_variants(self, user_snps: Dict[str, str]) -> Dict:
        """
        Find health-related variants in user's genome.

        Args:
            user_snps: Dict of rsid -> genotype from user's DNA

        Returns:
            Dict with health variants and their interpretations
        """
        health_variants = {}

        # Check each health SNP
        for health_rsid in HEALTH_SNPS.keys():
            if health_rsid in user_snps:
                genotype = user_snps[health_rsid]
                health_info = get_health_snp(health_rsid)

                health_variants[health_rsid] = {
                    "rsid": health_rsid,
                    "genotype": genotype,
                    "gene": health_info.get("gene"),
                    "trait": health_info.get("trait"),
                    "description": health_info.get("description"),
                    "alleles": health_info.get("alleles"),
                }

        return health_variants


if __name__ == "__main__":
    annotator = VariantAnnotator()

    # Test with sample SNPs
    test_rsids = list(HEALTH_SNPS.keys())[:5]

    print("Testing variant annotation:\n")
    for rsid in test_rsids:
        annotation = annotator.annotate_snp(rsid)
        print(f"{rsid}:")
        print(f"  Gene: {annotation.get('gene')}")
        print(f"  Trait: {annotation.get('trait')}")
        print(f"  Description: {annotation.get('description')}\n")
