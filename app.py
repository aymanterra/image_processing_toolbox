from flask import Flask, render_template, request
import os
import actions
from logger import logger
from helpers import getRandId

app = Flask(__name__)

uploads_dir = os.path.join(app.root_path, 'static', 'images')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image_histogram', methods=['GET', 'POST'])
def image_histogram():
    if request.method == "GET":
        return render_template('image_histogram/index.html')
    elif request.method == "POST":
        random_id = getRandId(10)
        orginal_img = request.files["file"]
        orginal_img_path = os.path.join(uploads_dir, f'original-{random_id}.jpeg')
        orginal_img.save(orginal_img_path)
        actions.image_histogram(random_id)
        return render_template('image_histogram/result.html', random_id=random_id)

@app.route('/histogram_equalization', methods=['GET', 'POST'])
def histogram_equalization():
    if request.method == "GET":
        return render_template('histogram_equalization/index.html')
    elif request.method == "POST":
        random_id = getRandId(10)
        orginal_img = request.files["file"]
        orginal_img_path =  os.path.join(uploads_dir, f'original-{random_id}.jpeg')
        orginal_img.save(orginal_img_path)
        actions.histogram_equalization(random_id)
        return render_template('histogram_equalization/result.html', random_id=random_id)

@app.route('/edge_detection', methods=['GET', 'POST'])
def edge_detection():
    if request.method == "GET":
        return render_template('edge_detection/index.html')
    elif request.method == "POST":
        random_id = getRandId(10)
        orginal_img = request.files["file"]
        orginal_img_path =  os.path.join(uploads_dir, f'original-{random_id}.jpeg')
        orginal_img.save(orginal_img_path)
        filtering_technique = request.form["filtering_technique"]
        actions.edge_detection(random_id, filtering_technique)
        return render_template('edge_detection/result.html', random_id=random_id, filtering_technique=filtering_technique)

@app.route('/image_fourier_transformation', methods=['GET', 'POST'])
def image_fourier_transformation():
    if request.method == "GET":
        return render_template('image_fourier_transformation/index.html')
    elif request.method == "POST":
        random_id = getRandId(10)
        orginal_img = request.files["file"]
        orginal_img_path =  os.path.join(uploads_dir, f'original-{random_id}.jpeg')
        orginal_img.save(orginal_img_path)
        actions.image_fourier_transformation(random_id)
        return render_template('image_fourier_transformation/result.html', random_id=random_id)

@app.route('/adding_noise', methods=['GET', 'POST'])
def adding_noise():
    if request.method == "GET":
        return render_template('adding_noise/index.html')
    elif request.method == "POST":
        random_id = getRandId(10)
        orginal_img = request.files["file"]
        orginal_img_path =  os.path.join(uploads_dir, f'original-{random_id}.jpeg')
        orginal_img.save(orginal_img_path)
        noise_type = request.form["noise_type"]
        params = request.form
        actions.adding_noise(random_id, noise_type, params)
        return render_template('adding_noise/result.html', random_id=random_id, noise_type=noise_type)

@app.route('/removing_noise', methods=['GET', 'POST'])
def removing_noise():
    if request.method == "GET":
        return render_template('removing_noise/index.html')
    elif request.method == "POST":
        random_id = getRandId(10)
        orginal_img = request.files["file"]
        orginal_img_path =  os.path.join(uploads_dir, f'original-{random_id}.jpeg')
        orginal_img.save(orginal_img_path)
        noise_type = request.form["noise_type"]
        params = request.form
        if noise_type == "Periodic" and params["removal_type"] == "Mask":
            actions.image_fourier_transformation(random_id)
            return render_template('removing_noise/mask_form.html', random_id=random_id, noise_type=noise_type, params=params)
        actions.removing_noise(random_id, noise_type, params)
        return render_template('removing_noise/result.html', random_id=random_id, noise_type=noise_type, params=params)

@app.route('/removing_noise_mask', methods=['POST'])
def mask_form():
    params = request.form
    random_id = params["random_id"]
    noise_type = params["noise_type"]
    actions.removing_noise(random_id, noise_type, params)
    return render_template('removing_noise/result.html', random_id=random_id, noise_type=noise_type, params=params)

if __name__ == "__main__":
    app.run(debug=True)
