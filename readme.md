
# SignaMatch: A Web-Based Signature Matching System

## Project Overview
SignaMatch is a Flask-based web application that compares an uploaded signature image with a reference dataset and displays the three most visually similar signatures.

## Technologies Used
- Python
- Flask
- OpenCV
- NumPy
- Pillow
- scikit-image
- HTML, CSS, and JavaScript

## Features
- Upload a signature image
- Preprocess images using grayscale conversion, Gaussian blur, and resizing
- Compare images using Structural Similarity Index Measure (SSIM)
- Display the top three visually similar results
- Show reference filenames and similarity scores

## Project Structure
- app.py: Flask backend
- templates/index.html: Website interface
- static/style.css: Website styling
- static/script.js: Frontend interactions
- signature_dataset/: Local reference images (not included in this repository)

## Installation
1. Clone this repository.
2. Open the project folder in a terminal.
3. Create and activate a virtual environment.
4. Install dependencies using `pip install -r requirements.txt`.
5. Add your authorized reference images to the `signature_dataset` folder.
6. Run `python app.py`.
7. Open http://127.0.0.1:5000 in your browser.

## Disclaimer
Similarity scores indicate visual resemblance only. They do not establish a signer's identity or verify signature authenticity.
