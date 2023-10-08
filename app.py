from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
import qrcode
import requests
import replicate

# pip install replicate

app = Flask(__name__)

# Dummy database (Replace with real database)
images = []

api_key = "r8_AOUWb0ow3k7nlSbHCmi0Ewn5VZr9DTP2zx8C7"  # Your actual API key
model_id = "ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"  # Your actual model ID

replicate_api_url = "https://api.replicate.ai/v1/models"
#print( Flask.url_for('/','static', filename='script1.js') )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/image/upload', methods=['POST'])
def upload_image():
    image_data = request.json['image']
    image_name = "cat.jpg"  # Replace with the actual image name
    image_decoded = base64.b64decode(image_data)
    image_np = np.frombuffer(image_decoded, dtype=np.uint8)
    image_cv = cv2.imdecode(image_np, flags=1)
    
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 100, 200)
    blurred = cv2.GaussianBlur(edges, (5, 5), 0)
    ret, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data('https://www.gofundme.com/')
    qr.make(fit=True)
    img_qr = qr.make_image(fill='black', back_color='white')
    
    pil_img = img_qr.convert('RGB')
    qr_np = np.array(pil_img)
    qr_cv = cv2.cvtColor(qr_np, cv2.COLOR_RGB2BGR)
    
    h, w, _ = image_cv.shape
    qr_resized = cv2.resize(qr_cv, (w, h))
    merged_image = cv2.addWeighted(image_cv, 0.5, qr_resized, 0.5, 0)
    
    _, img_encoded = cv2.imencode('.jpg', merged_image)
    image_base64 = base64.b64encode(img_encoded).decode('utf-8')
    
    # Define the prompt for the AI model
    ai_prompt = f"{image_name} process it to coloring book image with no colors"
    
    # replicate_data = {
    #     "input": {
    #         "image": image_base64,
    #         "prompt": ai_prompt  # Include the prompt here
    #     },
    #     "headers": {"Authorization": f"Token {api_key}"}
    # }
    # response = requests.post(f"{replicate_api_url}/{model_id}/run", json=replicate_data)
    # output = response.json()
    
    output = replicate.run(
    f"stability-ai/stable-diffusion:{model_id}",
     input= {
            "image": image_base64,
            "prompt": ai_prompt                                 # Include the prompt here
        },
    )
    print(output)

    processed_image_base64 = output.get('result', '')
    
    images.append(processed_image_base64)
    return jsonify({'message': 'Image uploaded and processed', 'processed_image': processed_image_base64}), 201

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(port=3000, debug=True)

