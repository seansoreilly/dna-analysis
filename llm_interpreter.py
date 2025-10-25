"""
Use Claude API to interpret genetic variants in plain English.
Provides personalized health insights without medical claims.
"""

import json
import os
from typing import Dict, List, Optional
from anthropic import Anthropic

MEDICAL_DISCLAIMER = """
⚠️ IMPORTANT DISCLAIMER:
This analysis is for educational and informational purposes only.
It is NOT medical advice, a diagnosis, or treatment recommendation.
Always consult with a healthcare provider or genetic counselor before making health decisions based on genetic information.
"""


class DNAInterpreter:
    """Use Claude to interpret DNA analysis results."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the interpreter."""
        self.client = Anthropic()
        self.conversation_history = []

    def system_prompt(self) -> str:
        """Get the system prompt for genetic interpretation."""
        return """You are a helpful genetics education assistant. Your role is to explain genetic variants and
their potential health implications in plain, accessible language.

Guidelines:
1. Always include the medical disclaimer when discussing health implications
2. Use probability language ("associated with", "may increase risk") rather than definitive statements
3. Explain what each allele/genotype means clearly
4. Mention that some findings are well-established while others are still being researched
5. Suggest consulting healthcare providers for clinical interpretation
6. Be accurate but avoid being alarming - present information objectively
7. When uncertain, say so clearly
8. Distinguish between:
   - Well-established findings (strong scientific consensus)
   - Probable findings (multiple studies support but not definitive)
   - Potential findings (preliminary evidence)

Do NOT:
- Provide medical diagnoses
- Recommend specific treatments
- Make absolute predictions about health outcomes
- Discuss genetic testing for conditions where clinical testing is required
"""

    def interpret_variant(self, variant_data: Dict) -> str:
        """
        Get AI interpretation of a single variant.

        Args:
            variant_data: Dict with variant info (rsid, genotype, gene, trait, description)

        Returns:
            Plain English interpretation
        """
        rsid = variant_data.get("rsid", "Unknown")
        genotype = variant_data.get("genotype", "")
        gene = variant_data.get("gene", "Unknown")
        trait = variant_data.get("trait", "Unknown")
        description = variant_data.get("description", "")
        alleles = variant_data.get("alleles", {})

        prompt = f"""Please explain this genetic variant to me in simple, clear language:

SNP: {rsid}
Gene: {gene}
Trait/Effect: {trait}
My genotype: {genotype}
Allele meanings: {json.dumps(alleles) if alleles else 'Not specified'}
Scientific description: {description}

Please explain:
1. What this variant does
2. What my specific genotype means for me
3. Any lifestyle considerations (if applicable)
4. How well-established this finding is"""

        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=self.system_prompt(),
            messages=self.conversation_history
        )

        interpretation = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": interpretation
        })

        return interpretation

    def interpret_health_profile(self, health_variants: Dict[str, Dict]) -> str:
        """
        Get AI synthesis of multiple health variants.

        Args:
            health_variants: Dict of rsid -> variant_data

        Returns:
            Synthesized health profile explanation
        """
        variants_text = ""
        for rsid, data in health_variants.items():
            variants_text += f"\n- {rsid} ({data.get('gene')}): {data.get('trait')} - Genotype: {data.get('genotype')}"

        prompt = f"""I've analyzed my genetic variants and found these health-related SNPs:
{variants_text}

Please provide:
1. A summary of what these variants tell me about my health predispositions
2. Areas where I should consider lifestyle changes (nutrition, exercise, etc)
3. Which findings are well-established vs. preliminary
4. Recommendations for follow-up with healthcare providers

Remember to include appropriate disclaimers."""

        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            system=self.system_prompt(),
            messages=self.conversation_history
        )

        synthesis = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": synthesis
        })

        return synthesis

    def ask_question(self, question: str) -> str:
        """
        Ask a follow-up question about genetics/variants.

        Args:
            question: User's question

        Returns:
            AI's response
        """
        self.conversation_history.append({
            "role": "user",
            "content": question
        })

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=self.system_prompt(),
            messages=self.conversation_history
        )

        answer = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    def reset_conversation(self):
        """Reset conversation history for a new analysis."""
        self.conversation_history = []


if __name__ == "__main__":
    import json

    print(MEDICAL_DISCLAIMER)
    print("\n" + "="*60 + "\n")

    # Test the interpreter
    interpreter = DNAInterpreter()

    # Sample variant
    test_variant = {
        "rsid": "rs762551",
        "genotype": "AA",
        "gene": "CYP1A2",
        "trait": "Caffeine sensitivity",
        "description": "Fast metabolizers (AA) clear caffeine quickly. Slow metabolizers (CC) retain caffeine longer",
        "alleles": {"A": "fast metabolizer", "C": "slow metabolizer"}
    }

    print("Interpreting variant rs762551...\n")
    interpretation = interpreter.interpret_variant(test_variant)
    print(interpretation)
