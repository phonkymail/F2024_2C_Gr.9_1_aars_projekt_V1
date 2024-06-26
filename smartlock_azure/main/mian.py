import os
import base64
import paho.mqtt.client as mqtt
from datetime import datetime
import face_recognition
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

broker_address = "192.168.43.144"
port = 1883
topic_rasp = "image"
topic_server = "recognition"
client_id = "vm"

save_directory = "/home/rav/Desktop/smartlock/main/new"
imagebase_folder = "/home/rav/Desktop/smartlock/main/upload"
intruder_folder = "/home/rav/Desktop/smartlock/main/intruz"
os.makedirs(save_directory, exist_ok=True)
os.makedirs(imagebase_folder, exist_ok=True)
os.makedirs(intruder_folder, exist_ok=True)

#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/rav/Desktop/smartlock/web/instance/users.db'
db = SQLAlchemy(app)

# 
class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#
class Intruder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(100), nullable=False)

class FaceRecognitionSystem:
    def __init__(self, save_directory, imagebase_folder, intruder_folder):
        self.save_directory = save_directory
        self.imagebase_folder = imagebase_folder
        self.intruder_folder = intruder_folder
        
    def save_image(self, encoded_image, file_name):
        try:
            image_data = base64.b64decode(encoded_image)
            file_path = os.path.join(self.save_directory, file_name)
            with open(file_path, "wb") as image_file:
                image_file.write(image_data)
            print(f"Image saved to {file_path}")
        except Exception as e:
            print(f"Error saving image: {e}")

    def load_known_faces(self):
        known_face_encodings = []
        known_face_names = []

        print("Loading known faces from upload folder...")
        for file in os.listdir(self.imagebase_folder):
            image_path = os.path.join(self.imagebase_folder, file)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                encoding = face_encodings[0]
                known_face_encodings.append(encoding)
                known_face_names.append(file)  
                print(f"Loaded encoding for {file}")
            else:
                print(f"No face detected in {file}")

        return known_face_encodings, known_face_names

    def compare_faces(self, known_face_encodings, known_face_names):
        recognized_files = []

        print("Comparing new images with known faces...")
        for file in os.listdir(self.save_directory):
            new_image_path = os.path.join(self.save_directory, file)
            new_image = face_recognition.load_image_file(new_image_path)
            new_face_encodings = face_recognition.face_encodings(new_image)

            if len(new_face_encodings) > 0:
                new_face_encoding = new_face_encodings[0]
                matches = face_recognition.compare_faces(known_face_encodings, new_face_encoding)
                
                if True in matches:
                    first_match_index = matches.index(True)
                    recognized_file = known_face_names[first_match_index]
                    print(f"Recognized: {recognized_file}")
                    recognized_files.append(recognized_file)
                else:
                    print(f"{file}: Not recognized")
            else:
                print(f"No face detected in {file}: Bad quality")

        return recognized_files

    def handle_unrecognized_images(self, recognized_files):
        if not recognized_files:
            print("None of the new images were recognized. Moving to intruder folder.")
            for file in os.listdir(self.save_directory):
                new_image_path = os.path.join(self.save_directory, file)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                intruder_image_path = os.path.join(self.intruder_folder, f"intruder_{timestamp}_{file}")
                os.rename(new_image_path, intruder_image_path)
#
                with app.app_context():
                    intruder = Intruder(timestamp=datetime.now(), image=intruder_image_path)
                    db.session.add(intruder)
                    db.session.commit()
        else:
            print("At least one image was recognized. No images moved to intruder folder.")

    def run_face_recognition(self):
        known_face_encodings, known_face_names = self.load_known_faces()
        recognized_files = self.compare_faces(known_face_encodings, known_face_names)
        self.handle_unrecognized_images(recognized_files)
        #
        with app.app_context():
            for recognized_file in recognized_files:
                worker = Worker(name=recognized_file)
                db.session.add(worker)
            db.session.commit()
        return recognized_files

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic_rasp)
    else:
        print(f"Failed to connect, return code {rc}\n")

received_images = []

def on_message(client, userdata, msg):
    global received_images
    try:
        payload = msg.payload.decode()
        file_name, encoded_image = payload.split(":", 1)
        
        print(f"Received file: {file_name}")
        received_images.append((file_name, encoded_image))
        
        if len(received_images) == 3:
            for file_name, encoded_image in received_images:
                face_recognition_system.save_image(encoded_image, file_name)
            
            recognized_files = face_recognition_system.run_face_recognition()
            
            if recognized_files:
                for recognized_file in recognized_files:
                    client.publish(topic_server, recognized_file)
            else:
                client.publish(topic_server, "no permission")
            
            received_images = []  
        
    except Exception as e:
        print(f"Error decoding or saving image: {e}")

def main():
    global face_recognition_system
    face_recognition_system = FaceRecognitionSystem(save_directory, imagebase_folder, intruder_folder)

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, port, 60)
    client.loop_forever()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    main()

