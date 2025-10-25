#!/usr/bin/env python3
"""
Main DNA health analysis tool.
Parses DNA file, finds health-related variants, and provides AI-powered insights.
"""

import sys
from pathlib import Path
from dna_parser import DNAParser
from health_snps import get_health_snps_list, get_health_snp
from variant_annotator import VariantAnnotator
from llm_interpreter import DNAInterpreter, MEDICAL_DISCLAIMER


def main():
    """Main analysis workflow."""
    print("\n" + "="*70)
    print("  DNA HEALTH ANALYSIS TOOL")
    print("="*70)
    print(MEDICAL_DISCLAIMER)
    print("="*70 + "\n")

    # Step 1: Get DNA file from user
    dna_file = input("Enter path to your 23andMe/Ancestry DNA file: ").strip()

    if not Path(dna_file).exists():
        print(f"Error: File not found: {dna_file}")
        sys.exit(1)

    # Step 2: Parse DNA file
    print(f"\nParsing DNA file...")
    parser = DNAParser(dna_file)
    snps = parser.parse()

    # Create lookup dict for quick access
    user_snps = {snp.rsid: snp.genotype for snp in snps}
    print(f"Successfully loaded {len(user_snps)} SNPs from your DNA file\n")

    # Step 3: Find health-related variants
    print("Analyzing health-related variants...")
    annotator = VariantAnnotator()
    health_variants = annotator.get_user_health_variants(user_snps)

    if not health_variants:
        print("No tracked health variants found in your DNA data.")
        sys.exit(0)

    print(f"Found {len(health_variants)} health-related variants in your genome\n")

    # Step 4: Display findings and get user input
    print("="*70)
    print("YOUR HEALTH VARIANT SUMMARY")
    print("="*70)

    for rsid, variant in sorted(health_variants.items())[:10]:  # Show first 10
        print(f"\n{rsid} ({variant.get('gene')})")
        print(f"  Trait: {variant.get('trait')}")
        print(f"  Your genotype: {variant.get('genotype')}")

    if len(health_variants) > 10:
        print(f"\n... and {len(health_variants) - 10} more variants\n")

    print("\n" + "="*70)
    print("INTERACTIVE ANALYSIS")
    print("="*70)
    print("Ask questions about your DNA analysis below.")
    print("Type 'quit' to exit.\n")

    # Step 5: Interactive conversation with LLM
    interpreter = DNAInterpreter()

    # Start with health profile synthesis
    print("Generating comprehensive health profile...\n")
    profile = interpreter.interpret_health_profile(health_variants)
    print(profile)

    # Interactive questions
    print("\n" + "-"*70)
    print("Ask me anything about your genetic variants:")
    print("-"*70 + "\n")

    while True:
        question = input("Your question: ").strip()

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
