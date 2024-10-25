# from flask import Flask, request, render_template, redirect, url_for, flash
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import numpy as np
# import os

# app = Flask(__name__)
# app.secret_key = "supersecretkey"
# model = load_model('malaria_model.h5')


# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)

#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)

#     if file and allowed_file(file.filename):
#         filename = os.path.join('uploads', file.filename)
#         file.save(filename)

#         img = image.load_img(filename, target_size=(150, 150))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array /= 255.0

#         prediction = model.predict(img_array)
#         os.remove(filename)

#         if prediction[0][0] > 0.5:
#             result = "Uninfected"
#         else:
#             result = "Infected"

#         return render_template('result.html', prediction=result)
#     else:
#         flash('Allowed file types are jpg, jpeg, png')
#         return redirect(request.url)


# def allowed_file(filename):
#     ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, request, render_template, redirect, url_for, flash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import gdown  # Ensure gdown is installed

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Download model from Google Drive
gdrive_file_id = '11THtZ1DiVEfpZUevYIDJXFxJU-RwfJN0'  # Your file ID
gdown.download(f'https://drive.google.com/uc?id={gdrive_file_id}', 'malaria_model.h5', quiet=False)

model = load_model('malaria_model.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = os.path.join('uploads', file.filename)
        file.save(filename)

        img = image.load_img(filename, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        prediction = model.predict(img_array)
        os.remove(filename)

        if prediction[0][0] > 0.5:
            result = "Uninfected"
        else:
            result = "Infected"

        return render_template('result.html', prediction=result)
    else:
        flash('Allowed file types are jpg, jpeg, png')
        return redirect(request.url)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)
