# Demo: Recipe PDF to JSON Extraction

So what I've built here is a **Python-based solution** for extracting recipe data from a PDF file to a JSON file.

It's built with **GPT-5**, **Python**, and **PyMuPDF**.

---

Here are some raw recipe PDFs. As you can see, it's formatted for humans — inconsistent spacing, mixed units, and no strict structure.

I drop it into **`data/input/`** and run the extractor from the terminal (**`src/extract.py`**).

Behind the scenes, the pipeline:

1. Parses the PDF into text (PyMuPDF)  
2. Sends it to the model with the instructions in **`prompts/recipe_extraction_prompt.txt`**  
3. Forces the output into the structure defined in **`schema/schema.json`**  

Here's the generated JSON output in **`data/output/`**. You can see:

- **Ingredients** per component as name and amount per portion (grams)  
- **Components** with prep/cook times, cooking method, and portion weights  
- **Metadata** — recipe name, chef, yield, and allergens — captured consistently  

**`schema/schema.json`** acts as a **contract** — the output must conform to these required fields before it's accepted.

If validation fails, the run is **rejected** instead of silently passing malformed data downstream.

---

What's important is **consistency**. Here are three different recipes with very different formatting — and despite that variation, the output structure remains identical across all of them.

That consistency is what makes the system scalable.
