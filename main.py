from detector import FaceDetector
from trainer import Trainer
from recognizer import FaceRecognitionSystem
from attendance_exporter import AttendanceExporter
from reporter import Report
import sys

while True:
    print("Press 1 to open detector, 2 to run trainer, or q to exit.")
    choice = input("Enter your choice: ")

    if choice == '1':
        detector = FaceDetector()
        detector.detect_and_save_face()
    elif choice == '2':
        trainer = Trainer('database.db', 'face/')
        trainer.train()
        trainer.save_model('trained_model.yml')
        trainer.close_database()
    elif choice == '3':
        system = FaceRecognitionSystem()
        system.run()
    elif choice =='4':
        exporter = AttendanceExporter('database.db')
        exporter.export_attendance_report()
        pass
    elif choice =='5':
        db_file = 'database.db'
        report = Report(db_file)
        report.generate_attendance_report(output_file='attendance_report.xlsx')
    elif choice.lower() == 'q':
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
    

    db_file = 'database.db'
    report = Report(db_file)
    report.generate_attendance_report(output_file='attendance_report.xlsx')