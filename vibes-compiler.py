import subprocess
import sys
import os
from pathlib import Path
from google import genai

KEY_FILE = Path.home() / ".vibes_api_key"

def load_api_key():
    if KEY_FILE.exists():
        key = KEY_FILE.read_text().strip()
        if key:
            return key

    print("[VIBES] No API key found.")
    key = input("Enter your Gemini API key: ").strip()

    if not key:
        print("[VIBES] Error: No key entered.")
        sys.exit(1)

    KEY_FILE.write_text(key)
    print(f"[VIBES] API key saved to {KEY_FILE}")

    return key


def compile_vibes(source_path):
    api_key = load_api_key()

    client = genai.Client(api_key=api_key)

    with open(source_path, "r", encoding="utf-8") as f:
        vibes_code = f.read()

    prompt = f"""
    You are the compiler for the Vibes Programming Language (VPL).
    Convert the following Vibes code into valid Python code.
    Only output Python code, no explanations.

    Vibes code:
    {vibes_code}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    generated_code = response.text

    out_file = "out.py"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"[VIBES] Code generated → {out_file}")
    return out_file


def run_compiled(path):
    subprocess.run(["python", path])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: vibes-compiler.py <file.vibe>")
        sys.exit(1)

    src = sys.argv[1]
    out = compile_vibes(src)
    run_compiled(out)
