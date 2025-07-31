#!/usr/bin/env python3
"""
Validation script to test output JSON files against the schema
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List

def load_schema() -> Dict[str, Any]:
    """Load the schema from schema.json"""
    try:
        with open('schema.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ schema.json not found!")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing schema.json: {e}")
        return {}

def validate_field_type(value: Any, expected_type: str) -> bool:
    """Validate if a field matches the expected type"""
    if expected_type == "string":
        return isinstance(value, str)
    elif expected_type == "number":
        return isinstance(value, (int, float))
    elif expected_type == "array of strings":
        return isinstance(value, list) and all(isinstance(item, str) for item in value)
    elif expected_type == "protein|starch|vegetable|sauce":
        return isinstance(value, str) and value in ["protein", "starch", "vegetable", "sauce"]
    else:
        return True  # Unknown type, assume valid

def validate_component(component: Dict[str, Any]) -> List[str]:
    """Validate a single component"""
    errors = []
    
    # Required fields for components
    required_fields = {
        "name": "string",
        "type": "protein|starch|vegetable|sauce",
        "prep_time_minutes": "number",
        "cook_time_minutes": "number",
        "cook_temp_fahrenheit": "number",
        "cook_method": "string",
        "portion_weight_grams": "number",
        "ingredients": "array"
    }
    
    for field, expected_type in required_fields.items():
        if field not in component:
            errors.append(f"Missing required field: {field}")
        elif field == "ingredients":
            if not isinstance(component[field], list):
                errors.append(f"ingredients must be an array")
            else:
                # Validate each ingredient
                for i, ingredient in enumerate(component[field]):
                    if not isinstance(ingredient, dict):
                        errors.append(f"ingredient {i} must be an object")
                    else:
                        if "name" not in ingredient:
                            errors.append(f"ingredient {i} missing 'name' field")
                        if "amount_per_portion_grams" not in ingredient:
                            errors.append(f"ingredient {i} missing 'amount_per_portion_grams' field")
                        elif not isinstance(ingredient["amount_per_portion_grams"], (int, float)):
                            errors.append(f"ingredient {i} amount_per_portion_grams must be a number")
        elif not validate_field_type(component[field], expected_type):
            errors.append(f"Field '{field}' has wrong type. Expected {expected_type}, got {type(component[field]).__name__}")
    
    return errors

def validate_recipe_data(data: Dict[str, Any]) -> List[str]:
    """Validate a recipe JSON against the schema"""
    errors = []
    
    # Required top-level fields
    required_fields = {
        "recipe_name": "string",
        "chef": "string", 
        "yield_count": "number",
        "allergens": "array of strings",
        "components": "array"
    }
    
    # Check required fields exist and have correct types
    for field, expected_type in required_fields.items():
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif field == "components":
            if not isinstance(data[field], list):
                errors.append("components must be an array")
            else:
                # Validate each component
                for i, component in enumerate(data[field]):
                    if not isinstance(component, dict):
                        errors.append(f"component {i} must be an object")
                    else:
                        component_errors = validate_component(component)
                        errors.extend([f"component {i}: {error}" for error in component_errors])
        elif not validate_field_type(data[field], expected_type):
            errors.append(f"Field '{field}' has wrong type. Expected {expected_type}, got {type(data[field]).__name__}")
    
    return errors

def validate_output_file(file_path: Path) -> Dict[str, Any]:
    """Validate a single output file"""
    print(f"\n🔍 Validating: {file_path.name}")
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"valid": False, "errors": ["File not found"]}
    except json.JSONDecodeError as e:
        return {"valid": False, "errors": [f"Invalid JSON: {e}"]}
    
    errors = validate_recipe_data(data)
    
    if errors:
        return {"valid": False, "errors": errors}
    else:
        return {"valid": True, "errors": []}

def main():
    """Main validation function"""
    print("🧪 Recipe Output Validation")
    print("=" * 50)
    
    # Load schema
    schema = load_schema()
    if not schema:
        print("❌ Cannot proceed without valid schema")
        return
    
    print("✅ Schema loaded successfully")
    
    # Find output files
    output_dir = Path("output")
    if not output_dir.exists():
        print("❌ Output directory not found")
        return
    
    json_files = list(output_dir.glob("*.json"))
    if not json_files:
        print("❌ No JSON files found in output directory")
        return
    
    print(f"📁 Found {len(json_files)} JSON files to validate")
    
    # Validate each file
    results = []
    for json_file in json_files:
        result = validate_output_file(json_file)
        results.append((json_file.name, result))
    
    # Print results
    print(f"\n{'='*60}")
    print("VALIDATION RESULTS")
    print(f"{'='*60}")
    
    valid_count = 0
    total_count = len(results)
    
    for filename, result in results:
        if result["valid"]:
            print(f"✅ {filename}: VALID")
            valid_count += 1
        else:
            print(f"❌ {filename}: INVALID")
            for error in result["errors"]:
                print(f"   - {error}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {valid_count}/{total_count} files are valid")
    
    if valid_count == total_count:
        print("🎉 All outputs match the schema!")
    else:
        print("⚠️  Some outputs need to be fixed")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 