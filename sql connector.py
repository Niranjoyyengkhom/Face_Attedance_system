import sqlite3
import xlsxwriter
# Connect to the database
conn = sqlite3.connect('database.db')

# Define a function to handle each action
def handle_action(action):
    if action == '1':
        # Prompt the user for the table name and column names
        table_name = input("Enter the table name: ")
        column_names = input("Enter the column names separated by commas: ")

        # Create the table
        conn.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, column_names))
        conn.commit()
        print("Table created successfully.")

    elif action == '2':
        # Prompt the user for the table name and values to insert
        table_name = input("Enter the table name: ")
        values = input("Enter the values to insert separated by commas: ")

        # Insert the data into the table
        conn.execute("INSERT INTO {} VALUES ({})".format(table_name, values))
        conn.commit()
        print("Row inserted successfully.")

    elif action == '3':
        # Prompt the user for the table name and ID of the row to delete
        table_name = input("Enter the table name: ")
        id = input("Enter the ID of the row to delete: ")

        # Delete the row from the table
        conn.execute("DELETE FROM {} WHERE id={}".format(table_name, id))
        conn.commit()
        print("Row deleted successfully.")

    elif action == '4':
        # Prompt the user for the table name, ID, and new values to update
        table_name = input("Enter the table name: ")
        id = input("Enter the ID of the row to update: ")
        values = input("Enter the new values separated by commas: ")

        # Update the row in the table
        conn.execute("UPDATE {} SET {} WHERE id={}".format(table_name, values, id))
        conn.commit()
        print("Row updated successfully.")

    elif action == '5':
        # Prompt the user for the table name and display the table schema
        table_name = input("Enter the table name: ")
        cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name))
        row = cursor.fetchone()
        if row is None:
            print("Table does not exist.")
        else:
            print(row[0])
            
    elif action == '6':
        # Prompt the user for the table name to delete
        table_name = input("Enter the name of the table to delete: ")

        # Delete the table
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        print("Table deleted successfully.")
        
    elif action == '7':
        # Prompt the user for the table name and column names to update
        table_name = input("Enter the table name: ")
        column_name = input("Enter the column name: ")
        new_column_name = input("Enter the new column name: ")
        

        # Update the table in the database
        conn.execute("ALTER TABLE {} RENAME COLUMN {} TO {}".format(table_name, column_name, new_column_name))
        conn.commit()
        print("Table updated successfully.")
    
    elif action == '8':
        # Prompt the user for the table name and new column name
        table_name = input("Enter the table name: ")
        column_name = input("Enter the new column name: ")
        
        # Add new column to the table
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name}")
        conn.commit()
        print("Column added successfully.")
    
    elif action == '9':
        # Prompt the user for the table name and column name to remove
        table_name = input("Enter the table name: ")
        column_name = input("Enter the name of the column to remove: ")

        # Remove the column from the table
        conn.execute("ALTER TABLE {} DROP COLUMN {}".format(table_name, column_name))
        conn.commit()
        print("Column removed successfully.")
    elif action == '10':
        # Prompt the user for the table name to truncate
        table_name = input("Enter the table name: ")

        # Delete all data from the table
        conn.execute("DELETE FROM {}".format(table_name))
        conn.commit()
        print("All data deleted successfully.")
    
    elif action == 'e':
    # Prompt the user for the table name and user id
        table_name = input("Enter the table name: ")
        id = input("Enter the user id: ")

        # Get the first and last login time for the user
        cursor = conn.execute("SELECT MIN(login_time), MAX(login_time) FROM {} WHERE id={}".format(table_name, id))
        row = cursor.fetchone()

        workbook = xlsxwriter.Workbook('login_times.xlsx')
        worksheet = workbook.add_worksheet()

        # Write the data to the excel file
        worksheet.write('A1', 'User ID')
        worksheet.write('B1', 'First Login Time')
        worksheet.write('C1', 'Last Login Time')
        worksheet.write('A2', id)
        worksheet.write('B2', row[0])
        worksheet.write('C2', row[1])

        workbook.close()

        print("Login times exported to login_times.xlsx.")


    elif action == '0':
        print("Exiting...")
        return False

    else:
        print("Invalid action entered. Please enter '1', '2', '3', '4', '5','6' or '0' only.")

    return True

# Prompt the user for their choice of action
while True:
    action = input("Enter '1' to create a new table, '2' to insert a new row, '3' to delete an existing row, '4' to update an existing row, '5' to display the schema for a table, 6 to Drop a Table ,or '0' to exit: ")

    # Handle the action
    if not handle_action(action):
        break

# Close the connection
conn.close()

