from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
import qrcode
import requests
import replicate

app = Flask(__name__)

# Dummy database (Replace with real database)
images = []

api_key = "r8_AOUWb0ow3k7nlSbHCmi0Ewn5VZr9DTP2zx8C7"  # Your actual API key
model_id = "ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"  # Your actual model ID

replicate_api_url = "https://api.replicate.ai/v1/models"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/image/upload', methods=['POST'])
def upload_image():
    output = []
    try:
        print("Step 1: Start")
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
        ai_prompt = f"Convert the sketch of {image_name} into a coloring book image without colors."

        output = replicate.run(
        f"stability-ai/stable-diffusion:{model_id}",
        input={
                "image": image_base64,
                "prompt": ai_prompt
            },
        )
        print(output)

        processed_image_url = output[0] if output else ''  # Use the first URL if available

        images.append(processed_image_url)
        print("Step 2: Image processed")
        return jsonify({'message': 'Image uploaded and processed', 'processed_image': processed_image_url}), 201

    except Exception as e:
        print("Exception occurred:", e)
        return jsonify({'error': str(e)}), 500

# print("Output from Replicate: ", output)

@app.route('/favicon.ico')
def favicon():
    return '', 204
# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
