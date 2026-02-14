# 🎯 Skill Corrector & Classifier

A Gradio-based web application powered by AI that normalizes, corrects, and classifies professional skills using Large Language Models (LLMs). Supports both French and English skills.

## What It Does

The app uses AI (LLM) to intelligently analyze skills:

1. **Normalizes** the input (handles typos, accents, case variations)
2. **Corrects** the skill using AI understanding (not just string matching)
3. **Classifies** the skill into categories:
   - Soft skill
   - Hard skill
   - Tool
   - Framework
   - Programming language
   - Domain knowledge
   - Other

4. **Returns** a JSON response with:
   - Original input
   - Normalized form
   - Canonical skill name (AI-corrected)
   - Category
   - Confidence score (0-100)
   - Analysis note

## ✨ Features

- 🤖 **AI-Powered Classification** - Uses LLM for intelligent skill analysis
- 🆓 **Free API Options** - Groq and Hugging Face free tiers supported
- 🌍 **Bilingual** - Supports French and English
- 🔧 **Handles Typos** - "machien lerning" → "Machine Learning"
- 🎨 **Accent-Aware** - "travail d'equipe" → "Travail d'équipe"
- ⚡ **Simple Interface** - Just enter a skill and get instant results

## 🚀 Quick Start

### 1. Get Your Free API Key

Choose one of these providers:

#### Option A: Groq (Recommended - Fastest)

1. Go to https://console.groq.com/keys
2. Sign up for a free account
3. Create a new API key
4. Copy the key

**Why Groq?**
- ⚡ Ultra-fast inference (Llama 3.3 70B)
- 🆓 Generous free tier
- 🎯 High accuracy

#### Option B: Hugging Face

1. Go to https://huggingface.co/settings/tokens
2. Sign up for a free account
3. Create a new token (Read access)
4. Copy the token

### 2. Configure Your API Key

Edit [app.py](app.py) and replace the placeholder:

```python
# Line 9-10 in app.py
API_KEY = os.getenv("LLM_API_KEY", "VOTRE_API_KEY_ICI")  # Remplacez par votre clé
PROVIDER = "groq"  # Options: "groq" ou "huggingface"
```

**Method 1: Direct in code** (simple)
```python
API_KEY = "gsk_your_actual_api_key_here"
PROVIDER = "groq"
```

**Method 2: Environment variable** (recommended for production)
```bash
# Windows PowerShell
$env:LLM_API_KEY = "gsk_your_actual_api_key_here"

# Linux/Mac
export LLM_API_KEY="gsk_your_actual_api_key_here"
```

### 3. Install and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will launch at `http://localhost:7860`

## 📦 Deploy on Hugging Face Spaces

### Option A: Web Upload

1. **Create a new Space** on [Hugging Face](https://huggingface.co/spaces)
2. **Select SDK:** Gradio
3. **Upload files:**
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. **Add Secret:**
   - Go to Space Settings → Variables and secrets
   - Add `LLM_API_KEY` with your API key value
   - Restart the space

### Option B: Git Push

```bash
git clone https://huggingface.co/spaces/<your-username>/<space-name>
cd <space-name>

# Copy your files
cp /path/to/app.py .
cp /path/to/requirements.txt .
cp /path/to/README.md .

git add .
git commit -m "Deploy skill classifier"
git push
```

Then add your API key as a **Secret** in Space Settings.

Your app will be available at:
`https://huggingface.co/spaces/<your-username>/<space-name>`

## 🎮 How to Use

1. Open the app in your browser
2. **Type a skill** (e.g., "machien lerning", "travail d'équipe")
3. **Click "Analyze Skill"** or press Enter
4. **Get instant results** with corrected name, category, and confidence

### Example Results

**Input:** `machien lerning`
```json
{
  "input": "machien lerning",
  "normalized": "machien lerning",
  "canonical": "Machine Learning",
  "category": "domain knowledge",
  "confidence": 92,
  "note": "Classified by Groq (Llama 3.3 70B)"
}
```

**Input:** `travail d'equipe`
```json
{
  "input": "travail d'equipe",
  "normalized": "travail d'equipe",
  "canonical": "Travail d'équipe",
  "category": "soft skill",
  "confidence": 95,
  "note": "Classified by Groq (Llama 3.3 70B)"
}
```

## 🔧 Configuration

In [app.py](app.py), you can customize:

**Lines 9-10: API Configuration**
```python
API_KEY = os.getenv("LLM_API_KEY", "YOUR_KEY_HERE")
PROVIDER = "groq"  # or "huggingface"
```

**Lines 12-19: Skill Categories**
```python
CATEGORIES = [
    "soft skill",
    "hard skill",
    "tool",
    "framework",
    "programming language",
    "domain knowledge",
    "other"
]
```

**Model parameters** (in `call_groq_api` or `call_huggingface_api`):
- `temperature`: 0.3 (lower = more consistent)
- `max_tokens`: 500 (response length)

## 🛠️ Tech Stack

- **Gradio** - Web interface
- **Requests** - HTTP API calls
- **Unidecode** - Accent normalization
- **Groq API** - Fast LLM inference (Llama 3.3 70B)
- **Hugging Face** - Alternative LLM provider (Mistral 7B)
- Python 3.8+

## 🔜 Future Enhancements

- [ ] Batch processing (analyze multiple skills at once)
- [ ] Export results to CSV/JSON
- [ ] Analytics dashboard
- [ ] Custom categories
- [ ] REST API endpoint
- [ ] Support for more LLM providers

## 🆘 Troubleshooting

### "API key not configured"
→ Edit [app.py](app.py) line 9 and add your API key.

### "API Error: 401"
→ Invalid API key. Check that you copied it correctly.

### "API Error: 429"
→ Rate limit exceeded. Wait a moment or upgrade your API plan.

### "Connection timeout"
→ Check your internet connection or try again.

### JSON parsing errors
→ The LLM response wasn't in the expected format. Try again.

## 📝 Database (Optional)

The `skills_db.json` file is **not required** for the LLM version - it's kept for reference only. The LLM handles classification intelligently without needing a predefined database.

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Add support for more LLM providers
- Improve prompts for better accuracy

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ and AI**
