import os
import shutil
import zipfile
import time
from git import Repo
import google.generativeai as genai
import gradio as gr

# --- 1. CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in Secrets. Please add it in Settings.")

genai.configure(api_key=API_KEY)

# --- ROBUST MODEL SELECTION ---
# This fixes the 404 error by asking the API "What models do you have?" first.
try:
    print("🔍 Checking available models...")
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    print(f"   Found: {available_models}")

    # Priority list
    if 'models/gemini-1.5-flash' in available_models:
        model_name = 'gemini-1.5-flash'
    elif 'models/gemini-1.5-pro' in available_models:
        model_name = 'gemini-1.5-pro'
    elif 'models/gemini-pro' in available_models:
        model_name = 'gemini-pro'
    else:
        model_name = available_models[0] # Fallback to whatever is there
        
    print(f"✅ Selected Model: {model_name}")
    model = genai.GenerativeModel(model_name)
    
except Exception as e:
    print(f"❌ Critical Error configuring model: {e}")
    # Fallback for very old libraries if update fails
    model = genai.GenerativeModel('gemini-pro')

# --- 2. CORE LOGIC ---
IGNORE_EXTENSIONS = {
    '.txt', '.md', '.json', '.xml', '.yaml', '.yml', '.csv', '.html', '.css',
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.svg',
    '.lock', '.gitignore', '.dockerignore', '.env', '.map'
}

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', 'env', '.idea', '.vscode', 'build', 'dist', 'bin'}

def is_code_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext not in IGNORE_EXTENSIONS and len(ext) > 1

def generate_documented_code(code_content, file_path):
    extension = os.path.splitext(file_path)[1]
    prompt = f"""
    You are a Senior Software Architect. Add professional documentation to this code.
    RULES:
    1. Detect language from '{extension}'.
    2. Add a file header summary.
    3. Add docstrings before functions/classes.
    4. Explain 'WHAT' and 'WHY' (non-vague).
    5. PRESERVE LOGIC EXACTLY.
    6. OUTPUT: Raw code only. No Markdown blocks.
    
    CODE:
    {code_content}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Cleanup Markdown
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            text = "\n".join(lines)
        return text
    except Exception as e:
        print(f"⚠️ API Error on {file_path}: {e}")
        return code_content

def process_directory(input_dir):
    file_count = 0
    for root, dirs, files in os.walk(input_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if is_code_file(file):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if not content.strip() or len(content) > 100000: continue

                    documented = generate_documented_code(content, file)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(documented)
                    
                    file_count += 1
                    time.sleep(1) # Rate limiting
                except Exception as e:
                    print(f"Failed {file}: {e}")
    return file_count

def zip_directory(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

# --- 3. GRADIO INTERFACE ---
def document_project(github_url, zip_file):
    base_dir = "working_dir"
    input_dir = os.path.join(base_dir, "input")
    output_zip = os.path.join(base_dir, "documented_project.zip")
    
    # Cleanup and Setup
    if os.path.exists(base_dir): shutil.rmtree(base_dir)
    os.makedirs(input_dir)
    
    try:
        status_msg = ""
        if zip_file is not None:
            with zipfile.ZipFile(zip_file.name, 'r') as zip_ref:
                zip_ref.extractall(input_dir)
            status_msg = "Extracted Zip."
        elif github_url:
            Repo.clone_from(github_url, input_dir)
            status_msg = "Cloned GitHub Repo."
        else:
            return None, "Please provide a Link or Zip file."

        print("🚀 Starting AI processing...")
        count = process_directory(input_dir)
        
        print("💾 Zipping...")
        zip_directory(input_dir, output_zip)
        
        return output_zip, f"✅ Success! {count} files documented. Download below."

    except Exception as e:
        return None, f"Error: {str(e)}"

# UI Layout
with gr.Blocks(title="Auto-Doc Helper") as demo:
    gr.Markdown("# 🤖 AI Code Documenter")
    gr.Markdown("Upload a project to add professional docstrings automatically.")
    
    with gr.Row():
        gh_input = gr.Textbox(label="GitHub URL")
        zip_input = gr.File(label="Upload Zip", file_types=['.zip'])
    
    submit_btn = gr.Button("Generate Docs", variant="primary")
    output = gr.File(label="Download Result")
    status = gr.Textbox(label="Status")

    submit_btn.click(fn=document_project, inputs=[gh_input, zip_input], outputs=[output, status])

if __name__ == "__main__":
    demo.launch()