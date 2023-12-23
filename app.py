from flask import Flask, render_template, request, jsonify, send_file
import generate_perceptron_image
from perceptron import Perceptron
import time
import os
import shutil
from apscheduler.schedulers.background import BackgroundScheduler

# Creating temporary images directory
current_dir = os.getcwd()
print(f"CWD: {current_dir}")
temp_images_dir = "temp_images"
temp_images_path = os.path.join(current_dir,temp_images_dir)
if not os.path.exists(temp_images_path):
    os.makedirs(temp_images_path)
    print(f"New directory created {temp_images_path}")
else :
    print(f"{temp_images_dir} already exists")

# directory clean up routine executed every 1 minute
def cleanup_dir() :
    print(f"Starting cleaning up {temp_images_dir}")
    try:
        entries = os.listdir(temp_images_path)
        for entry in entries:
            entry_path = os.path.join(temp_images_path, entry)
            if os.path.isfile(entry_path):
                os.remove(entry_path)
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
        print(f"The directory '{temp_images_path}' has been emptied.")
    except Exception as e:
        print(f"Error emptying directory: {e}")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',ts=int(time.time()))

@app.route('/run_perceptron', methods=['POST'])
def run_perceptron():
    data = request.get_json()

    title = data['title']
    response_vector = data['input']
    threshold = int(data['threshold'])
    
    input_vector = [0]*len(response_vector)
    weights = [0]*len(response_vector)
    for i,inp in enumerate(response_vector) :
        input_vector[i] = inp['value']
        weights[i] = inp['weight']
    
    perc = Perceptron(input_vector,weights,threshold)
    output = perc.predict()
    
    timestamp = int(time.time())
    image_name = f'perceptron_img{ timestamp }.png'
    image_path = os.path.join(temp_images_path,image_name)
    
    generate_perceptron_image.drawImg(perc,image_path)

    image_url = f'/get_perceptron_image/{image_name}'
    return jsonify({'output': output, 'image_url': image_url})

@app.route('/get_perceptron_image/<image_name>',methods=['GET'])
def get_perceptron_image(image_name):
    # Return the generated image file
    return send_file(os.path.join(temp_images_path,image_name), mimetype='image/png')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_dir,'interval',minutes=1)
    scheduler.start()
    app.run(debug=True)
    cleanup_dir()