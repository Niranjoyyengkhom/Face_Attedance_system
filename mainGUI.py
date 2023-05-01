from tkinter import *
from detector import FaceDetector
from trainer import Trainer
from recognizer import FaceRecognitionSystem
from attendance_exporter import AttendanceExporter
from reporter import Report
import sys

def open_detector():
    global running
    running = False
    detector = FaceDetector()
    detector.detect_and_save_face()

def run_trainer():
    trainer = Trainer('database.db', 'face/')
    trainer.train()
    trainer.save_model('trained_model.yml')
    trainer.close_database()

def run_recognition_system():
    global running
    running = True
    system = FaceRecognitionSystem()
    while running:
        system.run()

def stop_recognition_system():
    global running
    running = False

def export_attendance_report():
    exporter = AttendanceExporter('database.db')
    exporter.export_attendance_report()

def generate_attendance_report():
    db_file = 'database.db'
    report = Report(db_file)
    report.generate_attendance_report(output_file='attendance_report.xlsx')

root = Tk()
root.title("Face Recognition System")

running = False

# Create buttons for each option
detector_button = Button(root, text="Open detector", command=open_detector)
detector_button.pack(pady=10)

trainer_button = Button(root, text="Run trainer", command=run_trainer)
trainer_button.pack(pady=10)

recognition_button = Button(root, text="Run recognition system", command=run_recognition_system)
recognition_button.pack(pady=10)

stop_recognition_button = Button(root, text="Stop recognition system", command=stop_recognition_system)
stop_recognition_button.pack(pady=10)

exporter_button = Button(root, text="Export attendance report", command=export_attendance_report)
exporter_button.pack(pady=10)

report_button = Button(root, text="Generate attendance report", command=generate_attendance_report)
report_button.pack(pady=10)

exit_button = Button(root, text="Exit", command=sys.exit)
exit_button.pack(pady=10)

root.mainloop()
