# 🍳 Recipe Extraction Challenge

A Python-based solution for extracting recipe data from PDFs using GPT-4, LangChain, and PyMuPDF.

This project is created for the CookUnity recipe extraction challenge.

---

## 🚀 Running the Project

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key**:
   - Copy `env_example.txt` to `.env`
   - Replace the placeholder with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   - Get your API key from: https://platform.openai.com/api-keys

3. **Run the extraction**:
   ```bash
   cd src
   python extract.py
   ```

4. **Check results**:
   - JSON files are saved to `data/output/`
   - Each recipe generates a structured JSON file

---

## 📁 Project Structure

```
recipe-extraction-challenge/
├── data/
│   ├── input/          # PDF files
│   └── output/         # Generated JSON files
├── src/
│   ├── extract.py      # Main extraction script
├── schema/
│   └── schema.json     # JSON schema definition
├── requirements.txt     # Dependencies
├── env_example.txt     # Environment template
└── README.md          # Documentation
```

--

## 🛠️ Tool Selection & Flow

#### Python
- Fast development with rich AI / data science ecosystem

#### Processing Flow

1. **Extract** text from PDF using PyMuPDF
   - **PyMuPDF (fitz)**: Fast, reliable PDF text extraction with complex layout handling

2. **Parse** recipe text using GPT-4 via LangChain
   - **LangChain**: Provides error handling, built-in JSON parsing, and easy prompt engineering
   - **GPT-4**: Superior understanding of recipe structure and cooking terminology

3. **Structure** output as JSON using LangChain's JsonOutputParser

4. **Validate** against schema and save to file
   - **JSON Schema**: Ensures consistent output structure and validation

#### Data Management
- **Python-dotenv**: Secure API key management

---

## 🔧 Assumptions & Accuracy

#### Assumptions Made
- **Missing data**: Intelligently estimated based on cooking methods and component types
- **Chef names**: Only extracted from explicit mentions (no hallucination)

#### What Works Well
- **Structured Prompts:** help make sense of ambigious / missing data 
- **JSON Parsing:** adheres to schema after multiple iterations

#### What Needs Improvement
- Support for **handwritten** or **poorly scanned PDFs** and **unconventional recipe formats**

---

## 🚀 Future Improvements 

**Given 2 Hours..**
- I would do an in-depth validation of JSON Outputs with **unit tests**. I would also validate allergen outputs against a **known allergens list**. 

**Given 2 Weeks...**
- I would **fine-tune a custom GPT** on a wider variety of recipe data and add add a **front-end review UI** for upload + review + correction.

**To Scale...**
- I would implement a **human-in-the-loop review system**, as well as an **analystics dashboard** to show **per-field parsing confidence**.

---

## 🐛 Troubleshooting

#### OpenAI API key not found
- Ensure you have a `.env` file with your API key
- Check that `python-dotenv` is installed

#### JSON decode errors
- Usually means GPT returned malformed JSON
- Check your internet connection and API key validity
