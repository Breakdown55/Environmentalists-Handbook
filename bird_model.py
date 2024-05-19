import numpy as np
import librosa
import tensorflow as tf





def load_labels(label_path):
    with open(label_path, 'r') as f:
        return [line.strip() for line in f.readlines()]


def load_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


def preprocess_audio(audio_path, target_shape):
    sample_rate = target_shape[0]  # Assuming target_shape is [44032]
    y, sr = librosa.load(audio_path, sr=sample_rate)
    
    if len(y) < target_shape[0]:
        y = np.pad(y, (0, target_shape[0] - len(y)))
    else:
        y = y[:target_shape[0]]
    
    y = y.astype(np.float32)
    return y

def run_inference(interpreter, input_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], [input_data])
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

def classify_audio(audio_path, model_path, label_path):
    labels = load_labels(label_path)
    interpreter = load_model(model_path)
    
    input_details = interpreter.get_input_details()
    input_shape = input_details[0]['shape'][1]  
    
    audio_data = preprocess_audio(audio_path, [input_shape])
    
    predictions = run_inference(interpreter, audio_data)
    predicted_label = labels[np.argmax(predictions)]
    
    return predicted_label