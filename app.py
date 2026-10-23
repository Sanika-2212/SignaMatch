
from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError
from pathlib import Path
from skimage.metrics import structural_similarity
import cv2
import numpy as np
import io

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "signature_dataset"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
IMAGE_SIZE = (300, 150)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def preprocess_signature(image):
    """Standardize an image before comparing its visual appearance."""
    image = image.convert("RGB")
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = cv2.resize(image, IMAGE_SIZE)
    return image


def compare_signatures(image1, image2):
    first = preprocess_signature(image1)
    second = preprocess_signature(image2)

    score = structural_similarity(first, second, data_range=255)

    # Present a bounded visual similarity score.
    return round(float(np.clip(score * 100, 0, 100)), 2)


def get_dataset_images():
    if not DATASET_DIR.is_dir():
        return []

    images = []
    for path in sorted(DATASET_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() in {
            ".jpg", ".jpeg", ".png"
        }:
            try:
                with Image.open(path) as image:
                    images.append({
                        "filename": path.name,
                        "image": image.convert("RGB").copy()
                    })
            except (OSError, UnidentifiedImageError):
                continue

    return images


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("signature")

        if not uploaded_file or not uploaded_file.filename:
            error = "Please choose a signature image first."

        elif not allowed_file(uploaded_file.filename):
            error = "Please upload a JPG, JPEG, or PNG image."

        else:
            try:
                query_image = Image.open(
                    io.BytesIO(uploaded_file.read())
                ).convert("RGB")

                dataset = get_dataset_images()

                if not dataset:
                    error = (
                        "No dataset images found. Check your "
                        "signature_dataset folder."
                    )
                else:
                    for item in dataset:
                        score = compare_signatures(
                            query_image, item["image"]
                        )
                        results.append({
                            "filename": item["filename"],
                            "score": score
                        })

                    results.sort(
                        key=lambda result: result["score"],
                        reverse=True
                    )
                    results = results[:3]

            except (OSError, UnidentifiedImageError, ValueError):
                error = "The uploaded image could not be read. Try another."

    return render_template(
        "index.html",
        results=results,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
