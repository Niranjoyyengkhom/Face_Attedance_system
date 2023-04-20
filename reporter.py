import sqlite3
from datetime import datetime
import xlsxwriter

class Report:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()

    def generate_attendance_report(self, output_file=None):
        # Execute a SELECT query to retrieve the data for all employees and days
        self.cur.execute("SELECT id, date(login_time), min(login_time), max(logout_time) FROM logins GROUP BY id, date(login_time)")

        # Fetch all the rows
        rows = self.cur.fetchall()

        # Create a dictionary to store the number of days present for each ID
        days_present = {}

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

            # Increment the number of days present for this employee
            if id in days_present:
                days_present[id] += 1
            else:
                days_present[id] = 1

        # Export the number of days present to Excel
        if output_file is None:
            now = datetime.now()
            timestamp = now.strftime('%Y-%m-%d %H-%M-%S')
            output_file = f'attendance_report_{timestamp}.xlsx'

        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet()

        # Write the header row
        header = ['ID', 'Name', 'Days Present']
        for i, col in enumerate(header):
            worksheet.write(0, i, col)

        # Write the data rows
        for i, (id, name) in enumerate(self.cur.execute("SELECT id, name FROM people")):
            if id in days_present:
                days = days_present[id]
            else:
                days = 0

            worksheet.write(i+1, 0, id)
            worksheet.write(i+1, 1, name)
            worksheet.write(i+1, 2, days)

        workbook.close()
        print(f"Attendance report generated: {output_file}")

        #self.cur.execute("DELETE FROM logins")
        #self.conn.commit()
        #print("logins Data Remove Sucessfully")

    def __del__(self):
        self.conn.close()

def final_report():
    db_file = 'database.db'
    report = Report(db_file)
    report.generate_attendance_report()

if __name__ == '__main__':
    final_report()
