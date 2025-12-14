# 🤖 AI Code Documenter

**Automate your code documentation using AI.**

This tool takes a GitHub repository URL or a Zip file as input, analyzes every line of code using a Large Language Model (LLM), and inserts professional, non-vague docstrings and file headers. It preserves your logic exactly while explaining the "what" and "why" of your functions.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gradio](https://img.shields.io/badge/Frontend-Gradio-orange)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-8E75B2)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

* **📂 Dual Input Support:** Accepts public GitHub URLs or direct Zip file uploads.
* **🧠 Semantic Understanding:** Uses **Google Gemini 1.5 Flash** (with fallback to Pro) to understand complex logic, not just syntax.
* **🛡️ Logic Preservation:** Guaranteed to **only** add comments. Variable names, logic flow, and indentation remain untouched.
* **🌐 Language Agnostic:** Automatically detects programming languages (Python, JS, Java, C++, etc.) and applies the correct comment syntax.
* **🧹 Smart Filtering:** Automatically ignores non-code files (images, configs, binaries, `.git` folders) to save processing time.
* **⚡ Rate Limit Handling:** Built-in delays and retry logic to handle API limits gracefully.

---

## 🚀 Live Demo

**[Click here to view the Live App on Hugging Face Spaces](https://huggingface.co/spaces/AlenKAJi25/code-documenter)**



## 🛠️ Installation & Local Usage

To run this tool locally on your machine:

### 1. Clone the Repository


git clone [https://github.com/AlenKAji/Code-Documenter.git](https://github.com/AlenKAji/Code-Documenter.git)
<br>
cd Code-Documenter


### 2. Install Dependencies
```
pip install -r requirements.txt
```
Note: Ensure you have git installed on your system.

### 3. Set up Environment Variables
You need a Google Gemini API key. You can get one at Google AI Studio.

On Mac/Linux:
```
export GEMINI_API_KEY="your_api_key_here"
```
On Windows (PowerShell):
```
$env:GEMINI_API_KEY="your_api_key_here"
```
### 4. Run the App
```
python app.py
```
Open your browser and navigate to the local URL provided (usually http://127.0.0.1:7860).

--- 

## ⚙️ Configuration
The application automatically selects the best available model for your API key to avoid "404 Not Found" errors. It prioritizes models in this order:

- gemini-1.5-flash (Fastest & Cheapest)
- gemini-1.5-pro (Best Reasoning)
- gemini-pro (Legacy Fallback)

---

## 📁 Project Structure
```
Code-Documenter
      ├── app.py                 # Main application logic & Gradio UI
      ├── requirements.txt       # Python dependencies
      ├── README.md              # Project documentation
    
```
---

## 🛡️ Privacy & Safety Note
Code Transmission: Your code is sent to Google's Generative AI API for processing. Do not use this tool on sensitive, private, or proprietary codebases unless you are comfortable with Google's API Terms of Service.

No Storage: This tool processes files temporarily and deletes them after the session or when a new request is made. It does not permanently store your code on the hosting server.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

---

📄 License
Distributed under the MIT License. See LICENSE for more information.
