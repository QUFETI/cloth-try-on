from flask import Flask, request, jsonify, render_template
import cv2
import requests
from io import BytesIO
import base64

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/preds", methods=['POST'])
def submit():
    cloth = request.files['cloth']
    model = request.files['model']

    # Read the cloth and model images using cv2
    cloth_img = cv2.imdecode(np.fromstring(cloth.read(), np.uint8), cv2.IMREAD_COLOR)
    model_img = cv2.imdecode(np.fromstring(model.read(), np.uint8), cv2.IMREAD_COLOR)

    # Perform image processing using cv2 functions
    # ...
    # Your image processing code using cv2 goes here

    # Convert the processed image to PIL format
    op_pil = Image.fromarray(processed_img)

    # Convert the processed image to base64 format
    buffer = BytesIO()
    op_pil.save(buffer, 'PNG')
    buffer.seek(0)
    data = base64.b64encode(buffer.getvalue()).decode()

    # Replace the ngrok URL with your own ngrok URL or the URL of the API endpoint
    api_url = "http://f797-34-67-122-113.ngrok-free.app/api/transform"
    print("sending")

    # Create multipart form-data for the POST request
    files = {
        "cloth": ("cloth.jpg", cloth, "image/jpeg"),
        "model": ("model.jpg", model, "image/jpeg")
    }

    # Send a POST request to the API endpoint with the cloth and model images
    response = requests.post(api_url, files=files)
    response.raise_for_status()  # Check if the request was successful

    # Get the processed image from the response
    op = Image.open(BytesIO(response.content))

    # Convert the processed image to base64 format
    buffer = BytesIO()
    op.save(buffer, 'PNG')
    buffer.seek(0)
    data = base64.b64encode(buffer.getvalue()).decode()

    return render_template('index.html', op=data)

if __name__ == '__main__':
    app.run(port=5000)
