import json
from pathlib import Path
from datasets import load_dataset

# Configuration: set your file paths here
INPUT_PATH = Path("textbook2.json")   # path to your original JSON or JSONL
OUTPUT_PATH = Path("txtbook2_Update.json")     # where the converted file will be written


def main():
    # Load the dataset using Hugging Face's datasets
    # If your file is JSONL or a JSON array, datasets will handle it automatically.
    ds = load_dataset(
        "json",
        data_files=str(INPUT_PATH),
        split="train"
    )

    out = []
    for entry in ds:
        # Extract raw prompt/response fields
        prompt = entry.get("prompt") or entry.get("input") or ""
        response = entry.get("response") or entry.get("output") or ""
        prompt = prompt.strip()
        response = response.strip()
        if not prompt or not response:
            continue

        # Build the chat-style dialogue
        dialogue = [
            {"from": "human", "value": prompt},
            {"from": "gpt",   "value": response}
        ]
        out.append({"dialogue": dialogue})

    # Write out the new dialogue-formatted JSON
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(out, indent=2))
    print(f"✔ Converted {len(out)} entries → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
