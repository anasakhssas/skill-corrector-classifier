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
    "soft skill",
    "hard skill", 
    "tool",
    "framework",
    "programming language",
    "domain knowledge",
    "other"
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
    
    prompt = f"""You are a professional skills classifier. Analyze the following skill and provide a structured response.

Skill: "{skill_input}"

Instructions:
1. Normalize the skill (correct typos, standardize format, fix accents)
2. Classify it into ONE of these categories: {', '.join(CATEGORIES)}
3. Provide a confidence score (0-100)

Respond ONLY with a valid JSON object in this exact format:
{{
    "canonical": "Corrected Skill Name",
    "category": "category name",
    "confidence": 95
}}

Example:
Input: "machien lerning"
Output: {{"canonical": "Machine Learning", "category": "domain knowledge", "confidence": 90}}

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
        return json.dumps({
            "error": "Please enter a skill to analyze"
        }, ensure_ascii=False, indent=2)
    
    # Check if API key is configured
    if not API_KEY or API_KEY == "VOTRE_API_KEY_ICI":
        return json.dumps({
            "error": "API key not configured",
            "help": f"Configure your API key in app.py or set LLM_API_KEY environment variable. Get key from: {LLM_PROVIDERS[PROVIDER]['docs']}"
        }, ensure_ascii=False, indent=2)
    
    # Normalize the input
    normalized = normalize_skill(skill_input)
    
    # Call appropriate LLM API
    if PROVIDER == "groq":
        llm_result = call_groq_api(skill_input)
    else:  # huggingface
        llm_result = call_huggingface_api(skill_input)
    
    # Check for errors
    if "error" in llm_result:
        return json.dumps({
            "error": llm_result["error"],
            "detail": llm_result.get("detail", ""),
            "input": skill_input,
            "normalized": normalized
        }, ensure_ascii=False, indent=2)
    
    # Build final result
    result = {
        "input": skill_input,
        "normalized": normalized,
        "canonical": llm_result.get("canonical", skill_input),
        "category": llm_result.get("category", "other"),
        "confidence": llm_result.get("confidence", 0),
        "note": f"Classified by {LLM_PROVIDERS[PROVIDER]['name']}"
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)

# Create Gradio interface
def create_interface():
    """Create and return the Gradio interface."""
    
    with gr.Blocks(title="Skill Corrector & Classifier - Powered by LLM", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎯 Skill Corrector & Classifier")
        gr.Markdown(f"### Powered by AI - Using {LLM_PROVIDERS[PROVIDER]['name']}")
        
        with gr.Row():
            with gr.Column():
                skill_input = gr.Textbox(
                    label="Enter a skill to analyze",
                    placeholder="e.g., Docker, travail d'equipe, machien lerning, kubernete...",
                    lines=2,
                    scale=3
                )
                
                submit_btn = gr.Button("🚀 Analyze Skill", variant="primary", size="lg")
        
        with gr.Row():
            output = gr.JSON(label="Analysis Result", scale=2)
        
        # Examples
        gr.Examples(
            examples=[
                ["Docker"],
                ["travail d'équipe"],
                ["machien lerning"],
                ["kubernete"],
                ["PYTHON"],
                ["fibre optique"],
                ["communicaton"],
                ["spring boot"],
                ["devloppement web"],
                ["résolution de problémes"],
                ["tensorflow"],
                ["géstion de projet"]
            ],
            inputs=skill_input,
            label="💡 Try these examples"
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
        
        # Footer info
        gr.Markdown(
            f"""
            ---
            **Categories:** {', '.join(CATEGORIES)}
            
            **How it works:** 
            1. Enter a skill (supports French & English, handles typos and accents)
            2. AI analyzes and corrects the skill
            3. Get canonical name, category, and confidence score
            
            **Provider:** {LLM_PROVIDERS[PROVIDER]['name']}
            """
        )
    
    return demo

# Launch the app
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
