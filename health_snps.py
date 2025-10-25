"""
Curated database of health-related SNPs.
Focus on well-studied variants with clear health implications.
"""

# Health SNP Database
# Format: rsid -> {gene, trait, genotypes, descriptions}
HEALTH_SNPS = {
    # CARDIOVASCULAR HEALTH
    "rs10757274": {
        "gene": "9p21.3",
        "trait": "Cardiovascular disease risk",
        "alleles": {"G": "risk", "A": "protective"},
        "description": "Associated with increased risk of heart attack and stroke"
    },
    "rs1333049": {
        "gene": "9p21.3",
        "trait": "Cardiovascular disease",
        "alleles": {"C": "risk", "G": "protective"},
        "description": "Strongly associated with myocardial infarction"
    },
    "rs2383206": {
        "gene": "ANRIL",
        "trait": "Atherosclerosis",
        "alleles": {"T": "risk", "C": "protective"},
        "description": "Associated with atherosclerotic cardiovascular disease"
    },

    # CHOLESTEROL & LIPIDS
    "rs429358": {
        "gene": "APOE",
        "trait": "Cholesterol & Alzheimer's disease",
        "alleles": {"C": "normal", "T": "risk"},
        "description": "APOE4 variant associated with higher cholesterol and Alzheimer's risk"
    },
    "rs7412": {
        "gene": "APOE",
        "trait": "Cholesterol & Alzheimer's disease",
        "alleles": {"C": "normal", "T": "protective"},
        "description": "APOE2 variant, protective for Alzheimer's"
    },

    # CAFFEINE METABOLISM
    "rs762551": {
        "gene": "CYP1A2",
        "trait": "Caffeine sensitivity",
        "alleles": {"A": "fast metabolizer", "C": "slow metabolizer"},
        "description": "Fast metabolizers (AA) clear caffeine quickly. Slow metabolizers (CC) retain caffeine longer"
    },

    # LACTOSE TOLERANCE
    "rs4988235": {
        "gene": "MCM6",
        "trait": "Lactose intolerance",
        "alleles": {"C": "lactose tolerant", "T": "lactose intolerant"},
        "description": "CC = lactose tolerant, CT = mostly tolerant, TT = lactose intolerant"
    },

    # VITAMIN D
    "rs2282679": {
        "gene": "GC",
        "trait": "Vitamin D metabolism",
        "alleles": {"T": "higher vitamin D", "G": "lower vitamin D"},
        "description": "Affects vitamin D binding protein and vitamin D levels"
    },

    # DRUG METABOLISM
    "rs1045642": {
        "gene": "MDR1/ABCB1",
        "trait": "Drug metabolism",
        "alleles": {"C": "normal", "T": "reduced drug transport"},
        "description": "Affects absorption and transport of many medications"
    },
    "rs4149056": {
        "gene": "SLCO1B1",
        "trait": "Statin metabolism",
        "alleles": {"C": "normal metabolism", "T": "reduced metabolism"},
        "description": "TT carriers have reduced statin metabolism and increased side effect risk"
    },

    # ALZHEIMER'S DISEASE
    "rs11136000": {
        "gene": "CLUSTERIN",
        "trait": "Alzheimer's disease",
        "alleles": {"T": "increased risk", "C": "protective"},
        "description": "Associated with increased Alzheimer's disease risk"
    },

    # TYPE 2 DIABETES
    "rs7903146": {
        "gene": "TCF7L2",
        "trait": "Type 2 diabetes",
        "alleles": {"C": "lower risk", "T": "higher risk"},
        "description": "TT genotype associated with 1.5x increased diabetes risk"
    },
    "rs1801282": {
        "gene": "PPARG",
        "trait": "Insulin sensitivity",
        "alleles": {"C": "normal", "G": "improved insulin sensitivity"},
        "description": "G allele associated with improved insulin sensitivity"
    },

    # BONE HEALTH
    "rs1801018": {
        "gene": "COL1A1",
        "trait": "Bone mineral density",
        "alleles": {"S": "higher density", "s": "lower density"},
        "description": "Associated with bone mineral density"
    },

    # ATHLETIC PERFORMANCE
    "rs1815834": {
        "gene": "ACTN3",
        "trait": "Muscle fiber type",
        "alleles": {"R": "power/speed", "X": "endurance"},
        "description": "RR genotype associated with power and speed performance, XX with endurance"
    },

    # HAIR COLOR
    "rs12913832": {
        "gene": "HERC2",
        "trait": "Eye color",
        "alleles": {"A": "brown eyes", "G": "blue eyes"},
        "description": "Strongly associated with eye color, GG = blue, AA/GA = brown"
    },

    # ALCOHOL METABOLISM
    "rs1042026": {
        "gene": "ADH1B",
        "trait": "Alcohol flush reaction",
        "alleles": {"G": "normal", "A": "alcohol flush"},
        "description": "A allele associated with alcohol flush reaction and reduced alcohol tolerance"
    },

    # SLEEP
    "rs11900115": {
        "gene": "DEC2",
        "trait": "Sleep duration",
        "alleles": {"T": "normal sleep needs", "C": "may sleep less"},
        "description": "Associated with natural short sleep duration"
    },

    # METABOLISM & WEIGHT
    "rs9939609": {
        "gene": "FTO",
        "trait": "Obesity risk",
        "alleles": {"A": "lower obesity risk", "T": "higher obesity risk"},
        "description": "TT genotype associated with ~1.5 kg higher BMI and increased obesity risk"
    },

    # BLEEDING DISORDERS
    "rs6025": {
        "gene": "F5",
        "trait": "Blood clotting (Factor V Leiden)",
        "alleles": {"G": "normal", "A": "increased clotting risk"},
        "description": "A allele (Factor V Leiden) associated with increased blood clot risk"
    },

    # GLAUCOMA
    "rs2165241": {
        "gene": "SRBD1",
        "trait": "Glaucoma",
        "alleles": {"C": "lower risk", "T": "higher risk"},
        "description": "Associated with primary open-angle glaucoma"
    },

    # MIGRAINE
    "rs6478241": {
        "gene": "PRDM16",
        "trait": "Migraine",
        "alleles": {"A": "higher risk", "G": "protective"},
        "description": "Associated with increased migraine susceptibility"
    },
}


def get_health_snp(rsid: str) -> dict:
    """Get health information for a specific SNP."""
    return HEALTH_SNPS.get(rsid, None)


def get_all_health_snps() -> dict:
    """Get all health SNPs."""
    return HEALTH_SNPS.copy()


def get_health_snps_list() -> list:
    """Get list of all rsIDs we track."""
    return list(HEALTH_SNPS.keys())


def explain_genotype(rsid: str, genotype: str) -> str:
    """
    Generate human-readable explanation for a genotype.

    Args:
        rsid: SNP identifier
        genotype: User's genotype (e.g., "AA", "AG", "GG")

    Returns:
        Human-readable explanation
    """
    snp_info = get_health_snp(rsid)
    if not snp_info:
        return None

    alleles = snp_info.get('alleles', {})
    trait = snp_info.get('trait', '')
    description = snp_info.get('description', '')

    if not genotype or len(genotype) < 2:
        return None

    allele1, allele2 = genotype[0], genotype[1]

    effect1 = alleles.get(allele1, '')
    effect2 = alleles.get(allele2, '')

    # Build explanation
    explanation = f"**{rsid} ({snp_info.get('gene', 'Unknown')})**\n"
    explanation += f"Trait: {trait}\n"
    explanation += f"Your genotype: {genotype}\n"
    explanation += f"Interpretation: {description}"

    return explanation


if __name__ == "__main__":
    print(f"Health SNP Database: {len(HEALTH_SNPS)} tracked variants\n")

    # Show sample SNPs
    sample_rsids = list(HEALTH_SNPS.keys())[:5]
    for rsid in sample_rsids:
        info = get_health_snp(rsid)
        print(f"{rsid}: {info['gene']} - {info['trait']}")
