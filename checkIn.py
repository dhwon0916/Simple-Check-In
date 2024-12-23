import json
import os
from datetime import datetime
try:
    import tkinter as tk
    from tkinter import messagebox, filedialog
    import pandas as pd
except:
    import pip
    pip.main(["install", "--user", "tkinter"])
    pip.main(["install", "--user", "pandas"])
    pip.main(["install", "--user", "openpyxl"])
    import tkinter as tk
    from tkinter import messagebox, filedialog
    import pandas as pd

undo_stack = []
redo_stack = []

json_file = 'student_data.json'
file_path = os.path.join(os.path.dirname(__file__), json_file)

if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        json.dump([], f)
        messagebox.showinfo("File Created", f"File not found. A new file was created at {file_path}")

try:
    with open(file_path, 'r') as f:
        data = json.load(f)
    if data == []:
        valid = True
    else:
        if isinstance(data, list):
            valid = True
            for entry in data:
                if not isinstance(entry, dict):
                    valid = False
                    break
                if not all(isinstance(entry.get(key), expected_type) for key, expected_type in {"ID": int, "First Name": str, "Last Name": str, "Sex": str}.items()):
                    valid = False
                    break
        else:
            valid = False
    if not valid:
        messagebox.showerror("Error", "The JSON file format is incorrect.")
        exit(1)

except json.JSONDecodeError as e:
    messagebox.showerror("Error", f"Error reading JSON file: {e}")
    exit(1)

present = []
absent = data.copy()

def find_student(student_id, student_list):
    for student in student_list:
        if str(student['ID']) == str(student_id):
            return student
    return None

def is_duplicate_student(student_id):
    for student in present + absent:
        if str(student['ID']) == str(student_id):
            return True
    return False

def update_json_file():
    all_students = present + absent
    with open(file_path, 'w') as f:
        json.dump(all_students, f, indent=4)

def show_auto_dismiss_message(title, message):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("250x100")
    popup_label = tk.Label(popup, text=message, padx=20, pady=20)
    popup_label.pack()
    root.after(1000, popup.destroy)

def add_to_undo(action, student_data):
    undo_stack.append((action, student_data))
    redo_stack.clear()

def undo():
    if not undo_stack:
        messagebox.showinfo("Undo", "No actions to undo")
        return
    
    action, student_data = undo_stack.pop()
    redo_stack.append((action, student_data))
    
    if action == "mark_present":
        present.remove(student_data)
        absent.append(student_data)
    elif action == "mark_absent":
        absent.remove(student_data)
        present.append(student_data)
    elif action == "add_student":
        absent.remove(student_data)
    elif action == "remove_student":
        absent.append(student_data)
    
    update_display()
    update_json_file()

def redo():
    if not redo_stack:
        messagebox.showinfo("Redo", "No actions to redo")
        return
    
    action, student_data = redo_stack.pop()
    undo_stack.append((action, student_data))
    
    if action == "mark_present":
        absent.remove(student_data)
        present.append(student_data)
    elif action == "mark_absent":
        present.remove(student_data)
        absent.append(student_data)
    elif action == "add_student":
        absent.append(student_data)
    elif action == "remove_student":
        absent.remove(student_data)
    
    update_display()
    update_json_file()

def mark_present(event=None):
    student_id = student_id_entry.get().strip()
    if not student_id:
        show_auto_dismiss_message("Input Error", "Please enter a student ID")
        return
    
    student = find_student(student_id, present)
    if student:
        show_auto_dismiss_message("Already Marked", "Student is already marked present")
        student_id_entry.delete(0, tk.END)
        return

    student = find_student(student_id, absent)
    if student:
        absent.remove(student)
        present.insert(0, student)
        add_to_undo("mark_present", student)
        update_display()
        update_json_file()
        #show_auto_dismiss_message("Success", f"Student {student['First Name']} {student['Last Name']} is marked present!")
    else:
        show_auto_dismiss_message("Not Found", "Student not found")
    
    student_id_entry.delete(0, tk.END)

def update_display():
    present_list.delete(0, tk.END)
    absent_list.delete(0, tk.END)
    
    for student in present:
        present_list.insert(tk.END, f"{student['ID']} - {student['First Name']} {student['Last Name']}")
    
    present_label.config(text=f"Present Students ({len(present)})")
    
    for student in absent:
        absent_list.insert(tk.END, f"{student['ID']} - {student['First Name']} {student['Last Name']}")
    
    absent_label.config(text=f"Absent Students ({len(absent)})")

def move_to_absent(event):
    selected_index = present_list.curselection()
    if selected_index:
        student_data = present[selected_index[0]]
        present.remove(student_data)
        absent.insert(0, student_data)
        add_to_undo("mark_absent", student_data)
        update_display()
        update_json_file()

def move_to_present(event):
    selected_index = absent_list.curselection()
    if selected_index:
        student_data = absent[selected_index[0]]
        absent.remove(student_data)
        present.insert(0, student_data)
        add_to_undo("mark_present", student_data)
        update_display()
        update_json_file()

def add_student():
    student_id = new_student_id.get().strip()
    first_name = new_student_first_name.get().strip()
    last_name = new_student_last_name.get().strip()
    sex = new_student_sex.get().strip()

    if not student_id or not first_name or not last_name or not sex:
        messagebox.showerror("Input Error", "Please fill in all fields")
        return
    
    if is_duplicate_student(student_id):
        messagebox.showerror("Duplicate ID", "This student ID already exists.")
        return

    new_student = {
        "ID": int(student_id),
        "First Name": first_name,
        "Last Name": last_name,
        "Sex": sex
    }

    absent.append(new_student)
    add_to_undo("add_student", new_student)
    update_display()
    update_json_file()

    new_student_id.delete(0, tk.END)
    new_student_first_name.delete(0, tk.END)
    new_student_last_name.delete(0, tk.END)

    update_student_list_in_edit_window()

def remove_students():
    selected_indices = student_list.curselection()
    selected_students = [student_list.get(i) for i in selected_indices]
    
    for selected_student in selected_students:
        student_id = selected_student.split(" - ")[0]
        student = find_student(student_id, present + absent)
        if student:
            if student in present:
                present.remove(student)
            else:
                absent.remove(student)
            add_to_undo("remove_student", student)
    
    update_display()
    update_json_file()
    update_student_list_in_edit_window()

def update_student_list_in_edit_window():
    student_list.delete(0, tk.END)
    for student in present + absent:
        student_list.insert(tk.END, f"{student['ID']} - {student['First Name']} {student['Last Name']}")

def open_edit_window():
    global edit_window, new_student_id, new_student_first_name, new_student_last_name, new_student_sex, student_list

    root.attributes("-disabled", True)
    
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Students")

    def on_edit_window_close():
        root.attributes("-disabled", False)
        edit_window.destroy()

    edit_window.protocol("WM_DELETE_WINDOW", on_edit_window_close)
    
    tk.Label(edit_window, text="Add New Student").grid(row=0, column=0, columnspan=2)
    tk.Label(edit_window, text="ID:").grid(row=1, column=0)
    new_student_id = tk.Entry(edit_window, validate="key", validatecommand=validate_command)
    new_student_id.grid(row=1, column=1)

    tk.Label(edit_window, text="First Name:").grid(row=2, column=0)
    new_student_first_name = tk.Entry(edit_window)
    new_student_first_name.grid(row=2, column=1)

    tk.Label(edit_window, text="Last Name:").grid(row=3, column=0)
    new_student_last_name = tk.Entry(edit_window)
    new_student_last_name.grid(row=3, column=1)

    tk.Label(edit_window, text="Sex:").grid(row=4, column=0)
    new_student_sex = tk.StringVar(value="Male")

    male_radio = tk.Radiobutton(edit_window, text="Male", variable=new_student_sex, value="Male")
    male_radio.grid(row=4, column=1, sticky='w')

    female_radio = tk.Radiobutton(edit_window, text="Female", variable=new_student_sex, value="Female")
    female_radio.grid(row=5, column=1, sticky='w')
    
    add_button = tk.Button(edit_window, text="Add Student", command=add_student)
    add_button.grid(row=6, column=0, columnspan=2)

    tk.Label(edit_window, text="Remove Student(s)").grid(row=7, column=0, columnspan=2)
    
    student_list = tk.Listbox(edit_window, selectmode=tk.MULTIPLE, width=40, height=10)
    student_list.grid(row=8, column=0, columnspan=2)
    
    update_student_list_in_edit_window()

    remove_button = tk.Button(edit_window, text="Remove Selected", command=remove_students)
    remove_button.grid(row=9, column=0, columnspan=2)

def validate_numeric_input(action, value):
    if action == '1':
        return value.isdigit()
    return True

def save_attendance_file(save_path=None):
    current_date = datetime.now().strftime('%m-%d-%Y')
    file_name = f"{current_date} Attendance.xlsx"
    
    attendance_data = []
    for student in absent:
        attendance_data.append([f"{student['First Name']} {student['Last Name']}", student['ID'], student['Sex'], 'Absent'])
    for student in present:
        attendance_data.append([f"{student['First Name']} {student['Last Name']}", student['ID'], student['Sex'], 'Present'])
    
    df = pd.DataFrame(attendance_data, columns=["Name", "Student ID", "Sex", current_date])
    
    df.sort_values(by=[current_date, 'Sex', 'Name'], ascending=[True, False, True], inplace=True)
    
    if not save_path:
        save_path = os.path.join(os.path.dirname(__file__), file_name)
    
    df.to_excel(save_path, index=False)
    messagebox.showinfo("Saved", f"Attendance saved to {save_path}")

def on_closing():
    if messagebox.askyesno("Save attendance?", "Do you want to save attendance?"):
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            try:
                save_attendance_file(save_path)
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred: {str(e)}. Please save the file manually.")
                return
            if not os.path.exists(save_path):
                messagebox.showerror("Save Error", "File not saved. Please save the file manually.")
                return
        else:
            try:
                save_attendance_file()
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred: {str(e)}. Please save the file manually.")
                return
            if not os.path.exists(os.path.join(os.path.dirname(__file__), f"{datetime.now().strftime('%m-%d-%Y')} Attendance.xlsx")):
                messagebox.showerror("Save Error", "File not saved. Please save the file manually.")
                return
    root.destroy()

root = tk.Tk()
root.title("Student Attendance")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

student_id_label = tk.Label(input_frame, text="Enter Student ID:")
student_id_label.pack(side=tk.LEFT, padx=5)

validate_command = (root.register(validate_numeric_input), '%d', '%P')
student_id_entry = tk.Entry(input_frame, validate="key", validatecommand=validate_command)
student_id_entry.pack(side=tk.LEFT, padx=5)
student_id_entry.bind("<Return>", mark_present)

mark_present_button = tk.Button(input_frame, text="Mark Present", command=mark_present)
mark_present_button.pack(side=tk.LEFT, padx=5)

edit_button = tk.Button(input_frame, text="Edit", command=open_edit_window)
edit_button.pack(side=tk.LEFT, padx=5)

undo_button = tk.Button(input_frame, text="Undo", command=undo)
undo_button.pack(side=tk.LEFT, padx=5)

redo_button = tk.Button(input_frame, text="Redo", command=redo)
redo_button.pack(side=tk.LEFT, padx=5)

display_frame = tk.Frame(root)
display_frame.pack(pady=10)

present_label = tk.Label(display_frame, text="Present Students")
present_label.grid(row=0, column=0, padx=10)

absent_label = tk.Label(display_frame, text="Absent Students")
absent_label.grid(row=0, column=1, padx=10)

present_list = tk.Listbox(display_frame, width=40, height=15)
present_list.grid(row=1, column=0, padx=10, pady=5)
present_list.bind("<Double-Button-1>", move_to_absent)

absent_list = tk.Listbox(display_frame, width=40, height=15)
absent_list.grid(row=1, column=1, padx=10, pady=5)
absent_list.bind("<Double-Button-1>", move_to_present)

update_display()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

log_file_path = os.path.join(os.path.dirname(__file__), 'log.txt')
with open(log_file_path, 'w') as file:
    file.write("Present:\n" + str(present) + "\n\nAbsent:\n" + str(absent))