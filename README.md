# Recipe Extraction Challenge

A Python-based solution for extracting structured recipe data from PDF files using GPT-4 and PyMuPDF, optimized for food production workflows.

## 🚀 Features

- **PDF Text Extraction**: Uses PyMuPDF to extract text from recipe PDFs
- **AI-Powered Parsing**: Leverages GPT-4 via LangChain to convert unstructured text into structured JSON
- **Production-Focused Output**: Extracts recipe components, allergens, chef info, and yield counts
- **Component-Based Structure**: Organizes recipes by protein, starch, vegetable, and sauce components
- **Batch Processing**: Processes multiple PDF files automatically
- **Structured Output**: Generates clean JSON files for each recipe
- **Anti-Hallucination Measures**: Improved prompts to avoid AI hallucination of chef names

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for GPT-4 API calls

## 🛠️ Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   - Copy `env_example.txt` to `.env`
   - Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   - Get your API key from: https://platform.openai.com/api-keys

## 🎯 Usage

### Basic Usage

Run the extraction script to process all PDFs in the `sample-recipes` directory:

```bash
python extract.py
```

### What it does:

1. **Scans** the `sample-recipes` directory for PDF files
2. **Extracts** text from each PDF using PyMuPDF
3. **Parses** the text using GPT-4 via LangChain into structured JSON
4. **Saves** results to the `output` directory
5. **Displays** a summary of each processed recipe

### Output Structure

Each recipe generates a JSON file with this production-focused structure:

```json
{
  "recipe_name": "string",
  "chef": "string",
  "yield_count": "number",
  "allergens": ["array of strings"],
  "components": [
    {
      "name": "string",
      "type": "protein|starch|vegetable|sauce",
      "prep_time_minutes": "number",
      "cook_time_minutes": "number",
      "cook_temp_fahrenheit": "number (if applicable)",
      "cook_method": "string",
      "portion_weight_grams": "number (final weight per container)",
      "ingredients": [
        {
          "name": "string",
          "amount_per_portion_grams": "number"
        }
      ]
    }
  ]
}
```

## 📁 Project Structure

```
recipe-extraction-challenge/
├── sample-recipes/          # Input PDF files
│   ├── recipe_1_teriyaki_chicken.pdf
│   ├── recipe_2_beef_barbacoa.pdf
│   └── recipe_3_mediterranean_salmon.pdf
├── output/                  # Generated JSON files (created automatically)
├── extract.py              # Main extraction script (LangChain + GPT-4)
├── requirements.txt         # Python dependencies
├── env_example.txt         # Environment variables template
└── README.md              # This file
```

## 🤖 AI Tools Used

- **GPT-4 via LangChain**: For intelligent parsing of unstructured recipe text
- **PyMuPDF**: For reliable PDF text extraction
- **Custom Prompt Engineering**: Optimized prompts for production-focused recipe parsing
- **Anti-Hallucination Measures**: Improved prompts to avoid AI inventing chef names

## 📊 Accuracy Notes

### What works well:
- ✅ Structured PDFs with clear formatting
- ✅ Production recipes with component breakdowns
- ✅ Explicit ingredient amounts and cooking methods
- ✅ Clear yield counts and portion information
- ✅ Accurate chef name extraction (no hallucination)

### What's challenging:
- ⚠️ Handwritten or poorly scanned PDFs
- ⚠️ Unconventional recipe formats
- ⚠️ Missing allergen information (defaults to common allergens)
- ⚠️ Ambiguous component classifications

## 🔧 Assumptions

- **Missing data**: Times/temperatures default to 0 if not found
- **Allergens**: Common allergens (soy, wheat) are identified when present
- **Component types**: Classified as protein, starch, vegetable, or sauce
- **Portion weights**: Estimated based on ingredient amounts and cooking methods
- **Yield counts**: Extracted from PDF or estimated based on typical portion sizes
- **Chef names**: Only extracted from explicit mentions in text (no hallucination)

## 🚀 Future Improvements

### +2 Hours Enhancements:
- Add allergen detection algorithms
- Implement component type validation
- Add nutritional information calculation
- Improve portion weight estimation

### +2 Weeks Features:
- Fine-tune custom GPT model on production recipe data
- Build web UI for upload + review + correction
- Add error classification and correction suggestions
- Implement confidence scoring for each field

### Production Scale:
- AWS Lambda queue processing
- Human-in-the-loop review system
- Structured data validation layer
- Analytics dashboard for parsing confidence

## 💡 Demo Script for Loom

1. **Show project structure** - Display the folder with 3 sample PDFs
2. **Run the script** - Execute `python extract.py` in terminal (requires API key)
3. **Show real-time processing** - Watch as each PDF is processed
4. **Display results** - Show the generated JSON files in output folder
5. **Highlight accuracy** - Point out what was extracted correctly vs. assumptions made
6. **Discuss limitations** - Mention any parsing challenges or missing data

## 🐛 Troubleshooting

### Common Issues:

**"No module named 'fitz'"**
```bash
pip install PyMuPDF
```

**"OpenAI API key not found"**
- Ensure you have a `.env` file with your API key
- Check that `python-dotenv` is installed

**"JSON decode error"**
- This usually means GPT returned malformed JSON
- Check your internet connection
- Verify your OpenAI API key is valid

**"LangChain import errors"**
- Update to the latest LangChain version
- Check that all dependencies are installed correctly

## 📝 License

This project is created for the CookUnity recipe extraction challenge.

---

**Ready to extract some recipes?** 🍳

1. Set up your API key
2. Run `python extract.py`
3. Check the `output` folder for your structured recipe data! 