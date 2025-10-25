#!/usr/bin/env python3
"""
Automated DNA health analysis (non-interactive).
Analyzes your 23andMe DNA file and generates health insights.
"""

import os
from pathlib import Path
from dna_parser import DNAParser
from health_snps import get_health_snps_list, get_health_snp
from variant_annotator import VariantAnnotator
from llm_interpreter import DNAInterpreter, MEDICAL_DISCLAIMER

# Load environment
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def main():
    """Main analysis workflow."""
    print("\n" + "="*70)
    print("  DNA HEALTH ANALYSIS TOOL")
    print("="*70)
    print(MEDICAL_DISCLAIMER)
    print("="*70 + "\n")

    # Use your DNA file
    dna_file = "source/genome_Sean_O_Reilly_v3_Full_20170428141907.txt"

    if not Path(dna_file).exists():
        print(f"Error: File not found: {dna_file}")
        return

    # Step 1: Parse DNA file
    print(f"Parsing DNA file: {dna_file}")
    parser = DNAParser(dna_file)
    snps = parser.parse()

    # Create lookup dict for quick access
    user_snps = {snp.rsid: snp.genotype for snp in snps}
    print(f"Successfully loaded {len(user_snps)} SNPs from your DNA file\n")

    # Step 2: Find health-related variants
    print("Analyzing health-related variants...")
    annotator = VariantAnnotator()
    health_variants = annotator.get_user_health_variants(user_snps)

    if not health_variants:
        print("No tracked health variants found in your DNA data.")
        return

    print(f"Found {len(health_variants)} health-related variants in your genome\n")

    # Step 3: Display findings
    print("="*70)
    print("YOUR HEALTH VARIANT SUMMARY")
    print("="*70 + "\n")

    for rsid, variant in sorted(health_variants.items()):
        print(f"{rsid:15} | {variant.get('gene'):12} | {variant.get('genotype'):5} | {variant.get('trait')}")

    # Step 4: Generate comprehensive health profile
    print("\n" + "="*70)
    print("COMPREHENSIVE HEALTH PROFILE")
    print("="*70 + "\n")

    interpreter = DNAInterpreter()
    print("Generating health profile analysis...\n")
    profile = interpreter.interpret_health_profile(health_variants)
    print(profile)

    # Step 5: Interactive mode
    print("\n" + "="*70)
    print("INTERACTIVE Q&A")
    print("="*70)
    print("Ask questions about your genetic variants.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Your question (or 'quit'): ").strip()

        if question.lower() in ('quit', 'exit', 'q'):
            print("\nThank you for using DNA Health Analysis Tool!")
            break

        if not question:
            continue

        print(f"\nAnalyzing...")
        response = interpreter.ask_question(question)
        print(f"\n{response}\n")
        print("-"*70)


if __name__ == "__main__":
    main()
