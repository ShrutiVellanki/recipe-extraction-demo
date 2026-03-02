## 👋 Welcome

I'm **Shruti**, a Toronto-based **Software Engineer**. 👩‍💻 

This is a showcase of an AI-driven workflow that takes chaotic, human-written recipes and transforms them into clean, validated data—fueling food operations at scale.

---

## ⚙️ Workflow Snapshot

- **Python app** that extracts recipe data from PDF to JSON
- Powered by **GPT-5**, **Python**, **PyMuPDF**

| Step            | Description                                                                              |
| --------------- | ---------------------------------------------------------------------------------------- |
| **1. Input**    | Drop messy recipe PDFs in `data/input`                                                   |
| **2. Extract**  | Run `src/extract.py` from the terminal                                                   |
| **3. Parse**    | Convert PDF content to raw text using `PyMuPDF`                                          |
| **4. AI Pass**  | Send the text (plus prompts) to the AI for extraction                                    |
| **5. Structure**| Enforce output to fit `schema.json`                                                      |
| **6. Output**   | Get clean JSON with detailed components in `data/output/`                                |
| **7. Validate** | Everything checked against the schema contract; non-conforming outputs are rejected      |

**Output consistency**—even with messy inputs—is what unlocks true operational scale.

---

## 💡 Value at a Glance

| Challenge / Stage                  | Description                                                                                      |
| ---------------------------------- | ------------------------------------------------------------------------------------------------ |
| **🗂️ Legacy Pain**                 | Slow, inconsistent manual entry. Scaling requires standardization and normalization.              |
| **⚡ Solution**                     | AI + schema validation = reliable, structured data for nutrition, costing, production—at scale.  |
| **🤖 AI's Role**                    | Parse unstructured input, enforce structure, and increase throughput at scale.  |
| **❓ First Failure: Ambiguity**     | Ambiguities (missing data, poor formatting, images) compound; automation unchecked is risky.      |
| **🕵️ Human Review: Uncertainty**   | Humans review edge cases, supervise low-confidence output (human-in-the-loop).                    |
| **👨‍🍳 Human Review: Taste**        | Flavor, substitutions, and rollout decisions always remain human-led.                             |
