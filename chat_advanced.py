#!/usr/bin/env python3
"""
Advanced DNA chat - Ask questions about ANY genetic trait or variant.
"""

import os
from pathlib import Path
from dna_parser import DNAParser
from variant_annotator import VariantAnnotator
from universal_interpreter import UniversalDNAInterpreter, SYSTEM_PROMPT
from llm_interpreter import MEDICAL_DISCLAIMER

# Load environment
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def print_header():
    """Print welcome header."""
    print("\n" + "="*70)
    print("  🧬 ADVANCED DNA CHAT - Ask About ANY Trait or Variant")
    print("="*70)
    print(MEDICAL_DISCLAIMER)
    print("="*70 + "\n")


def initialize_dna():
    """Load and analyze user's DNA."""
    dna_file = "source/genome_Sean_O_Reilly_v3_Full_20170428141907.txt"

    if not Path(dna_file).exists():
        print(f"\n❌ Error: DNA file not found: {dna_file}")
        return None, None

    # Parse DNA
    parser = DNAParser(dna_file)
    snps = parser.parse()
    user_snps = {snp.rsid: snp.genotype for snp in snps}

    # Find health variants
    annotator = VariantAnnotator()
    health_variants = annotator.get_user_health_variants(user_snps)

    print(f"✓ Loaded {len(user_snps):,} SNPs from your genome")
    print(f"✓ Found {len(health_variants)} tracked health variants\n")

    return user_snps, health_variants


def print_help():
    """Print help message."""
    help_text = """
ADVANCED DNA CHAT - You can ask about:

SPECIFIC VARIANTS:
  • "Tell me about rs429358"
  • "What does my APOE variant mean?"
  • "Compare rs762551 AA vs AC genotypes"
  • "What's the connection between rs7903146 and diabetes?"

TRAITS & CONDITIONS:
  • "What causes lactose intolerance?"
  • "What genes control eye color?"
  • "Which variants are associated with caffeine sensitivity?"
  • "How hereditary is Alzheimer's disease?"
  • "What determines athletic performance?"

YOUR PERSONAL GENETICS:
  • "What does my genetic profile tell me?"
  • "Which of my variants have the biggest health impact?"
  • "What lifestyle changes matter most for my genetics?"
  • "Am I at genetic risk for [condition]?"

GENETICS EDUCATION:
  • "How do dominant and recessive genes work?"
  • "What's the difference between SNPs and mutations?"
  • "How common is the APOE4 variant?"
  • "What does heritability mean?"

COMMANDS:
  'variants'    - Show your 21 tracked health variants
  'help'        - Show this help
  'lookup <rsid>' - Detailed info on a specific variant
  'trait <name>' - Genetic basis of a trait
  'reset'       - Start new conversation
  'quit'        - Exit chat
"""
    print(help_text)


def chat_loop(user_snps, health_variants):
    """Run advanced interactive chat loop."""
    interpreter = UniversalDNAInterpreter()
    interpreter.set_user_snps(user_snps)

    print("="*70)
    print("💬 ASK ANYTHING ABOUT GENETICS & YOUR DNA")
    print("="*70)
    print("Type 'help' for examples and commands\n")
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
            print("\nThank you for using Advanced DNA Chat! 🧬")
            break

        if question.lower() == 'help':
            print_help()
            continue

        if question.lower() == 'variants':
            print("\n📋 Your Health Variants:")
            print("-"*70)
            for rsid, variant in sorted(health_variants.items()):
                print(f"  {rsid:15} | {variant.get('gene'):12} | {variant.get('genotype'):5} | {variant.get('trait')}")
            print()
            continue

        if question.lower() == 'reset':
            interpreter.reset_conversation()
            print("\n✓ Conversation reset. Starting fresh.\n")
            continue

        # Handle lookup commands
        if question.lower().startswith('lookup '):
            rsid = question.replace('lookup ', '').strip().upper()
            if not rsid.startswith('RS'):
                rsid = 'rs' + rsid if not rsid.startswith('rs') else rsid
            print(f"\n📚 Looking up {rsid}...\n")
            try:
                response = interpreter.lookup_variant(rsid)
                print(f"Claude: {response}\n")
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")
            continue

        if question.lower().startswith('trait '):
            trait = question.replace('trait ', '').strip()
            print(f"\n🧬 Researching genetic basis of {trait}...\n")
            try:
                response = interpreter.lookup_trait(trait)
                print(f"Claude: {response}\n")
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")
            continue

        # Regular question
        print("\nClaude: ", end="", flush=True)
        try:
            response = interpreter.ask(question)
            print(response)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again.\n")

        print()


def main():
    """Main chat application."""
    print_header()

    # Initialize DNA analysis
    user_snps, health_variants = initialize_dna()

    if not health_variants:
        return

    # Start advanced chat loop
    chat_loop(user_snps, health_variants)


if __name__ == "__main__":
    main()
