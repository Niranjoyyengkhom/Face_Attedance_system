import cv2
import os
import sqlite3

class FaceDetector:
    def __init__(self):
        # Connect to the database or create it if it doesn't exist
        self.conn = sqlite3.connect('database.db')

        # Create a table to store the names and image file paths
        self.conn.execute('CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')

        # Path to the folder where the images will be saved
        self.path = 'face/'

        # Create the folder if it doesn't exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # Initialize the camera
        self.cam = cv2.VideoCapture(0)

        # Initialize the face detector
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Prompt the user to enter the name for the face
        self.name = input('Enter name for this face: ')
        self.count = 1

        # Retrieve the ID of the newly inserted name
        if self.name:
            cursor = self.conn.execute('SELECT id FROM people WHERE name = ?', (self.name,))
            row = cursor.fetchone()
            if row is not None:
                self.id = row[0]
                print(f"Welcome back, {self.name}! Your ID is {self.id}.")
            else:
                self.conn.execute('INSERT INTO people (name) VALUES (?)', (self.name,))
                self.conn.commit()
                cursor = self.conn.execute('SELECT id FROM people WHERE name = ?', (self.name,))
                row = cursor.fetchone()
                self.id = row[0]
                print(f"Hello, {self.name}! Your ID is {self.id}.")
        else:
            print("No name entered. Exiting...")
            self.cam.release()
            cv2.destroyAllWindows()
            self.conn.close()
            exit()

    def detect_and_save_face(self):
        # Iterate until 20 images are saved
        while self.count <= 20:
            # Read the frame
            _, frame = self.cam.read()

            # Detect faces in the frame
            faces = self.face_detector.detectMultiScale(frame, 1.3, 5)

            # Draw bounding boxes around the faces and show the frame
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Save the image with the name
                if self.name:
                    # Convert the frame to grayscale
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # Save the image with a meaningful name
                    filename = os.path.join(self.path, self.name + '_' + str(self.count) + '.jpg')
                    cv2.imwrite(filename, gray[y:y+h, x:x+w])
                    self.count += 1

            # Show the frame
            cv2.imshow('frame', frame)

            # Wait for 1 millisecond for a key press
            key = cv2.waitKey(1)

            # If the 'q' key is pressed, exit the loop
            if key == ord('q'):
                break

        # Release the camera and close all windows
        self.cam.release()
        cv2.destroyAllWindows()

        # Close the database connection
        self.conn.close()

        # Print the ID of the new person added
        print(f'The ID of the new person added is: {self.id}')

if __name__ == "__main__":
    detector = FaceDetector()
    detector.detect_and_save_face()
