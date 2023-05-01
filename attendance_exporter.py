import sqlite3
from datetime import datetime


class AttendanceExporter:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()
        now = datetime.now()
        self.timestamp = now.strftime('%Y-%m-%d %H-%M-%S')

    def export_attendance_report(self):
        # Execute a SELECT query to retrieve the data for all employees and days
        self.cur.execute("SELECT id, date(login_time), min(login_time), max(logout_time) FROM logins GROUP BY id, date(login_time)")

        # Fetch all the rows
        rows = self.cur.fetchall()

        # Process each row of data
        for row in rows:
            # Extract the ID, date, first login time and last logout time
            id = row[0]
            date = row[1]
            first_login_time = row[2]
            last_logout_time = row[3]

            # Execute a SELECT query to retrieve the name of the employee
            self.cur.execute(f"SELECT name FROM people WHERE id='{id}'")

            # Fetch the row
            person_row = self.cur.fetchone()

            # Extract the name
            name = person_row[0]

            # Insert the data into the attendance table
            self.cur.execute("INSERT INTO attendance (name, date, first_login_time, last_logout_time) VALUES (?, ?, ?, ?)",
                             (name, date, first_login_time, last_logout_time))

        # Commit the changes to the database
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# Create an instance of the AttendanceExporter class and export the attendance report
exporter = AttendanceExporter('database.db')
exporter.export_attendance_report()
