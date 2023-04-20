import cv2
import sqlite3
from datetime import datetime

class FaceRecognitionSystem:
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trained_model.yml')
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS logins
                         (id INTEGER, name TEXT, login_time TEXT, logout_time TEXT)''')

        self.cap = cv2.VideoCapture(0)
        
    def recognize_face(self, frame, gray, x, y, w, h):
        id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
        self.c.execute("SELECT name, id FROM people WHERE id=?", (id,))
        row = self.c.fetchone()
        if row is not None:
            name = row[0]
            id = row[1]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            name = "unknown"
            id = None
            confidence = "  {0}%".format(round(confidence))
        cv2.putText(frame, str(name), (x+5,y-5), self.font, 1, (255,255,255), 2)
        cv2.putText(frame, str(confidence), (x+5,y+h-5), self.font, 1, (255,255,0), 1)
        return id, name
        
    def check_login(self, id, name):
        self.c.execute("SELECT * FROM logins WHERE id=? AND logout_time IS NULL", (id,))
        row = self.c.fetchone()
        if row is None:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.c.execute("INSERT INTO logins (id, name, login_time) VALUES (?, ?, ?)", (id, name, current_time))
            self.conn.commit()
        else:
            login_id = row[0]
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.c.execute("UPDATE logins SET logout_time=? WHERE id=? AND logout_time IS NULL", (current_time, id))
            self.conn.commit()
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                id, name = self.recognize_face(frame, gray, x, y, w, h)
                if id is not None:
                    self.check_login(id, name)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        self.conn.close()

if __name__ == "__main__":
    system = FaceRecognitionSystem()
    system.run()
