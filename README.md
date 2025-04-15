# ai-workflow-mvp

**ai-workflow-mvp** is a lightweight framework to prototype and run AI workflows using YAML and Prompty. Built for developers who want a minimal but scalable base to compose multi-step LLM pipelines and deploy them easily with FastAPI and Docker.

---

## ✨ Features

- YAML-based flow definitions ✅
- Prompty prompt templates with parameters ✅
- CLI and FastAPI interfaces ✅
- Environment-variable-based config ✅
- Docker-ready deployment ✅

---

## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/ai-workflow-mvp.git
cd ai-workflow-mvp
```

### 2. Set up `.env`

```env
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. Run via CLI

```bash
python3 -m pipeline_core.flows.run_flow --flow pipeline_core/flows/hello.yaml
```

### 4. Run API Server (Dev)

```bash
./scripts/dev_start.sh
# access via http://localhost:8000/docs
```

### 5. Run API Server (Prod, Docker)

```bash
docker build -t ai-workflow-mvp .
docker run -p 8000:8000 --env-file .env ai-workflow-mvp
```

---

## 🔁 Example Flow: `hello.yaml`

```yaml
name: Hello Flow
blocks:
  - id: translate_to_spanish
    type: prompt
    prompty_path: pipeline_core/prompts/translate_to_spanish.prompty
    inputs:
      text_input: "Hello!"
    outputs:
      - spanish_text

  - id: translate_back_to_english
    type: prompt
    prompty_path: pipeline_core/prompts/translate_back_to_english.prompty
    inputs:
      spanish_text: ${translate_to_spanish.spanish_text}
    outputs:
      - file_saved_path

  - id: save_output
    type: save_file
    inputs:
      text: ${translate_back_to_english.file_saved_path}
      path: ./outputs/translated_back.txt
```

---

## 🧠 Example Prompty Template: `translate_to_spanish.prompty`

```yaml
name: translate_to_spanish
input_variables:
  - text_input
model:
  api: chat
  configuration:
    model: gpt-3.5-turbo
parameters:
  temperature: 0.3
  max_tokens: 512
messages:
  - role: system
    content: "You are a translator."
  - role: user
    content: "Translate the following English text into Spanish:\n\n{{text_input}}"
```

---

## 🧰 Project Structure

```
.
├── pipeline_core/
│   ├── flows/
│   │   └── run_flow.py
│   ├── models/
│   │   └── models.py (PromptBlock, FlowRunner)
│   └── prompts/
│       └── *.prompty
├── api/
│   └── main.py
├── scripts/
│   ├── dev_start.sh
│   └── prod_start.sh
├── requirements.txt
├── Dockerfile
└── .env
```

---

## 📜 License

MIT License — built by [Matias Iglesias](https://github.com/matuteiglesias)

---

## 🌱 Future Ideas

- Plugin-style block extensions (tools, retrieval, etc.)
- Flow visualizer / trace tools
- HuggingFace deployment starter
- Prompt + flow marketplace

> PRs and contributions welcome! This is just the start.


