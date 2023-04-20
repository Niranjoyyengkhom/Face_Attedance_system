import os
from datetime import datetime
import xlsxwriter
import sqlite3


class AttendanceExporter:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()
        now = datetime.now()
        self.timestamp = now.strftime('%Y-%m-%d %H-%M-%S')

    def export_attendance_report(self):
        # Create a new Excel workbook and add a worksheet
        workbook = xlsxwriter.Workbook(f'Attendance Report {self.timestamp}.xlsx')
        worksheet = workbook.add_worksheet()

        # Write the headers for the worksheet
        worksheet.write('A1', 'Name')
        worksheet.write('B1', 'Date')
        worksheet.write('C1', 'First Login')
        worksheet.write('D1', 'Last Logout')

        # Execute a SELECT query to retrieve the data for all employees and days
        self.cur.execute("SELECT id, date(login_time), min(login_time), max(logout_time) FROM logins GROUP BY id, date(login_time)")

        # Fetch all the rows
        rows = self.cur.fetchall()

        # Initialize the row counter
        row_num = 2

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

            # Write the data to the worksheet
            worksheet.write(f'A{row_num}', name)
            worksheet.write(f'B{row_num}', date)
            worksheet.write(f'C{row_num}', first_login_time)
            worksheet.write(f'D{row_num}', last_logout_time)

            # Insert the data into the attendance table
            self.cur.execute("INSERT INTO attendance (name, date, first_login_time, last_logout_time) VALUES (?, ?, ?, ?)",
                             (name, date, first_login_time, last_logout_time))

            # Increment the row counter
            row_num += 1

        # Commit the changes to the database
        self.conn.commit()

        # Close the workbook
        workbook.close()

    def __del__(self):
        self.conn.close()


# Create an instance of the AttendanceExporter class and export the attendance report
exporter = AttendanceExporter('database.db')
exporter.export_attendance_report()
