import fitz  # PyMuPDF
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI # Connects to OpenAI API
from langchain.prompts import ChatPromptTemplate # Structured prompts for LLMs
from langchain_core.output_parsers import JsonOutputParser # Parses JSON output from LLMs
from jsonschema import validate, ValidationError

# Load environment variables
load_dotenv()

class RecipeExtractor:
    def __init__(self, recipe_schema, prompt_template):
        """Initialize the recipe extractor with LangChain components"""
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.output_parser = JsonOutputParser()
        
        # Set schema and prompt template
        self.recipe_schema = recipe_schema
        self.prompt_template = prompt_template

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using PyMuPDF"""
        try:
            with fitz.open(pdf_path) as doc:
                text = "\n".join([page.get_text() for page in doc])
                return text.strip()
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return None

    def parse_recipe_text(self, text):
        """Parse recipe text using LangChain and GPT-4 with schema validation"""
        try:
            # Create the chain with schema validation
            chain = self.prompt_template | self.llm | self.output_parser
            
            # Prepare the input parameters
            input_params = {
                "json_schema": json.dumps(self.recipe_schema, indent=2),
                "recipe_text": text
            }
            
            # Run the chain with schema
            result = chain.invoke(input_params)
            
            # Validate the result against schema
            validate(instance=result, schema=self.recipe_schema)
            return result
        except ValidationError as e:
            print(f"Schema validation error: {e.message}")
            print(f"Path: {' -> '.join(str(p) for p in e.path)}")
            return None
        except Exception as e:
            print(f"Error parsing recipe text: {e}")
            return None

    def process_recipe(self, pdf_path):
        """Process a single recipe PDF"""
        print(f"Processing: {pdf_path}")
        
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            print(f"Failed to extract text from {pdf_path}")
            return None
        
        # Parse the recipe text
        result = self.parse_recipe_text(text)
        
        if result:
            return result
        else:
            print(f"Failed to parse recipe from {pdf_path}")
            return None

    def save_json_output(self, data, output_path):
        """Save JSON output to file"""
        try:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved output to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving output: {e}")
            return False


def main():
    """Main function to process all recipes"""
    # Load schema and prompt template
    try:
        with open('schema/schema.json', 'r') as f:
            recipe_schema = json.load(f)
    except FileNotFoundError:
        print("⚠️  schema.json not found, using default schema")
        recipe_schema = None
    
    try:
        with open('prompts/recipe_extraction_prompt.txt', 'r') as f:
            prompt_text = f.read()
    except FileNotFoundError:
        print("⚠️  recipe_extraction_prompt.txt not found")
        prompt_text = None
    
    if not prompt_text:
        raise FileNotFoundError("prompts/recipe_extraction_prompt.txt not found")
    
    # Create the prompt template using the loaded text with schema parameter
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("human", "{recipe_text}")
    ])

    # Initialize the extractor
    extractor = RecipeExtractor(recipe_schema, prompt_template)
    
    # Get all PDF files from data/input directory
    pdf_dir = Path("data/input")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in data/input directory")
        return
    
    # Create output directory
    output_dir = Path("data/output")
    output_dir.mkdir(exist_ok=True)
    
    # Process each PDF
    successful_extractions = 0
    total_files = len(pdf_files)
    
    for pdf_file in pdf_files:
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_file.name}")
        print(f"{'='*60}")
        
        # Process the recipe
        result = extractor.process_recipe(pdf_file)
        
        if result:
            # Save to JSON file
            output_file = output_dir / f"{pdf_file.stem}.json"
            if extractor.save_json_output(result, output_file):
                successful_extractions += 1
        else:
            print(f"Failed to process {pdf_file.name}")
    
    # Print final summary
    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Successfully processed: {successful_extractions}/{total_files} files")
    print(f"Output files saved to: {output_dir}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 