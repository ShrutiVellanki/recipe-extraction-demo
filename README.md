# 🍳 Recipe Extraction Demo

A Python-based solution for extracting recipe data from PDFs using GPT-5, LangChain, and PyMuPDF.

[Demo](https://www.loom.com/share/dada9955b1fa4f92a69dd31d77d56442?sid=8cee7d59-657c-45cb-964f-7a783104450d)

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
├── prompt/
│   └── recipe_extraction_prompt.txt
├── requirements.txt     # Dependencies
├── env_example.txt     # Environment template
└── README.md          # Documentation
```

---

## 🛠️ Tool Selection & Flow

#### Python
- Fast development with rich AI / data science ecosystem

#### Processing Flow

1. **Extract** text from PDF using PyMuPDF
   - **PyMuPDF (fitz)**: Fast, reliable PDF text extraction with complex layout handling
      - [Benchmarks](https://github.com/py-pdf/benchmarks) well across text extraction speed and quality

2. **Parse** recipe text using GPT-5 via LangChain
   - **LangChain**: Provides error handling, built-in JSON parsing, and easy prompt engineering
      - Orchestration layer for future use (multi-step parsing):
         - e.g. could connect [LlamaParse](https://www.llamaindex.ai/llamaparse) for PDF parsing when PDFs have figures
         - e.g. could connect to custom multilingual model for handwritten text
         - e.g. could connect to database that had nutritional information 
      - Models are swappable via LangChain config (Claude, Gemini, GPT, etc.)
   - **GPT-5**: Superior understanding of recipe structure and cooking terminology

3. **Structure** output as JSON using LangChain's JsonOutputParser

4. **Validate** against schema and save to file
   - **JSON Schema**: Ensures consistent output structure and validation

#### Data Management
- **Python-dotenv**: Secure API key management

#### Other Tools Considered
- [LlamaIndex](https://www.llamaindex.ai/) (future use, could cross reference with an index of similar recipes)
- LlamaParse (future use, could introduce parsing for PDFs with figures)
- Vanilla API calls instead of frameworks for RAG

--- 

## Prompting Approach
- **Tradeoff**: fallback logic, less flexibility, more structure (picked because structure is more essential for prepped meals)
- **Schema-based prompting**: guardrails in place so that LLM knows what its working toward
- **Future improvement**: Few Shot Prompting, gives the LLM examples of effective parsing

---

## 🔧 Assumptions & Accuracy

#### Assumptions Made
- **Missing data**: Intelligently estimated based on cooking methods and component types
- **Chef names**: Only extracted from explicit mentions (no hallucination)

#### What Works Well
- **Structured Prompts:** help make sense of ambiguous / missing data 
- **JSON Parsing:** adheres to schema after multiple iterations

#### What Needs Improvement
- Support for **handwritten** or **poorly scanned PDFs** and **unconventional recipe formats**

---

## 🚀 Future Improvements 

**What I wish I'd done differently:**
- Leverage Langchain better (e.g. use its [PyMuPDFLoader](https://python.langchain.com/docs/integrations/document_loaders/pymupdf/))
- Batch process PDFs to see if it improves processing speed

**Given 2 Hours..**
- I would do an in-depth validation of JSON Outputs with **unit tests**. I would also validate allergen outputs against a **known allergens list**. 

**Given 2 Weeks...**
- I would **fine-tune a custom GPT** on a wider variety of recipe data (pairs of recipe data + JSON output) and add a **front-end review UI** for upload + review + correction.

**To Scale...**
- I would implement a **human-in-the-loop review system**, as well as an **analytics dashboard** to show **per-field parsing confidence**.

   - Per-Field Confidence Scores could be derived from...
      1. Heuristics: (e.g. whether portion sizes are explicitly mentioned, mathematically derived, or best guesses)
      2. Agent-as-judge: An AI Agent can explain how confident it is about certain fields
      3. Human review: A human can sanity check fields for confidence by annotating JSON output
   - Proposed Tool: [LangSmith](https://www.langchain.com/langsmith) is an observability and [evaluation](https://www.langchain.com/evaluation) platform for AI models. It works well with the LangChain ecosystem and lets us avoid the hassle of building and configuring UI
   - Other key metrics: extraction speed, per field confidence, overall confidence, error rate

---

## 🐛 Troubleshooting

#### OpenAI API key not found
- Ensure you have a `.env` file with your API key
- Check that `python-dotenv` is installed

#### JSON decode errors
- Usually means GPT returned malformed JSON
- Check your internet connection and API key validity
