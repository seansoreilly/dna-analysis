"""
Streamlit app for Health Trait Agent
Analyze ANY health trait based on YOUR DNA
"""

import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from health_trait_agent import HealthTraitAgent

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Page configuration
st.set_page_config(
    page_title="DNA Health Trait Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .disclaimer {
        background-color: #fff3cd;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
        border-left: 4px solid #ffc107;
    }
    .variant-table {
        margin-top: 1em;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
    st.session_state.dna_loaded = False
    st.session_state.user_snps_count = 0
    st.session_state.health_variants_found = 0

# Sidebar
with st.sidebar:
    st.markdown("### 🧬 DNA Health Analyzer")
    st.markdown("---")

    # DNA file loading options
    st.markdown("**Load Your DNA**")

    load_option = st.radio(
        "Choose how to load your DNA:",
        options=["Upload File", "File Path"],
        label_visibility="collapsed"
    )

    dna_file = None

    if load_option == "Upload File":
        uploaded_file = st.file_uploader(
            "Choose your 23andMe DNA file",
            type=["txt"],
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            dna_file = uploaded_file
    else:
        dna_file_path = st.text_input(
            "DNA file path",
            value="source/genome_Sean_O_Reilly_v3_Full_20170428141907.txt",
            label_visibility="collapsed"
        )
        if dna_file_path:
            dna_file = dna_file_path

    # Load button
    if st.button("Load DNA File", use_container_width=True, type="primary"):
        if dna_file is None:
            st.error("Please select or upload a DNA file first")
        else:
            with st.spinner("Loading and parsing your DNA (this may take a minute)..."):
                try:
                    agent = HealthTraitAgent()

                    # Handle uploaded file or file path
                    if hasattr(dna_file, 'read'):
                        # It's an uploaded file - save temporarily
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                            tmp.write(dna_file.read())
                            tmp_path = tmp.name
                        success = agent.load_dna(tmp_path)
                    else:
                        # It's a file path
                        success = agent.load_dna(dna_file)

                    if success:
                        st.session_state.agent = agent
                        st.session_state.dna_loaded = True
                        st.session_state.user_snps_count = len(agent.user_snps)

                        # Count health variants
                        health_variants = sum(
                            1 for rsid in agent.health_snps_db.keys()
                            if rsid in agent.user_snps
                        )
                        st.session_state.health_variants_found = health_variants

                        st.success(f"✓ Loaded {st.session_state.user_snps_count:,} SNPs")
                        st.success(f"✓ Found {health_variants} health-related variants")
                    else:
                        st.error("Failed to load DNA file - please check the file format")
                except FileNotFoundError:
                    st.error("❌ DNA file not found. Please check the file path or upload the file.")
                except Exception as e:
                    st.error(f"❌ Error loading DNA: {str(e)}")

    st.markdown("---")

    # Show loaded status
    if st.session_state.dna_loaded:
        st.markdown("**📊 Your DNA Profile**")
        st.metric("Total SNPs Loaded", f"{st.session_state.user_snps_count:,}")
        st.metric("Health Variants", st.session_state.health_variants_found)

        st.markdown("---")

        # Show health variants
        if st.checkbox("Show your health variants", value=True):
            st.markdown("**Your Health Variants**")
            agent = st.session_state.agent

            variant_data = []
            for rsid, info in sorted(agent.health_snps_db.items()):
                if rsid in agent.user_snps:
                    variant_data.append({
                        "rsID": rsid,
                        "Gene": info.get("gene", "?"),
                        "Genotype": agent.user_snps[rsid],
                        "Trait": info.get("trait", "?")
                    })

            if variant_data:
                for v in variant_data:
                    st.caption(f"**{v['rsID']}** ({v['Gene']}) {v['Genotype']}")
                    st.caption(f"_{v['Trait']}_")

        st.markdown("---")

        # Reset conversation button
        if st.button("Reset Conversation", use_container_width=True):
            st.session_state.agent.reset_conversation()
            st.session_state.conversation = []
            st.success("Conversation reset")
            st.rerun()
    else:
        st.info("👈 Load your DNA file to get started")

# Main content
st.markdown('<div class="main-header">🧬 DNA Health Trait Analyzer</div>', unsafe_allow_html=True)
st.markdown("Ask about ANY health trait and learn about your genetic predisposition")

# Medical disclaimer
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Medical Disclaimer:</strong> This tool provides educational information about genetics, not medical advice.
It should not be used for diagnosis or treatment. Always consult healthcare professionals for medical concerns.
</div>
""", unsafe_allow_html=True)

# Check if DNA is loaded
if not st.session_state.dna_loaded:
    st.warning("👈 Please load your DNA file using the sidebar to get started")

    st.markdown("### Example Questions")
    st.markdown("""
    Once you load your DNA, you can ask questions like:
    - "Do I have increased risk for heart disease?"
    - "What's my genetic predisposition to type 2 diabetes?"
    - "How does caffeine affect me genetically?"
    - "What's my Alzheimer's disease risk based on my DNA?"
    - "Am I genetically predisposed to obesity?"
    - "What about my cholesterol metabolism?"
    """)
else:
    # Initialize chat history if not exists
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Display conversation history
    for i, msg in enumerate(st.session_state.conversation):
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    # User input
    if question := st.chat_input("Ask about a health trait..."):
        # Add user message to history
        st.session_state.conversation.append({
            "role": "user",
            "content": question
        })

        # Display user message
        with st.chat_message("user"):
            st.write(question)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your DNA..."):
                try:
                    response = st.session_state.agent.ask_about_trait(question)
                    st.write(response)

                    # Add assistant response to history
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": response
                    })
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Help section
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        **This tool helps you understand your genetics:**

        1. **Ask any health-related question** - The agent will identify genes involved in that trait
        2. **The system checks YOUR DNA** - It looks for relevant variants in your 939,000+ SNPs
        3. **You get personalized answers** - Based on your specific genotypes
        4. **Follow-up questions work** - The agent remembers your conversation history

        **Example Questions:**
        - "What's my risk for high blood pressure?"
        - "How does my caffeine metabolism work?"
        - "What's my genetic risk for depression?"
        - "Do I have variants related to exercise performance?"

        **Important Notes:**
        - This is educational information, not medical advice
        - Click "Reset Conversation" to start a new conversation thread
        - Your DNA stays private - nothing is stored or transmitted
        """)
