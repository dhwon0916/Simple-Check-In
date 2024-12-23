# General Check-In Program

This repository contains a versatile **Check-In Program** designed to streamline attendance management for events, clubs, classrooms, or organizations. It also includes a complementary **Excel Compiler** for consolidating attendance data from multiple files into a single report.

---

## Main Program: Check-In Program (`checkIn.py`)

### Description

The Check-In Program is a user-friendly application with a graphical interface that allows administrators to efficiently track attendance. Students can be marked as present or absent, and their records can be easily managed and exported for further analysis. For the best experience, it is recommended to use a **barcode scanner** to quickly check in attendees by scanning their IDs.

### Features

- Mark students as **present** or **absent** using their ID.
- Add, edit, or remove student records via a simple GUI.
- **Undo/Redo functionality** for changes made to attendance or student lists.
- Save attendance data to an Excel file for reporting and archiving.
- Automatically validates student data to prevent duplicates.
- Supports **barcode scanners** for fast and efficient check-ins.

### How to Use

1. Run the program:
   ```bash
   python checkIn.py
   ```
2. Use a **barcode scanner** or manually enter a student ID to mark attendance.
3. Double-click on names in the "Present" or "Absent" lists to toggle their status.
4. Access the "Edit" menu to add or remove students.
5. Close the program to save changes, with an option to export attendance to Excel.

### Requirements

- Python 3.x
- Libraries:
  - `tkinter`
  - `pandas`
  - `openpyxl`

---

## Additional Tool: Excel Compiler (`ExcelCompiler.py`)

### Description

The Excel Compiler complements the Check-In Program by consolidating attendance records from multiple Excel files. It generates a sorted report summarizing attendance data, including total absences and statuses for all tracked dates.

### Features

- Processes multiple Excel files and compiles them into a single report.
- Sorts attendance data by date for clear analysis.
- Calculates total absences for each student.
- Outputs the consolidated report as `sorted_attendance.xlsx`.

### How to Use

1. Place all attendance Excel files in the same directory as `ExcelCompiler.py`.
2. Run the program:
   ```bash
   python ExcelCompiler.py
   ```
3. The generated report `sorted_attendance.xlsx` will appear in the same directory.

### Requirements

- Python 3.x
- Libraries:
  - `pandas`
  - `openpyxl`

---

## Installation

1. Ensure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).
2. Install the required libraries by running:
   ```bash
   pip install pandas openpyxl
   ```
3. Download or clone this repository and place it in a desired directory.

---

## Support

If you have questions or encounter issues, please reach out to [DonghyunWon2@gmail.com](mailto\:DonghyunWon2@gmail.com).

---

## Future Enhancements

- **Check-In Program**:

  - Integration with cloud-based databases for real-time attendance tracking.
  - Enhanced reporting features for more detailed analytics.

- **Excel Compiler**:

  - Improved handling of varying attendance sheet formats.
  - Automatic detection of irrelevant files in the working directory.

Thank you for using these tools to simplify your attendance management process!

