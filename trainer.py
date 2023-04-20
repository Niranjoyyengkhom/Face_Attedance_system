import cv2
import numpy as np
import sqlite3
import os

class Trainer:
    def __init__(self, database_path, images_path):
        self.conn = sqlite3.connect(database_path)
        self.path = images_path
        self.faces = []
        self.labels = []
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    def _load_images(self):
        cursor = self.conn.execute('SELECT id, name FROM people')
        for row in cursor:
            person_id = row[0]
            person_name = row[1]
            for filename in os.listdir(self.path):
                if filename.startswith(person_name):
                    img = cv2.imread(os.path.join(self.path, filename))
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    self.faces.append(gray)
                    self.labels.append(person_id)

    def train(self):
        self._load_images()
        self.face_recognizer.train(self.faces, np.array(self.labels))

    def save_model(self, file_path):
        self.face_recognizer.save(file_path)

    def close_database(self):
        self.conn.close()


if __name__ == '__main__':
    trainer = Trainer('database.db', 'face/')
    trainer.train()
    trainer.save_model('trained_model.yml')
    trainer.close_database()
