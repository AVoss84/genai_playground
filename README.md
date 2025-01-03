# GenAI Playground

Completely unrelated GenAI code examples 

## Local package installation

Create virtual environment with all package dependencies

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh                  # get uv manager
uv venv genai --python 3.12
source genai/bin/activate
```

```bash
#uv pip install -r requirements.txt
# Optional: in case of missing ssl certificates (uv does not pick up pip's config)
uv pip install -r requirements.txt --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

Run streamlit dashboard 
```bash
streamlit run streamlit_llama32_vision.py
```

Run chainlit dashboard for agentic dashboard
```bash
chainlit run chainlit_llama32_vision.py --host 127.0.0.1 --port 5000 -w
```
