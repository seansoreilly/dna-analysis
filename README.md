# DNA Health Analysis Tool

A privacy-first DNA analysis tool that uses LLMs to explain genetic variants and health traits in plain English.

## Features

- **Local DNA Parsing**: Parse 23andMe/Ancestry raw DNA files locally on your machine
- **Universal Genetics Q&A**: Ask questions about ANY genetic trait, variant, or health condition
- **Health Variant Detection**: Identify ~30+ well-studied health-related SNPs in your genome
- **LLM-Powered Insights**: Use Claude to get personalized explanations of your genetic traits
- **Interactive Analysis**: Ask follow-up questions about your genetics with conversation context
- **Dynamic Lookup**: Research specific SNPs or genetic traits on-the-fly
- **Privacy-First**: Your DNA data never leaves your computer

## Installation

### Requirements
- Python 3.8+
- Anthropic API key

### Setup

```bash
# Install dependencies
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Optional: Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
```

## Usage

### 🚀 Main Interface: Universal Genetics Chat

```bash
python3 chat_advanced.py
```

Ask questions about **ANY genetic trait or variant**:
```
You: What determines eye color genetically?
You: Tell me about rs429358
You: What genes control height?
You: Which variants are associated with lactose intolerance?
You: lookup rs762551
You: trait caffeine sensitivity
```

Type `help` in chat for examples and commands.

### Other Interfaces

**Limited chat (30 health variants only):**
```bash
python3 chat.py
```

**Full analysis with automatic questions:**
```bash
python3 analyze_dna_auto.py
```

**Manual file selection:**
```bash
python3 analyze_dna.py
```

## Architecture

### Components

**1. dna_parser.py** - DNA File Parser
- Parses 23andMe and Ancestry raw data files
- Extracts SNP data (rsID, chromosome, position, genotype)
- Validates and filters malformed data

**2. health_snps.py** - Health SNP Database
- Curated list of ~30 well-studied health SNPs
- Focuses on: cardiovascular health, metabolism, drug response, nutrition
- Links to scientific literature and explanations

**3. variant_annotator.py** - Variant Annotation
- Integrates with variant databases
- Maps user's SNPs to health information
- Provides detailed annotations

**4. llm_interpreter.py** - Health-Specific Interpreter
- Uses Claude API for health variant interpretation
- Explains 30 curated variants in plain English
- Provides personalized health insights
- Maintains conversation context

**5. universal_interpreter.py** - Universal Genetics Engine
- Answers questions about ANY genetic trait or variant
- Researches genetics dynamically
- Personalizes answers using user's SNP data
- Supports variant lookup, trait lookup, comparisons

**6. chat_advanced.py** - Universal Chat Interface
- Main entry point for asking any genetics question
- Commands: lookup, trait, variants, help, reset
- Conversation history for context
- No limitations on what you can ask

**7. analyze_dna.py** - Manual DNA Analysis
- Orchestrates full pipeline with file prompts
- Provides interactive interface
- Shows health variant summary

## Genetics You Can Explore

### Pre-Analyzed (30 Health Variants)
- **Cardiovascular**: Heart disease, stroke, atherosclerosis risk
- **Metabolism**: Caffeine sensitivity, lactose tolerance, obesity
- **Drugs**: Statin response, general drug metabolism
- **Neurological**: Alzheimer's disease, migraine risk
- **Vitamins**: Vitamin D metabolism
- **Other**: Bone health, athletic performance, eye color, alcohol response

### Unlimited (with Universal Chat)
Ask about **ANY genetic trait**:
- Physical traits (height, hair color, body shape)
- Metabolism (cholesterol, blood sugar, weight)
- Athletic performance (muscle type, VO2 max)
- Sensory (taste, smell, color vision)
- Sleep and circadian rhythms
- Personality traits (limited evidence)
- Disease predispositions
- And thousands of other genes and traits

## Data

All DNA processing happens locally. Only annotated variant information is sent to Claude API - never raw DNA data.

### What data goes to Claude?
- Variant annotations (gene names, traits, descriptions)
- Your genotypes for health SNPs only
- General health-related questions

### What stays local?
- Your full DNA file
- All 939,000+ SNPs from your genome
- The raw DNA data file itself

## Important Disclaimers

⚠️ **MEDICAL DISCLAIMER**:
- This tool is for educational purposes only
- It is NOT a medical diagnosis
- It is NOT a substitute for professional medical advice
- Always consult with a healthcare provider or genetic counselor before making health decisions based on genetic information
- Some findings are well-established, others are still being researched

## Example Output

```
rs762551 (CYP1A2)
  Trait: Caffeine sensitivity
  Your genotype: AC

Interpretation: Your rs762551 variant (AC genotype) suggests you have
intermediate caffeine metabolism. You likely clear caffeine faster than
CC carriers but slower than AA carriers. This means you probably tolerate
coffee reasonably well but may want to avoid caffeine in the late afternoon
to prevent sleep disruption.
```

## Files

```
dna-analysis/
├── dna_parser.py           # DNA file parsing
├── health_snps.py          # Health SNP database
├── variant_annotator.py    # Variant annotation engine
├── llm_interpreter.py      # LLM explanation engine
├── analyze_dna.py          # Main application
├── source/                 # Your DNA files (gitignored)
└── README.md               # This file
```

## Testing

```bash
# Test individual components
python3 dna_parser.py           # Test DNA parsing
python3 health_snps.py          # Test SNP database
python3 variant_annotator.py    # Test annotation
python3 llm_interpreter.py      # Test LLM (requires API key)
```

## Next Steps

Potential enhancements:
- [ ] Support for VCF files (whole genome sequencing)
- [ ] Export analysis reports to PDF
- [ ] Family pedigree analysis
- [ ] Integration with more variant databases (SNPedia, ClinVar)
- [ ] Risk calculator (calculate combined disease risk scores)
- [ ] Ancestry analysis integration
- [ ] Drug-gene interaction checker for prescriptions

## Privacy & Ethics

- **No data collection**: Your DNA data is never stored or transmitted
- **Open source**: You can audit exactly what happens with your data
- **Local first**: All heavy computation happens on your machine
- **User control**: You decide what information to share

## Disclaimer

This tool is a research/educational project. While it attempts to provide accurate information about genetic variants, genetic science is constantly evolving. Always verify important health information with qualified healthcare providers.

## Support

For issues, questions, or contributions, please refer to the Task Master system:
- Task 1: DNA file parser ✓
- Task 2: Health SNP database ✓
- Task 3: Variant annotation ✓
- Task 4: LLM explanation engine ✓
