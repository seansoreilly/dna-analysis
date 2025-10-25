# Quick Start Guide

## Setup (One-Time)

```bash
# 1. Install Python dependencies
pip install anthropic python-dotenv

# 2. Your API key is already in .env
# ✓ ANTHROPIC_API_KEY is configured

# 3. You're ready to go!
```

## Running the Tool

### Interactive Analysis (Full Experience)

```bash
python3 analyze_dna.py
```

This starts an interactive session where you can:
1. Point to your DNA file
2. See your health variants
3. Ask questions about your genetics
4. Get personalized insights

### Quick Test

```bash
python3 test_pipeline.py
```

Shows a quick demo of the full pipeline with sample outputs.

## How It Works

```
Your DNA File (23andMe/Ancestry)
         ↓
    [Parse 939K+ SNPs locally]
         ↓
    [Find 21 health variants in your DNA]
         ↓
    [Annotate with gene/trait info]
         ↓
    [Claude explains in plain English]
         ↓
    Personalized Health Insights
```

## Example: Lactose Tolerance

Your DNA shows: `rs4988235: AA`

**Claude explains:**
> Your genotype (AA) suggests you're likely lactose intolerant. This means your body probably doesn't produce much lactase enzyme in adulthood. However, individual tolerance varies—some people with this genotype can still digest dairy. Test how you personally feel after consuming dairy products.

## Your Key Findings

You have **21 tracked health variants**, including:

| Variant | Gene | Trait | Your Genotype |
|---------|------|-------|---------------|
| rs762551 | CYP1A2 | Caffeine sensitivity | AC (intermediate) |
| rs429358 | APOE | Alzheimer's/Cholesterol | TT (protective) |
| rs4988235 | MCM6 | Lactose tolerance | AA (likely intolerant) |
| rs9939609 | FTO | Obesity risk | TT (lower risk) |
| rs10757274 | 9p21.3 | Cardiovascular disease | AG (modest risk) |

## Asking Questions

After the health profile, you can ask:
- "What does my APOE mean?"
- "Am I at risk for diabetes?"
- "How does my caffeine metabolism work?"
- "What lifestyle changes would help me?"
- "How reliable is this finding?"

Claude will answer in context of your specific genetics.

## Important

⚠️ **This is NOT medical advice.** Always consult healthcare providers for medical decisions. This tool is for education and understanding your genetic data.

## Files Overview

- **analyze_dna.py** - Main interactive tool
- **test_pipeline.py** - Quick demo
- **dna_parser.py** - Parses your DNA file
- **health_snps.py** - 30 health variants database
- **variant_annotator.py** - Maps your SNPs to health info
- **llm_interpreter.py** - Uses Claude for explanations
- **source/** - Your DNA files (stays local)

## Next Steps

1. Try: `python3 test_pipeline.py` to see it in action
2. Try: `python3 analyze_dna.py` for interactive mode
3. Ask questions about your specific variants
4. Share findings with your doctor (with context about limitations)

Enjoy discovering your genetics! 🧬
