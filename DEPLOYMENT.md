# Deployment Guide

## Local Development

### Quick Start
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### Environment Setup
The app requires:
- `.env` file with `ANTHROPIC_API_KEY`
- DNA file in `source/` directory (or user can specify path)

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy—it's free and handles hosting automatically.

#### Steps:

1. **Push code to GitHub**
   ```bash
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub account
   - Click "New app"

3. **Configure app**
   - Repository: `your-username/dna-analysis`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **Add Secrets**
   - In Streamlit Cloud dashboard, click "⋮" → "Settings" → "Secrets"
   - Add your API key:
     ```
     ANTHROPIC_API_KEY = "your-api-key-here"
     ```

5. **Deploy**
   - Click "Deploy!"
   - App will be live at `https://your-username-dna-analysis.streamlit.app`

**Note:** For security, `.env` files are never uploaded. Secrets must be configured in the Streamlit Cloud dashboard.

### Option 2: Docker (Self-Hosted)

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY streamlit_app.py .
COPY health_trait_agent.py .
COPY dna_parser.py .
COPY health_snps.py .
COPY variant_annotator.py .

# Create source directory for DNA files
RUN mkdir -p source

# Configure Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "runOnSave = true" >> ~/.streamlit/config.toml

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

#### Build and Run

```bash
# Build image
docker build -t dna-analyzer .

# Run container with API key
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY="your-api-key" \
  -v $(pwd)/source:/app/source \
  dna-analyzer
```

Visit `http://localhost:8501`

### Option 3: Traditional Server (Python)

#### Requirements
- Python 3.8+
- Server with public IP
- SSL certificate (recommended)

#### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn (production)
pip install gunicorn
gunicorn --bind 0.0.0.0:8501 \
  --workers 1 \
  --worker-class sync \
  --timeout 120 \
  streamlit.web.cli:main -- run streamlit_app.py
```

Or use supervisor/systemd for process management.

## Important Considerations

### Security

1. **API Keys**: Never commit `.env` to Git
   - Use `.gitignore` (already configured)
   - Use platform-specific secret management (Streamlit Cloud, Docker, etc.)

2. **DNA Data**:
   - User DNA files are loaded locally, not transmitted
   - Only variant annotations sent to Claude API
   - No data storage—processed on-demand

3. **HTTPS**: Use SSL/TLS in production

### Scaling

- For single user: Streamlit Cloud free tier is sufficient
- For multiple users: Consider dedicated server
- Database: Not needed—stateless design

### Customization

Before deploying, consider:
- Change DNA file path in sidebar
- Update medical disclaimer
- Add organization branding
- Customize color scheme

## Troubleshooting

### "ModuleNotFoundError" on Deploy
- Ensure all imports are in `requirements.txt`
- Check Python version compatibility
- Verify all .py files are included

### Streamlit Cloud Timeout
- Large DNA files may take >60 seconds to parse
- Consider pre-parsing files or using a background task

### API Key Issues
- Streamlit Cloud: Add via Secrets panel
- Docker: Pass via environment variable
- Local: Use `.env` file

## Support

For issues with:
- **Streamlit**: https://discuss.streamlit.io
- **Anthropic API**: https://console.anthropic.com
- **This project**: Check GitHub issues

---

Happy deploying! 🚀🧬
