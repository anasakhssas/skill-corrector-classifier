import json
import gradio as gr
from unidecode import unidecode
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# ==================== CONFIGURATION ====================
# L'API key est chargée automatiquement depuis le fichier .env
API_KEY = os.getenv("LLM_API_KEY")
PROVIDER = "groq"  # Options: "groq" ou "huggingface"

CATEGORIES = [
    "Langues",                          # French, English, Spanish, etc.
    "Compétences comportementales",     # Leadership, Communication, Teamwork, etc.
    "Compétences techniques",           # Data Analysis, Project Management, etc.
    "Logiciels & Outils",               # Excel, Photoshop, Git, Docker, etc.
    "Langages de programmation",        # Python, Java, JavaScript, etc.
    "Frameworks & Bibliothèques",       # React, Django, Spring Boot, etc.
    "Domaines d'expertise",             # Machine Learning, Marketing, Finance, etc.
    "Certifications",                   # PMP, AWS Certified, SCRUM Master, etc.
    "Autre"
]

# Available LLM providers
LLM_PROVIDERS = {
    "groq": {
        "name": "Groq (Llama 3.3 70B)",
        "api_url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama-3.3-70b-versatile",
        "docs": "https://console.groq.com/keys"
    },
    "huggingface": {
        "name": "Hugging Face (Mistral 7B)",
        "api_url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "docs": "https://huggingface.co/settings/tokens"
    }
}

def normalize_skill(text):
    """
    Normalize a skill string:
    - Strip whitespace
    - Lowercase
    - Remove accents
    - Collapse multiple spaces to single space
    """
    if not text:
        return ""
    
    # Strip and lowercase
    normalized = text.strip().lower()
    
    # Remove accents
    normalized = unidecode(normalized)
    
    # Collapse multiple spaces
    normalized = " ".join(normalized.split())
    
    return normalized

def call_groq_api(skill_input):
    """Call Groq API for skill classification."""
    
    prompt = f"""You are a professional recruiter skills classifier for CV/Resume analysis. Analyze the following skill and classify it.

Skill to classify: "{skill_input}"

Instructions:
1. **CORRECT** any typos, spelling errors, missing accents (especially in French), and formatting issues
   - Fix missing accents: "travail d'equipe" → "Travail d'équipe"
   - Fix typos: "machien lerning" → "Machine Learning"
   - Standardize capitalization
   - Fix spacing and punctuation
   
2. Classify it into ONE of these categories:
   - Langues (French, English, Spanish, etc.)
   - Compétences comportementales (Leadership, Communication, Teamwork, etc.)
   - Compétences techniques (Data Analysis, Project Management, etc.)
   - Logiciels & Outils (Excel, Photoshop, Git, Docker, etc.)
   - Langages de programmation (Python, Java, JavaScript, etc.)
   - Frameworks & Bibliothèques (React, Django, Spring Boot, etc.)
   - Domaines d'expertise (Machine Learning, Marketing, Finance, etc.)
   - Certifications (PMP, AWS Certified, SCRUM Master, etc.)
   - Autre (if none of the above fit)

3. Provide a confidence score (0-100)

Respond ONLY with a valid JSON object:
{{
    "canonical": "Corrected Name",
    "category": "category name",
    "confidence": 95
}}

Examples:
- Input: "travail d'equipe" → {{"canonical": "Travail d'équipe", "category": "Compétences comportementales", "confidence": 100}}
- Input: "anglais" → {{"canonical": "Anglais", "category": "Langues", "confidence": 100}}
- Input: "machien lerning" → {{"canonical": "Machine Learning", "category": "Domaines d'expertise", "confidence": 90}}
- Input: "python" → {{"canonical": "Python", "category": "Langages de programmation", "confidence": 100}}
- Input: "gestion de projet" → {{"canonical": "Gestion de projet", "category": "Compétences techniques", "confidence": 100}}

Now classify: "{skill_input}"
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a professional skills classifier. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            llm_result = json.loads(content)
            return llm_result
        else:
            return {"error": f"API Error: {response.status_code}", "detail": response.text}
    
    except Exception as e:
        return {"error": str(e)}

def call_huggingface_api(skill_input):
    """Call Hugging Face Inference API for skill classification."""
    
    prompt = f"""<s>[INST] You are a professional skills classifier.

Skill to analyze: "{skill_input}"

Classify this skill and respond with ONLY a JSON object:
{{
    "canonical": "Corrected Name",
    "category": "one of: {', '.join(CATEGORIES)}",
    "confidence": 85
}}
[/INST]"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.3,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result[0]["generated_text"].strip()
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            llm_result = json.loads(content)
            return llm_result
        else:
            return {"error": f"API Error: {response.status_code}", "detail": response.text}
    
    except Exception as e:
        return {"error": str(e)}

def process_skill(skill_input):
    """
    Main processing function that uses LLM to classify skills.
    """
    if not skill_input or not skill_input.strip():
        return "Veuillez entrer une compétence à analyser."
    
    # Check if API key is configured
    if not API_KEY or API_KEY == "VOTRE_API_KEY_ICI":
        return "❌ API key non configurée"
    
    # Normalize the input
    normalized = normalize_skill(skill_input)
    
    # Call appropriate LLM API
    if PROVIDER == "groq":
        llm_result = call_groq_api(skill_input)
    else:  # huggingface
        llm_result = call_huggingface_api(skill_input)
    
    # Check for errors
    if "error" in llm_result:
        return f"❌ Erreur: {llm_result['error']}"
    
    # Return formatted response with correction
    category = llm_result.get("category", "Autre")
    canonical = llm_result.get("canonical", skill_input)
    confidence = llm_result.get("confidence", 0)
    
    # Show if there was a correction
    input_lower = skill_input.strip().lower()
    canonical_lower = canonical.lower()
    
    if input_lower != canonical_lower:
        # There was a correction
        result = f"✅ **{canonical}**\n\n"
        result += f"_(Corrigé depuis : {skill_input})_\n\n"
        result += f"📂 Catégorie : **{category}**\n"
        result += f"🎯 Confiance : {confidence}%"
    else:
        # No correction needed
        result = f"✅ **{canonical}**\n\n"
        result += f"📂 Catégorie : **{category}**\n"
        result += f"🎯 Confiance : {confidence}%"
    
    return result

# Create Gradio interface
def create_interface():
    """Create and return the Gradio interface."""
    
    # Custom CSS - Minimal and centered
    custom_css = """
    /* Centered minimal design */
    .gradio-container {
        max-width: 600px !important;
        margin: 0 auto !important;
        padding: 40px 20px !important;
    }
    
    /* Header */
    .header-title {
        font-size: 28px;
        font-weight: 700;
        color: #202124;
        text-align: center;
        margin-bottom: 40px;
    }
    
    /* Input field */
    .input-field textarea {
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .input-field textarea:focus {
        border-color: #10a37f !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1) !important;
    }
    
    /* Output field */
    .output-field textarea {
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        text-align: left !important;
        color: #202124 !important;
        background: #f9fafb !important;
        min-height: 140px !important;
    }
    
    /* Button */
    button {
        background: #10a37f !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        width: 100% !important;
        margin-top: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    button:hover {
        background: #0e8c6d !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(16, 163, 127, 0.3) !important;
    }
    
    /* Remove footer */
    footer {display: none !important;}
    """
    
    with gr.Blocks(title="Skill Classifier") as demo:
        
        # Header
        gr.Markdown("## 🎯 Skill Classifier AI", elem_classes="header-title")
        
        # Input
        skill_input = gr.Textbox(
            label="",
            placeholder="Entrez une compétence...",
            lines=2,
            show_label=False,
            elem_classes="input-field"
        )
        
        # Submit button
        submit_btn = gr.Button("Classifier")
        
        # Output (using Markdown for better formatting)
        output = gr.Markdown(
            value="",
            elem_classes="output-field"
        )
        
        # Event handlers
        submit_btn.click(
            fn=process_skill,
            inputs=skill_input,
            outputs=output
        )
        
        skill_input.submit(
            fn=process_skill,
            inputs=skill_input,
            outputs=output
        )
    
    return demo, custom_css

# Launch the app
if __name__ == "__main__":
    demo, css = create_interface()
    demo.launch(css=css)
