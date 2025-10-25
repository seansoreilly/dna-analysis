#!/usr/bin/env python3
"""
Test script demonstrating the full DNA analysis pipeline.
Shows DNA parsing, variant finding, and LLM interpretation.
"""

import os
from pathlib import Path
from dna_parser import DNAParser
from variant_annotator import VariantAnnotator
from llm_interpreter import DNAInterpreter, MEDICAL_DISCLAIMER

# Load environment
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def main():
    print("\n" + "="*70)
    print("  DNA HEALTH ANALYSIS - TEST PIPELINE")
    print("="*70)
    print(MEDICAL_DISCLAIMER)
    print("="*70 + "\n")

    # Step 1: Parse DNA
    print("STEP 1: Parsing DNA file...")
    dna_file = "source/genome_Sean_O_Reilly_v3_Full_20170428141907.txt"

    if not Path(dna_file).exists():
        print(f"Error: {dna_file} not found")
        return

    parser = DNAParser(dna_file)
    snps = parser.parse()
    user_snps = {snp.rsid: snp.genotype for snp in snps}

    # Step 2: Find health variants
    print("\nSTEP 2: Analyzing health variants...")
    annotator = VariantAnnotator()
    health_variants = annotator.get_user_health_variants(user_snps)

    print(f"\nFound {len(health_variants)} health variants:\n")
    for rsid in sorted(health_variants.keys())[:5]:
        variant = health_variants[rsid]
        print(f"  {rsid:15} | Gene: {variant['gene']:12} | Genotype: {variant['genotype']:5} | {variant['trait']}")

    if len(health_variants) > 5:
        print(f"  ... and {len(health_variants) - 5} more\n")

    # Step 3: LLM analysis
    print("\nSTEP 3: Generating health profile with LLM...\n")
    interpreter = DNAInterpreter()

    # Show health profile (first part)
    profile = interpreter.interpret_health_profile(health_variants)
    print(profile[:1500])
    print("\n[Full profile available in interactive mode]\n")

    # Step 4: Interactive questions
    print("="*70)
    print("STEP 4: Interactive Question Answering")
    print("="*70 + "\n")

    sample_questions = [
        "What does my APOE genotype tell me about Alzheimer's risk?",
        "Am I lactose intolerant based on my DNA?",
    ]

    for question in sample_questions:
        print(f"Q: {question}")
        response = interpreter.ask_question(question)
        print(f"A: {response[:500]}...\n")
        print("-"*70 + "\n")


if __name__ == "__main__":
    main()
