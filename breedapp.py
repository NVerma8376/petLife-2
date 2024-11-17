import base64
from flask import Flask, request, render_template_string
from breed import predict_breed_from_base64  # Directly import the function

app = Flask(__name__)

# Route to display the upload form
@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dog Breed Prediction</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background-color: #f7f7ff;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    max-width: 700px;
                    margin: 50px auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }
                h1 {
                    color: #a26fff;
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    font-weight: 600;
                }
                .file-input-wrapper {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-bottom: 20px;
                }
                input[type="file"] {
                    display: none;
                }
                label {
                    background-color: #a26fff;
                    color: white;
                    padding: 15px 30px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1.2em;
                    transition: background-color 0.3s ease;
                }
                label:hover {
                    background-color: #d7b8ff;
                }
                input[type="submit"] {
                    background-color: #a26fff;
                    color: white;
                    padding: 15px 30px;
                    border-radius: 8px;
                    border: none;
                    cursor: pointer;
                    font-size: 1.2em;
                    margin-top: 20px;
                    width: 200px;
                    transition: background-color 0.3s ease;
                }
                input[type="submit"]:hover {
                    background-color: #d7b8ff;
                }
                .file-name {
                    margin-top: 10px;
                    font-size: 1.1em;
                    color: #555;
                }
                .result {
                    margin-top: 30px;
                    text-align: center;
                    padding: 20px;
                    background-color: #d7b8ff;
                    border: 1px solid #a26fff;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    display: none;
                    color: #333;
                }
                .result img {
                    width: 100%;
                    max-width: 400px;
                    height: auto;
                    object-fit: contain;
                    margin-bottom: 15px;
                    border-radius: 8px;
                }
                .error {
                    color: #e74c3c;
                    text-align: center;
                    font-size: 1.2em;
                    margin-top: 20px;
                }
                footer {
                    text-align: center;
                    margin-top: 50px;
                    font-size: 0.9em;
                    color: #777;
                }
                footer a {
                    color: #777;
                    text-decoration: none;
                    font-weight: 600;
                }
                footer a:hover {
                    color: #a26fff;
                }
            </style>
            <script>
                // JavaScript to show the chosen file name after selection
                function showFileName(input) {
                    var fileName = input.files[0].name;
                    document.getElementById("file-name-display").innerText = fileName;
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Upload Image for Dog Breed Prediction</h1>
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <div class="file-input-wrapper">
                        <input type="file" name="image" accept="image/*" id="file-input" required onchange="showFileName(this)">
                        <label for="file-input">Choose File</label>
                        <div id="file-name-display" class="file-name"></div> <!-- Display chosen file name -->
                    </div>
                    <input type="submit" value="Upload Image">
                </form>

                {% if breed %}
                <div id="result" class="result">
                    <img id="dog-image" src="data:image/jpeg;base64,{{ image_base64 }}" alt="Dog Image">
                    <p id="breed-name">Predicted Breed: {{ breed }}</p>
                    <p id="confidence">Confidence: {{ confidence }}%</p>
                </div>
                {% elif error %}
                <div class="error">
                    <p>Error: {{ error }}</p>
                </div>
                {% endif %}
            </div>
           
        </html>
    ''')

# Route to handle the image upload and conversion to base64
@app.route('/upload', methods=['POST'])
def upload_image():
    error = None
    image_base64 = ''
    breed = None
    confidence = None

    if 'image' not in request.files:
        error = 'No file part'
        return render_template_string('''<p>{{ error }}</p>''', error=error), 400
    
    file = request.files['image']
    if file.filename == '':
        error = 'No selected file'
        return render_template_string('''<p>{{ error }}</p>''', error=error), 400
    
    # Read the image file and convert to base64
    image_data = file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')  # Store image as base64 string
    
    try:
        # Call the breed prediction function from breed.py
        breed, confidence = predict_breed_from_base64(image_base64)
    except Exception as e:
        error = f"Error in prediction: {str(e)}"
        return render_template_string('''<p>{{ error }}</p>''', error=error)

    # If no error occurs, render the result template
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dog Breed Prediction Result</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background-color: #f7f7ff;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    max-width: 700px;
                    margin: 50px auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }
                h1 {
                    color: #a26fff;
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    font-weight: 600;
                }
                .result img {
                    width: 100%;
                    max-width: 400px;
                    height: auto;
                    object-fit: contain;
                    margin-bottom: 20px;
                    border-radius: 10px;
                }
                .result h2 {
                    font-size: 1.8em;
                    color: #a26fff;
                }
                .result p {
                    font-size: 1.2em;
                    color: #555;
                }
                footer {
                    text-align: center;
                    margin-top: 50px;
                    font-size: 0.9em;
                    color: #777;
                }
                footer a {
                    color: #777;
                    text-decoration: none;
                    font-weight: 600;
                }
                footer a:hover {
                    color: #a26fff;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Dog Breed Prediction Result</h1>
                <img src="data:image/jpeg;base64,{{ image_base64 }}" alt="Uploaded Image">
                <h2>Predicted Breed: {{ breed }}</h2>
                <p>Confidence: {{ confidence }}%</p>
                <br>
                <a href="/">Go Back</a>
            </div>
            
        </body>
        </html>
    ''', breed=breed, confidence=confidence, image_base64=image_base64)

if __name__ == '__main__':
    app.run(debug=True)



