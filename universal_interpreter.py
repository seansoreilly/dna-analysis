"""
Universal DNA interpreter - answer questions about ANY genetic variant or trait.
Uses Claude to research and explain genetics dynamically.
"""

import json
from typing import Dict, Optional
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

SYSTEM_PROMPT = """You are an expert genetics educator and DNA analyst. Your role is to answer questions about:
- Specific genetic variants (SNPs) and their effects
- Genetic traits and what genes control them
- Whether someone might carry certain variants
- How to interpret genetic test results
- The relationship between genes and health/traits
- What genes are involved in specific conditions

IMPORTANT GUIDELINES:
1. Always include a medical disclaimer when discussing health implications
2. Distinguish between:
   - Well-established findings (strong scientific consensus)
   - Probable findings (supported by multiple studies)
   - Preliminary findings (early research)
3. Use probability language: "associated with", "may increase risk", "likely"
4. Explain what alleles mean and how dominant/recessive works
5. Be clear about limitations: "genetics is only one factor"
6. Suggest consulting healthcare providers for clinical interpretation
7. Reference specific genes, SNPs, and studies when possible
8. Explain the difference between having a variant and developing a disease/trait

DO NOT:
- Make definitive medical diagnoses
- Recommend specific treatments
- Make absolute predictions about health outcomes
- Discuss genetic testing where clinical validation is required

When asked about a specific variant:
1. Explain what gene it's in and what that gene does
2. Explain the alleles and their effects
3. Describe what it means for different genotypes (homozygous/heterozygous)
4. Discuss population frequency
5. Mention associated health/trait implications with evidence strength
6. Note lifestyle factors that interact with this gene

When asked about a trait or condition:
1. Explain the genetic basis (if known)
2. List key genes involved
3. Discuss heritability (what % is genetic vs environmental)
4. Explain how to find out if someone might carry relevant variants
5. Discuss preventable vs non-preventable aspects
"""

class UniversalDNAInterpreter:
    """Answer questions about any aspect of genetics and DNA."""

    def __init__(self):
        """Initialize the interpreter."""
        self.client = Anthropic()
        self.conversation_history = []
        self.user_snps = {}  # Store user's SNP data if provided

    def set_user_snps(self, snps: Dict[str, str]):
        """
        Set user's SNP data for personalized answers.

        Args:
            snps: Dictionary of rsid -> genotype from user's DNA
        """
        self.user_snps = snps
        print(f"✓ Loaded {len(snps):,} of your SNPs for personalized analysis")

    def ask(self, question: str) -> str:
        """
        Ask a question about genetics, traits, or specific variants.

        Args:
            question: User's question about DNA/genetics

        Returns:
            Expert explanation from Claude
        """
        # Add context about user's SNPs if asking about specific variants
        full_question = question

        # Check if question is about a specific variant and we have that data
        for rsid in self.user_snps.keys():
            if rsid.lower() in question.lower():
                genotype = self.user_snps[rsid]
                full_question += f"\n\n[User's genotype at {rsid}: {genotype}]"
                break

        self.conversation_history.append({
            "role": "user",
            "content": full_question
        })

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=self.conversation_history
        )

        answer = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    def lookup_variant(self, rsid: str) -> str:
        """
        Look up information about a specific variant.

        Args:
            rsid: SNP identifier (e.g., "rs429358")

        Returns:
            Information about the variant
        """
        question = f"""Tell me about the genetic variant {rsid}:
1. What gene is it in?
2. What does that gene do?
3. What are the alleles and what do they mean?
4. What health/trait implications does this variant have?
5. How common is this variant in the population?"""

        if rsid in self.user_snps:
            question += f"\n\nI have the {self.user_snps[rsid]} genotype at this variant. What does this mean for me?"

        return self.ask(question)

    def lookup_trait(self, trait: str) -> str:
        """
        Look up genetic basis of a trait or condition.

        Args:
            trait: Health condition or trait (e.g., "lactose intolerance", "red hair")

        Returns:
            Explanation of genetic basis
        """
        question = f"""Explain the genetics of {trait}:
1. What genes are involved?
2. What's the heritability (% genetic vs environmental)?
3. What are the main genetic variants?
4. How can someone find out if they might have a genetic predisposition?
5. What lifestyle factors interact with these genes?"""

        return self.ask(question)

    def find_variants_for_trait(self, trait: str) -> str:
        """
        Find what variants might be associated with a trait.

        Args:
            trait: Health trait or condition

        Returns:
            List of relevant variants and their effects
        """
        question = f"""What specific SNPs (genetic variants) are associated with {trait}?
1. List the main variants studied
2. For each, explain the alleles and their effects
3. Give the rsIDs if known
4. Discuss which are well-established vs preliminary
5. How would someone check if they carry these variants?"""

        return self.ask(question)

    def compare_genotypes(self, rsid: str, genotype1: str, genotype2: str) -> str:
        """
        Compare what two different genotypes mean.

        Args:
            rsid: Variant identifier
            genotype1: First genotype (e.g., "AA")
            genotype2: Second genotype (e.g., "TT")

        Returns:
            Comparison of the effects
        """
        question = f"""Compare these two genotypes at {rsid}:
- {genotype1} vs {genotype2}

Explain:
1. What does each genotype mean?
2. How do they differ in their effects?
3. What are the health/trait implications of each?
4. How common is each genotype?"""

        return self.ask(question)

    def personalized_summary(self, health_variants: Dict[str, Dict]) -> str:
        """
        Generate personalized genetic summary for user's variants.

        Args:
            health_variants: Dictionary of rsid -> variant info from user's DNA

        Returns:
            Personalized genetic summary and recommendations
        """
        # Format variants for Claude
        variants_text = "Your genetic variants:\n"
        for rsid, data in health_variants.items():
            variants_text += f"- {rsid} ({data.get('gene')}): {data.get('genotype')} - {data.get('trait')}\n"

        question = f"""{variants_text}

Based on my genetics, provide:
1. Overall genetic profile summary
2. Key health strengths based on my genotypes
3. Areas where I have increased genetic risk
4. Most impactful lifestyle changes I can make
5. Which variants are well-established vs preliminary findings
6. Genes/traits you'd recommend I learn more about"""

        return self.ask(question)

    def reset_conversation(self):
        """Reset conversation history for new topic."""
        self.conversation_history = []


if __name__ == "__main__":
    interpreter = UniversalDNAInterpreter()

    # Test examples
    print("Testing universal DNA interpreter:\n")

    print("1. Lookup a specific variant:")
    print("-" * 70)
    result = interpreter.lookup_variant("rs762551")
    print(result[:500] + "...\n")

    print("2. Lookup a trait:")
    print("-" * 70)
    interpreter.reset_conversation()
    result = interpreter.lookup_trait("red hair")
    print(result[:500] + "...\n")
