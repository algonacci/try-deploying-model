from fastapi import FastAPI, File, UploadFile
import uvicorn

import io
from PIL import Image
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("model.h5")
app = FastAPI()


def preprocess_image(image):
    image = image.resize((300, 300))
    image_array = np.array(image)
    image_array = tf.keras.applications.resnet50.preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    resized_image = preprocess_image(image)
    predictions = model.predict(resized_image)

    if predictions > 0.5:
        return {"It is a night"}
    else:
        return {"It is a day"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, timeout_keep_alive=1200)
