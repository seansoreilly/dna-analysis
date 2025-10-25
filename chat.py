#!/usr/bin/env python3
"""
Interactive DNA chat interface.
Ask questions about your genetic variants in a conversational format.
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


def print_header():
    """Print welcome header."""
    print("\n" + "="*70)
    print("  🧬 DNA HEALTH CHAT")
    print("="*70)
    print(MEDICAL_DISCLAIMER)
    print("="*70)
    print("\nInitializing your DNA analysis...")


def initialize_dna():
    """Load and analyze user's DNA."""
    dna_file = "source/genome_Sean_O_Reilly_v3_Full_20170428141907.txt"

    if not Path(dna_file).exists():
        print(f"\n❌ Error: DNA file not found: {dna_file}")
        return None, None, None

    # Parse DNA
    parser = DNAParser(dna_file)
    snps = parser.parse()
    user_snps = {snp.rsid: snp.genotype for snp in snps}

    # Find health variants
    annotator = VariantAnnotator()
    health_variants = annotator.get_user_health_variants(user_snps)

    print(f"✓ Loaded {len(user_snps):,} SNPs")
    print(f"✓ Found {len(health_variants)} health variants\n")

    return user_snps, health_variants, annotator


def print_quick_reference(health_variants):
    """Print quick reference of user's variants."""
    print("="*70)
    print("YOUR HEALTH VARIANTS (Quick Reference)")
    print("="*70)
    for rsid, variant in sorted(list(health_variants.items())[:10]):
        print(f"  {rsid:15} {variant.get('gene'):12} {variant.get('genotype'):5}  {variant.get('trait')}")
    if len(health_variants) > 10:
        print(f"  ... and {len(health_variants) - 10} more variants\n")
    else:
        print()


def chat_loop(health_variants, interpreter):
    """Run interactive chat loop."""
    print("="*70)
    print("💬 ASK ANYTHING ABOUT YOUR DNA")
    print("="*70)
    print("Examples:")
    print("  • What does my APOE variant mean?")
    print("  • Am I at risk for cardiovascular disease?")
    print("  • What about my caffeine metabolism?")
    print("  • How do I interpret my results?")
    print("  • What lifestyle changes should I make?")
    print("\nCommands:")
    print("  'variants'  - Show all your health variants")
    print("  'help'      - Show this help message")
    print("  'quit'      - Exit chat\n")
    print("-"*70 + "\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting chat. Thank you!")
            break

        if not question:
            continue

        # Handle commands
        if question.lower() == 'quit':
            print("\nThank you for using DNA Health Chat! 🧬")
            break

        if question.lower() == 'help':
            print("\nAvailable commands:")
            print("  'variants'  - Show all your health variants")
            print("  'help'      - Show this help message")
            print("  'quit'      - Exit chat\n")
            continue

        if question.lower() == 'variants':
            print("\nYour Health Variants:")
            print("-"*70)
            for rsid, variant in sorted(health_variants.items()):
                print(f"  {rsid:15} | {variant.get('gene'):12} | {variant.get('genotype'):5} | {variant.get('trait')}")
            print()
            continue

        # Ask Claude about DNA
        print("\nClaude: ", end="", flush=True)
        try:
            response = interpreter.ask_question(question)
            print(response)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again.\n")

        print()


def main():
    """Main chat application."""
    print_header()

    # Initialize DNA analysis
    user_snps, health_variants, annotator = initialize_dna()

    if not health_variants:
        return

    # Show quick reference
    print_quick_reference(health_variants)

    # Initialize LLM interpreter
    interpreter = DNAInterpreter()

    # Start chat loop
    chat_loop(health_variants, interpreter)


if __name__ == "__main__":
    main()
