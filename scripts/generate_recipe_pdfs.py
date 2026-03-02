"""
Generate sample recipe PDFs with the same structure as the originals
but different recipes and chef names. Uses PyMuPDF (fitz) with bold headings
and "- " bullets (no special characters that render as ?).
"""
import fitz
from pathlib import Path

MARGIN = 50
FONTSIZE = 10
LINE_HEIGHT = 13
PAGE_WIDTH = 595
PAGE_HEIGHT = 842


def _is_heading(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    # Title line (recipe + chef), section headers, component names, "Ingredients per portion"
    if "Chef " in s and len(s) < 80:
        return True
    if s.isupper() and len(s) < 50:  # COMPONENTS:, PORTIONING:, etc.
        return True
    if s.endswith(":") and len(s) < 45:  # "Ingredients per portion:", "Yield:"
        return True
    if "(" in s and ")" in s and any(x in s for x in ["Protein", "Starch", "Veg", "Sauce"]):
        return True
    if s.startswith("PROTEIN:") or s.startswith("STARCH:") or s.startswith("VEGETABLE:") or s.startswith("SAUCE:"):
        return True
    if s in ("Allergens", "FINAL PORTIONS:", "Assembly per container:") or s.startswith("Allergens:") or s.startswith("ALLERGENS:"):
        return True
    return False


def _add_page_from_text(doc: fitz.Document, text: str) -> None:
    """Add a page to doc with formatted text: bold headings, normal body, bullets as '- '."""
    text = text.replace("●", "- ")  # avoid ? from unsupported character
    lines = text.split("\n")
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    y = MARGIN
    x0 = MARGIN
    x1 = PAGE_WIDTH - MARGIN
    for line in lines:
        line = line.strip()
        if not line or line.startswith("-- ") and " of " in line and " --" in line:
            continue
        is_heading = _is_heading(line)
        fontname = "helv"
        fontsize = 12 if is_heading else FONTSIZE
        rect = fitz.Rect(x0, y, x1, y + 40)
        overflow = page.insert_textbox(rect, line, fontsize=fontsize, fontname=fontname, align=fitz.TEXT_ALIGN_LEFT)
        if overflow < 0:
            # Text didn't fit; advance by one line and retry (truncate or allow overflow)
            y += LINE_HEIGHT
        else:
            used = rect.height - overflow
            y += max(LINE_HEIGHT, used)
        if y > PAGE_HEIGHT - MARGIN - 20:
            break


def text_to_pdf(text: str, output_path: Path) -> None:
    """Write multi-page PDF from text, splitting on '-- N of M --' page markers."""
    doc = fitz.open()
    page_marker = "\n-- "
    parts = text.split(page_marker)
    current = parts[0].strip()
    if current:
        _add_page_from_text(doc, current)
    for i in range(1, len(parts)):
        block = parts[i]
        if " --" in block:
            _, rest = block.split(" --", 1)
            current = rest.strip()
        else:
            current = block.strip()
        if current:
            _add_page_from_text(doc, current)
    doc.save(output_path)
    doc.close()


# --- Recipe 1 ---
RECIPE_1 = """Thai Basil Pork Bowl Chef Kenji Tanaka
Yield: 90 portions
COMPONENTS:
Pork (Protein)
- Prep Time: 12 min
- Cook Time: 10 min @ high heat
- Method: Slice, stir-fry in wok
Ingredients per portion:
- Pork shoulder, thinly sliced: 100g
- Thai basil: 8g
- Garlic, minced: 3g
- Vegetable oil: 5g
Jasmine Rice (Starch)
- Prep Time: 5 min
- Cook Time: 18 min
- Method: Steam
Ingredients per portion:
- Jasmine rice, dry: 70g
- Water: 140g
- Salt: 1g
Stir-Fried Green Beans (Veg)
- Prep Time: 15 min
- Cook Time: 6 min
- Method: Wok-fry
Ingredients per portion:
- Green beans: 50g
- Red bell pepper, sliced: 25g
- Oyster sauce: 8g
- Vegetable oil: 3g

-- 1 of 2 --

Spicy Lime Sauce (Sauce)
- Prep Time: 5 min
- Cook Time: 2 min
- Method: Mix, no cook
Ingredients per portion:
- Fish sauce: 12g
- Lime juice: 10g
- Sugar: 6g
- Chili flakes: 1g
PORTIONING:
- Pork: 115g
- Rice: 185g
- Vegetables: 90g
- Sauce: 30g
Allergens: Fish, Soy"""

# --- Recipe 2 ---
RECIPE_2 = """Priya's Coconut Curry Vegetable Bowls
Makes about 75–85 portions depending on serving size
The Curry: Sauté 2 cups diced onion, 4 tbsp ginger-garlic paste, then add 3 lbs chopped tomatoes. Toast your spices — 4 tbsp curry powder, 2 tbsp garam masala, 1 tbsp turmeric. Add 2 large cans coconut milk and simmer 25 min. Each portion gets about 180g curry.
For the Basmati Rice: Rinse 5 kg basmati, cook with cardamom and a pinch of salt. Per portion you need 80g cooked rice. Fluff and keep warm.
Roasted Chickpeas: Drain and roast 4 kg chickpeas with cumin, coriander, and a little oil at 400°F for 20 min. Each portion: 60g chickpeas.
The Raita: Whisk 2 kg yogurt with grated cucumber (squeezed), mint, salt, and a pinch of cumin. Portion 40g per bowl.
Assembly per container:
- Curry: 180g
- Rice: 80g
- Chickpeas: 60g
- Raita: 40g
- Top with 10g cilantro and 5g toasted coconut!

-- 1 of 1 --"""

# --- Recipe 3 ---
RECIPE_3 = """Pan-Seared Halibut with Spring Vegetables Chef Yuki Nakamura
Production Yield: 100 portions
COMPONENT BREAKDOWN:
PROTEIN: Pan-Seared Halibut Prep: Pat dry, season
Cook: 6 min per side @ medium-high
Internal Temp: 145°F
Base Ingredients (per portion):
- Halibut fillet: 130g
- Olive oil: 5g
- Lemon juice: 5g
- Kosher salt: 1.5g
- Black pepper: 0.5g
- Fresh dill: 2g
STARCH: Garlic Mashed Potatoes Prep: Peel, quarter
Cook: 20 min boil, mash
Per Portion:
- Russet potatoes: 150g
- Butter: 10g
- Garlic, roasted: 3g
- Cream: 15g
- Salt: 1g
VEGETABLE: Sautéed Spring Vegetables Prep: Trim, cut uniform
Cook: 6 min sauté
Per Portion:
- Asparagus: 40g
- Peas: 25g
- Fennel, sliced: 20g

-- 1 of 2 --

- Olive oil: 4g
- Lemon zest: 0.5g
SAUCE: Brown Butter Caper Sauce Prep: Reduce, whisk
Per Portion:
- Butter: 12g
- Capers: 5g
- Lemon juice: 4g
- Parsley, chopped: 2g
FINAL PORTIONS:
- Halibut: 140g
- Mashed potatoes: 180g
- Spring vegetables: 90g
- Sauce: 25g
ALLERGENS: Fish, Dairy"""


def main():
    project_root = Path(__file__).parent.parent
    input_dir = project_root / "data" / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    recipes = [
        (RECIPE_1, "recipe_1_thai_basil_pork.pdf"),
        (RECIPE_2, "recipe_2_coconut_curry_vegetable.pdf"),
        (RECIPE_3, "recipe_3_halibut_spring_vegetables.pdf"),
    ]
    for text, filename in recipes:
        out = input_dir / filename
        text_to_pdf(text, out)
        print(f"Wrote {out}")

    old_names = [
        "recipe_1_teriyaki_chicken.pdf",
        "recipe_2_beef_barbacoa.pdf",
        "recipe_3_mediterranean_salmon.pdf",
    ]
    for name in old_names:
        path = input_dir / name
        if path.exists():
            path.unlink()
            print(f"Removed {path}")


if __name__ == "__main__":
    main()
