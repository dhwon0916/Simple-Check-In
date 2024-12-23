import os
import pandas as pd

studentList = []
sList = []
script_directory = os.path.dirname(os.path.abspath(__file__))
excel_files = [os.path.join(script_directory, f) for f in os.listdir(script_directory) if f.endswith('.xlsx')]

if not excel_files:
    input("No Excel files found in the script directory.\n")
    quit()
try:
    for file in excel_files:
        if not file.endswith('sorted_attendance.xlsx'):
            excel_data = pd.ExcelFile(file)
            df = excel_data.parse(excel_data.sheet_names[0])
            students = df[['Name', 'Student ID']]

    studentList = list(set(students.to_string(index=False).split("\n")))

    for i in studentList:
        student = i.split()
        student.insert(-1, "-")
        sList.append(' '.join(student))

    sList.remove("Name Student - ID")

    attendance = {}
    for i in sList:
        attendance[i] = {}
        sID = int(i.split(' - ')[-1])
        for file in excel_files:
            excel_data = pd.ExcelFile(file)
            df = excel_data.parse(excel_data.sheet_names[0])
            attendance[i][df.columns[3]] = df[df['Student ID'] == sID].to_string(index=False).split()[-1]

    def sort_attendance_data(attendance_dict):
        sorted_data = []
        for student, dates in attendance_dict.items():
            sorted_dates = sorted(dates.items(), key=lambda x: pd.to_datetime(x[0], format='%m-%d-%Y'))
            sorted_data.append((student, dict(sorted_dates)))
        return sorted_data

    def write_attendance_to_excel(attendance_dict, output_file='sorted_attendance.xlsx'):
        sorted_attendance = sort_attendance_data(attendance_dict)
        
        # Prepare data for the final Excel output
        data_for_excel = {}
        all_dates = sorted({date for student, dates in attendance_dict.items() for date in dates.keys()}, key=lambda x: pd.to_datetime(x, format='%m-%d-%Y'))
        header = ['Name', 'Student ID', 'Total Absents'] + all_dates

        for student, dates in sorted_attendance:
            student_name, student_id = student.rsplit(' - ', 1)  # Split into name and ID
            row = [student_name, student_id]
            
            # Count absents and add it to the row
            total_absents = sum(1 for status in dates.values() if status == 'Absent')
            row.append(total_absents)
            
            for date in all_dates:
                row.append(dates.get(date, 'Absent'))
            
            data_for_excel[student] = row
        
        # Create DataFrame and write to Excel
        df = pd.DataFrame.from_dict(data_for_excel, orient='index', columns=header)
        df.reset_index(drop=True, inplace=True)
        df.to_excel(output_file, index=False)
        
        print(f"Attendance data has been successfully written to {output_file}.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'sorted_attendance.xlsx')
    write_attendance_to_excel(attendance, output_file=output_path)
except:
    print("Remove any Excel files that are not attendance sheets from the script directory.")
    input("Press Enter to exit.")