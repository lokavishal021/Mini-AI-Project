import os
from flask import Flask, request, jsonify, render_template
import datetime
import requests

app = Flask(__name__)

# --- Image Captioning Setup (lazy loading) ---
processor = None
model = None

def load_image_models():
    global processor, model
    if processor is None or model is None:
        try:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise

def get_image_caption(image):
    try:
        load_image_models()
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error generating caption: {str(e)}"

# --- Gemini AI Integration with Automatic Fallback & Extended Timeout ---
MODELS = ["gemini-flash-lite-latest", "gemini-flash-latest"]

def call_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Sorry, I didn't understand that. (Please configure your GEMINI_API_KEY)"

    system_instruction = "You are OmniBot, an intelligent and professional AI assistant created for a DevOps and Cloud Automation project. Provide accurate, well-explained responses and format all code snippets with proper markdown syntax highlighting."
    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"parts": [{"text": prompt}]}]
    }

    last_error = ""
    for model_name in MODELS:
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            # 10s connect, 60s read timeout to allow full token generation
            response = requests.post(api_url, json=payload, timeout=(10, 60))
            if response.status_code == 200:
                result = response.json()
                candidates = result.get('candidates', [])
                if candidates and 'content' in candidates[0] and 'parts' in candidates[0]['content']:
                    return candidates[0]['content']['parts'][0]['text'].strip()
            else:
                last_error = f"{model_name} status {response.status_code}"
                continue
        except Exception as e:
            last_error = f"{model_name} exception: {str(e)}"
            continue

    return f"Sorry, I encountered an issue contacting the AI model. Details: {last_error}"

# --- Assistant Logic ---
def assistant_logic(send):
    data_btn = send.lower().strip()

    # GUI Triggers
    if "open youtube" in data_btn:
        return "OPEN_YOUTUBE"
    elif "open google" in data_btn:
        return "OPEN_GOOGLE"
    elif "open facebook" in data_btn:
        return "OPEN_FACEBOOK"
    elif "open sbtet" in data_btn:
        return "OPEN_SBTET"
    elif "open music" in data_btn:
        return "OPEN_MUSIC"
    elif "shutdown" in data_btn or "quit" in data_btn:
        return "Ok sir. Shutting down."
    elif "time now" in data_btn or "what time" in data_btn:
        now = datetime.datetime.now()
        return now.strftime("Current time is %I:%M %p")

    # Everything else routed to Gemini
    return call_gemini(send)

# --- File Reading Functions ---
def read_pdf_file(file):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def read_docx_file(file):
    try:
        import docx
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def read_txt_file(file):
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

# --- Routes ---
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file') or request.files.get('image')
    if file:
        filename = file.filename.lower()
        try:
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')): 
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(file.read()))
                caption = get_image_caption(img)

                weapons = ["gun", "knife", "pistol", "bomb", "rifle"]
                detected_weapons = [weapon for weapon in weapons if weapon in caption.lower()]

                if detected_weapons:
                    caption = f"⚠️ Warning: Possible weapon detected ({', '.join(detected_weapons)}).\n" + caption

                return jsonify({"caption": caption})

            elif filename.endswith('.pdf'):
                content = read_pdf_file(file)
                return jsonify({"type": "text", "result": content})
            elif filename.endswith('.docx'):
                content = read_docx_file(file)
                return jsonify({"type": "text", "result": content})
            elif filename.endswith('.txt'):
                content = read_txt_file(file)
                return jsonify({"type": "text", "result": content})
            else:
                return jsonify({"status": "error", "message": "Unsupported file type"})
        
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    
    return jsonify({"status": "no file uploaded"})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    reply = assistant_logic(user_message)
    return jsonify({"reply": reply})

@app.route("/test")
def test():
    return "Flask server is running!"

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Flask Virtual Assistant...")
    print("=" * 50)
    print(f"Server will start at: http://127.0.0.1:5000/")
    print("Press CTRL+C to quit")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)