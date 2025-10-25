"""
Health Trait Agent - Intelligent system that understands your full DNA
and relates it to any health trait you ask about.

This agent:
- Loads your entire genome (939K+ SNPs)
- Understands major health-related variants
- When you ask about a trait, it:
  1. Identifies genes involved in that trait
  2. Checks YOUR DNA for those variants
  3. Explains your personal genetic predisposition
  4. Gives actionable recommendations
"""

from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from dna_parser import DNAParser
from health_snps import get_all_health_snps

# Load environment
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class HealthTraitAgent:
    """Intelligent agent that relates your DNA to health traits."""

    def __init__(self):
        """Initialize the agent with user's DNA."""
        import httpx
        # Create client with explicit http client configuration
        try:
            self.client = Anthropic(
                http_client=httpx.Client()
            )
        except (TypeError, AttributeError):
            # Fallback if http_client parameter doesn't work
            self.client = Anthropic()
        self.conversation_history = []
        self.user_snps = {}
        self.health_snps_db = get_all_health_snps()
        self.model = "claude-haiku-4-5-20251001"

    def load_dna(self, dna_file: str) -> bool:
        """Load user's DNA file."""
        if not Path(dna_file).exists():
            print(f"❌ DNA file not found: {dna_file}")
            return False

        print(f"Loading your DNA from {dna_file}...")
        parser = DNAParser(dna_file)
        snps = parser.parse()
        self.user_snps = {snp.rsid: snp.genotype for snp in snps}

        print(f"✓ Loaded {len(self.user_snps):,} SNPs")
        print(f"✓ Analyzing {len(self.health_snps_db)} health-related variants\n")

        return True

    def _build_system_prompt(self) -> str:
        """Build system prompt with user's DNA context."""
        # Get user's health variants
        user_health_variants = {}
        for rsid, info in self.health_snps_db.items():
            if rsid in self.user_snps:
                user_health_variants[rsid] = {
                    "genotype": self.user_snps[rsid],
                    "gene": info.get("gene"),
                    "trait": info.get("trait"),
                    "alleles": info.get("alleles"),
                }

        # Format for prompt
        variants_text = "USER'S HEALTH VARIANTS:\n"
        for rsid, data in sorted(user_health_variants.items()):
            variants_text += f"- {rsid} ({data['gene']}): {data['genotype']} - {data['trait']}\n"

        return f"""You are a health genetics expert who understands this user's specific DNA.

{variants_text}

IMPORTANT GUIDELINES:
1. When the user asks about a health trait, you should:
   - Identify which genes and variants affect that trait
   - Check if the user carries any of those variants (listed above)
   - Explain what their specific genotypes mean
   - Relate their DNA to their personal risk/predisposition
   - Give actionable lifestyle recommendations

2. Always include medical disclaimer: "This is educational info, not medical advice"

3. Use language like:
   - "Based on your specific genotypes..."
   - "You carry the [allele] variant at [gene]..."
   - "This means for you personally..."

4. Distinguish between:
   - Well-established findings (strong evidence)
   - Probable findings (supported by research)
   - Preliminary findings (early research)

5. Always explain what genes/variants affect the trait and whether the user has them

6. DO NOT make medical diagnoses - explain genetic predisposition only

7. For traits not in the database, explain the genetic basis generally, then note what variants the user has that might be relevant

When answering about health traits, ALWAYS:
- Reference the user's actual genotypes
- Explain how their specific variants affect their risk
- Connect their DNA to the trait they're asking about
- Provide science-based, not fear-based, information
"""

    def ask_about_trait(self, question: str) -> str:
        """
        Ask the agent about a health trait.
        Agent will check user's DNA and relate it to the trait.

        Args:
            question: User's question about a health trait

        Returns:
            Personalized analysis relating their DNA to the trait
        """
        self.conversation_history.append({
            "role": "user",
            "content": question
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self._build_system_prompt(),
            messages=self.conversation_history
        )

        answer = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    def reset_conversation(self):
        """Start a new conversation."""
        self.conversation_history = []


def main():
    """Run the health trait agent."""
    print("\n" + "="*70)
    print("  🧬 HEALTH TRAIT AGENT")
    print("  Analyze ANY health trait based on YOUR DNA")
    print("="*70 + "\n")

    # Initialize agent
    agent = HealthTraitAgent()

    # Load user's DNA
    dna_file = "source/genome_Sean_O_Reilly_v3_Full_20170428141907.txt"
    if not agent.load_dna(dna_file):
        return

    # Instructions
    print("="*70)
    print("Ask about ANY health trait - I'll explain your genetic predisposition")
    print("="*70)
    print("\nExamples:")
    print("  • Do I have increased risk for heart disease?")
    print("  • What's my genetic predisposition to type 2 diabetes?")
    print("  • How does caffeine affect me genetically?")
    print("  • What's my Alzheimer's disease risk based on my DNA?")
    print("  • Am I genetically predisposed to obesity?")
    print("  • What about my cholesterol metabolism?")
    print("\nCommands:")
    print("  'quit'   - Exit")
    print("  'reset'  - Start new conversation")
    print("  'variants' - Show your health variants\n")
    print("-"*70 + "\n")

    # Main loop
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! 🧬")
            break

        if not question:
            continue

        if question.lower() == 'quit':
            print("\nGoodbye! 🧬")
            break

        if question.lower() == 'reset':
            agent.reset_conversation()
            print("✓ Conversation reset\n")
            continue

        if question.lower() == 'variants':
            print("\n📋 Your Health Variants:")
            print("-"*70)
            for rsid, info in agent.health_snps_db.items():
                if rsid in agent.user_snps:
                    genotype = agent.user_snps[rsid]
                    print(f"  {rsid:15} | {info.get('gene'):12} | {genotype:5} | {info.get('trait')}")
            print()
            continue

        # Ask agent about the trait
        print("\nAgent: ", end="", flush=True)
        try:
            response = agent.ask_about_trait(question)
            print(response)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again.\n")

        print()


if __name__ == "__main__":
    main()
