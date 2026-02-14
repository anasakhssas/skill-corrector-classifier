---
title: Skill Corrector & Classifier
emoji: 🎯
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 6.0.0
app_file: app.py
pinned: false
license: mit
---

# 🎯 Skill Corrector & Classifier

Une application web alimentée par l'IA qui corrige, normalise et classifie les compétences professionnelles en utilisant des LLM (Large Language Models). Supporte le français et l'anglais.

## 🌟 Fonctionnalités

- 🤖 **Classification IA** - Utilise Groq (Llama 3.3 70B) pour une analyse intelligente
- 🔧 **Correction automatique** - "travail d'equipe" → "Travail d'équipe"
- 🎯 **Catégorisation précise** - Classifie en 9 catégories de recrutement
- 🆓 **Gratuit** - Utilise l'API gratuite de Groq
- ⚡ **Rapide** - Réponses en temps réel
- 🌍 **Bilingue** - Français et anglais

## 📋 Catégories

- 🗣️ **Langues** - French, English, Spanish, etc.
- 💼 **Compétences comportementales** - Leadership, Communication, Teamwork, etc.
- 🔨 **Compétences techniques** - Data Analysis, Project Management, etc.
- 🛠️ **Logiciels & Outils** - Excel, Photoshop, Git, Docker, etc.
- 💻 **Langages de programmation** - Python, Java, JavaScript, etc.
- 📦 **Frameworks & Bibliothèques** - React, Django, Spring Boot, etc.
- 🎓 **Domaines d'expertise** - Machine Learning, Marketing, Finance, etc.
- 🏆 **Certifications** - PMP, AWS Certified, SCRUM Master, etc.
- ❓ **Autre** - Autres compétences

## 🎮 Utilisation

1. **Entrez une compétence** dans le champ de texte (par ex: "machien lerning", "travail d'equipe")
2. **Cliquez sur "Classifier"** ou appuyez sur Entrée
3. **Obtenez les résultats** avec :
   - ✅ Nom corrigé de la compétence
   - 📂 Catégorie identifiée
   - 🎯 Score de confiance (%)
   - _(Indication de correction si applicable)_

## 🔧 Configuration requise

Cette application nécessite une clé API Groq. Pour utiliser l'app :

1. **Obtenez une clé API gratuite** sur [console.groq.com/keys](https://console.groq.com/keys)
2. **L'administrateur doit configurer** `LLM_API_KEY` dans les Secrets du Space

⚠️ **Note aux utilisateurs:** Si l'app affiche "❌ API key non configurée", l'administrateur du Space doit ajouter la clé API dans les Settings.

## 🚀 Déploiement

Pour déployer votre propre instance :

1. **Fork ou clone** ce Space
2. Allez dans **Settings → Variables and secrets**
3. Ajoutez un nouveau secret :
   - **Name:** `LLM_API_KEY`
   - **Value:** Votre clé API Groq (commence par `gsk_`)
4. **Redémarrez** le Space

L'application démarrera automatiquement !

## 💡 Exemples

### Exemple 1: Correction d'accent
**Entrée:** `travail d'equipe`  
**Sortie:**
```
✅ Travail d'équipe
(Corrigé depuis : travail d'equipe)
📂 Catégorie : Compétences comportementales
🎯 Confiance : 100%
```

### Exemple 2: Correction de faute de frappe
**Entrée:** `machien lerning`  
**Sortie:**
```
✅ Machine Learning
(Corrigé depuis : machien lerning)
📂 Catégorie : Domaines d'expertise
🎯 Confiance : 95%
```

### Exemple 3: Classification simple
**Entrée:** `Python`  
**Sortie:**
```
✅ Python
📂 Catégorie : Langages de programmation
🎯 Confiance : 100%
```

## 🛠️ Stack Technique

- **Gradio 6.0** - Interface web
- **Groq API** - LLM inference (Llama 3.3 70B)
- **Python 3.8+**
- **Librairies:** requests, unidecode, python-dotenv

## 📝 License

MIT License - Libre d'utilisation et de modification

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Suggérer des fonctionnalités
- Améliorer les prompts pour une meilleure précision

---

**Made with ❤️ and AI**
