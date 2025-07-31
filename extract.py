import fitz  # PyMuPDF
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

def load_schema():
    """Load the schema from schema.json"""
    try:
        with open('schema.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  schema.json not found, using default schema")
        return None

class RecipeExtractor:
    def __init__(self):
        """Initialize the recipe extractor with LangChain components"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.output_parser = JsonOutputParser()
        
        # Load schema from file or use default
        schema = load_schema()
        if schema:
            # Convert schema to LangChain format
            self.recipe_schema = {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                    "chef": {"type": "string"},
                    "yield_count": {"type": "number"},
                    "allergens": {"type": "array", "items": {"type": "string"}},
                    "components": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string", "enum": ["protein", "starch", "vegetable", "sauce"]},
                                "prep_time_minutes": {"type": "number"},
                                "cook_time_minutes": {"type": "number"},
                                "cook_temp_fahrenheit": {"type": "number"},
                                "cook_method": {"type": "string"},
                                "portion_weight_grams": {"type": "number"},
                                "ingredients": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "amount_per_portion_grams": {"type": "number"}
                                        },
                                        "required": ["name", "amount_per_portion_grams"]
                                    }
                                }
                            },
                            "required": ["name", "type", "prep_time_minutes", "cook_time_minutes", "cook_temp_fahrenheit", "cook_method", "portion_weight_grams", "ingredients"]
                        }
                    }
                },
                "required": ["recipe_name", "chef", "yield_count", "allergens", "components"]
            }
        else:
            # Define the JSON schema for recipe output with new structure
            self.recipe_schema = {
                "type": "object",
                "properties": {
                    "recipe_name": {"type": "string"},
                    "chef": {"type": "string"},
                    "yield_count": {"type": "number"},
                    "allergens": {"type": "array", "items": {"type": "string"}},
                    "components": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string", "enum": ["protein", "starch", "vegetable", "sauce"]},
                                "prep_time_minutes": {"type": "number"},
                                "cook_time_minutes": {"type": "number"},
                                "cook_temp_fahrenheit": {"type": "number"},
                                "cook_method": {"type": "string"},
                                "portion_weight_grams": {"type": "number"},
                                "ingredients": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "amount_per_portion_grams": {"type": "number"}
                                        },
                                        "required": ["name", "amount_per_portion_grams"]
                                    }
                                }
                            },
                            "required": ["name", "type", "prep_time_minutes", "cook_time_minutes", "cook_temp_fahrenheit", "cook_method", "portion_weight_grams", "ingredients"]
                        }
                    }
                },
                "required": ["recipe_name", "chef", "yield_count", "allergens", "components"]
            }
        
        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a data extraction assistant for a food production company. You will receive raw text from a chef's PDF recipe. Parse it into structured JSON format.

IMPORTANT INSTRUCTIONS:
- Only return valid JSON that matches the specified schema
- Use your best judgment to infer missing information
- Use 0 for missing times, temperatures, or weights
- For component types, choose from: protein, starch, vegetable, sauce
- For allergens, identify common allergens like: dairy, eggs, fish, shellfish, tree nuts, peanuts, wheat, soy
- For cook methods, use descriptive terms like: bake, grill, sauté, steam, fry, roast, etc.
- For portion_weight_grams, estimate the final cooked weight per portion
- If yield_count is not specified, estimate based on typical portion sizes

CHEF NAME EXTRACTION:
- Look for chef names in the first few lines of the recipe
- Common patterns: "Chef [Name]", "[Name]'s [Recipe]", or recipe title followed by "Chef [Name]"
- Only extract chef names that are explicitly mentioned in the text
- If no chef name is found, use "Unknown Chef"
- Do NOT hallucinate or invent chef names that are not in the text
- Pay attention to multi-word names like "Jean-Pierre Dubois"

JSON Schema:
{json_schema}

Only return valid JSON. Do not include any explanatory text."""),
            ("human", "Please parse this recipe text into the specified JSON format:\n\n{recipe_text}")
        ])

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
        """Parse recipe text using LangChain and GPT-4"""
        try:
            # Create the chain
            chain = self.prompt_template | self.llm | self.output_parser
            
            # Run the chain
            result = chain.invoke({
                "json_schema": json.dumps(self.recipe_schema, indent=2),
                "recipe_text": text
            })
            
            return result
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
            # Validate the result
            if self.validate_recipe_data(result):
                return result
            else:
                print(f"Validation failed for {pdf_path}")
                return None
        else:
            print(f"Failed to parse recipe from {pdf_path}")
            return None

    def validate_recipe_data(self, data):
        """Basic validation of recipe data"""
        required_fields = ["recipe_name", "chef", "yield_count", "allergens", "components"]
        
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return False
        
        # Validate components
        components = data.get("components", [])
        if not components:
            print("No components found")
            return False
        
        for component in components:
            required_component_fields = ["name", "type", "prep_time_minutes", "cook_time_minutes", "cook_temp_fahrenheit", "cook_method", "portion_weight_grams", "ingredients"]
            for field in required_component_fields:
                if field not in component:
                    print(f"Missing required component field: {field}")
                    return False
        
        return True

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

    def print_recipe_summary(self, data):
        """Print a summary of the extracted recipe"""
        print(f"Recipe Name: {data.get('recipe_name', 'Unknown')}")
        print(f"Chef: {data.get('chef', 'Unknown')}")
        print(f"Yield: {data.get('yield_count', 0)} portions")
        
        allergens = data.get('allergens', [])
        if allergens:
            print(f"Allergens: {', '.join(allergens)}")
        else:
            print("Allergens: None identified")
        
        components = data.get('components', [])
        print(f"Components: {len(components)}")
        
        for i, component in enumerate(components, 1):
            print(f"  {i}. {component.get('name', 'Unknown')} ({component.get('type', 'unknown')})")
            print(f"     Prep: {component.get('prep_time_minutes', 0)}min, Cook: {component.get('cook_time_minutes', 0)}min")
            print(f"     Method: {component.get('cook_method', 'Unknown')}")
            print(f"     Portion weight: {component.get('portion_weight_grams', 0)}g")
            ingredients = component.get('ingredients', [])
            print(f"     Ingredients: {len(ingredients)} items")

def main():
    """Main function to process all recipes"""
    # Initialize the extractor
    extractor = RecipeExtractor()
    
    # Get all PDF files from sample-recipes directory
    pdf_dir = Path("sample-recipes")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in sample-recipes directory")
        return
    
    # Create output directory
    output_dir = Path("output")
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
            
            # Print summary
            extractor.print_recipe_summary(result)
        else:
            print(f"Failed to process {pdf_file.name}")
    
    # Print final summary
    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Successfully processed: {successful_extractions}/{total_files} files")
    print(f"Output files saved to: {output_dir}")
    print(f"{'='*60}")
    
    # Run validation if outputs exist
    if successful_extractions > 0:
        print("\n🔍 Running validation...")
        try:
            import subprocess
            subprocess.run(["python3", "validate_outputs.py"], check=True)
        except subprocess.CalledProcessError:
            print("⚠️  Validation script failed to run")
        except FileNotFoundError:
            print("⚠️  Validation script not found")

if __name__ == "__main__":
    main() 