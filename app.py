from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pix2text import Pix2Text
from screenshot_tool import ScreenshotTool
import threading

app = Flask(__name__)

# Configure allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_equations(equations):
    if equations.startswith('\\begin{array}'):
        # Directly render the equation
        return equations
    elif '\n' not in equations.strip():
        # Single-line equation, wrap it in \[ \]
        return f'\\[ {equations} \\]'
    else:
        return equations

@app.route('/')
def index():
    snip()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    
    if file and allowed_file(file.filename):
        img_fp = 'uploads/' + secure_filename(file.filename)
        file.save(img_fp)

        try:
            p2t = Pix2Text()
            equations = p2t.recognize_formula(img_fp)
            processed_equations = process_equations(equations)
            return render_template('equations.html', equations=processed_equations)
        except Exception as e:
            return f'Error processing image: {str(e)}'

    return 'Invalid file format'

def snip():
    # Define a function to run the ScreenshotTool in a separate thread
    def run_screenshot_tool():
        screenshot_tool = ScreenshotTool()
        screenshot_tool.run()

    # Start the ScreenshotTool in a separate thread
    threading.Thread(target=run_screenshot_tool).start()

    return jsonify({'message': 'Screenshot tool initiated'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
