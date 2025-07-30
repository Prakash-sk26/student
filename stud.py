import sqlite3
from tkinter import *
from tkinter import messagebox
import re

def connect_db():
    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                course TEXT,
                email TEXT
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def insert_data(name, age, course, email):
    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO student (name, age, course, email) VALUES (?, ?, ?, ?)", (name, age, course, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student Added")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def view_all():
    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def delete_data(student_id):
    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", f"Student ID {student_id} deleted")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def update_data(student_id, name, age, course, email):
    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("""
            UPDATE student
            SET name = ?, age = ?, course = ?, email = ?
            WHERE id = ?
        """, (name, age, course, email, student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", f"Student ID {student_id} updated")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

def main_window():
    connect_db()
    root = Tk()
    root.title("Student Registration System")
    root.geometry("600x600")
    root.config(bg="#f4f4f9")

    # Frame for better organization
    frame = Frame(root, bg="#f4f4f9")
    frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

    # Title Label
    title_label = Label(frame, text="Student Registration", font=("Arial", 20, "bold"), bg="#f4f4f9", fg="#3e8e41")
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Labels & Entry
    Label(frame, text="Name", font=("Arial", 12), bg="#f4f4f9").grid(row=1, column=0, sticky=W, pady=5, padx=10)
    name_entry = Entry(frame, font=("Arial", 12))
    name_entry.grid(row=1, column=1, pady=5, padx=10)

    Label(frame, text="Age", font=("Arial", 12), bg="#f4f4f9").grid(row=2, column=0, sticky=W, pady=5, padx=10)
    age_entry = Entry(frame, font=("Arial", 12))
    age_entry.grid(row=2, column=1, pady=5, padx=10)

    Label(frame, text="Course", font=("Arial", 12), bg="#f4f4f9").grid(row=3, column=0, sticky=W, pady=5, padx=10)
    course_entry = Entry(frame, font=("Arial", 12))
    course_entry.grid(row=3, column=1, pady=5, padx=10)

    Label(frame, text="Email", font=("Arial", 12), bg="#f4f4f9").grid(row=4, column=0, sticky=W, pady=5, padx=10)
    email_entry = Entry(frame, font=("Arial", 12))
    email_entry.grid(row=4, column=1, pady=5, padx=10)

    # Add Student Button
    def add_student():
        try:
            name = name_entry.get().strip()
            age = int(age_entry.get().strip())  # Convert to integer
            course = course_entry.get().strip()
            email = email_entry.get().strip()

            # Validate the email format
            if not validate_email(email):
                messagebox.showerror("Invalid Email", "Please enter a valid email address.")
                return

            insert_data(name, age, course, email)
        except ValueError:
            messagebox.showerror("Invalid Age", "Please enter a valid age as a number.")

    add_button = Button(frame, text="Add Student", font=("Arial", 12), command=add_student, bg="#4CAF50", fg="white", relief=RAISED)
    add_button.grid(row=5, column=1, pady=10)

    # View All Button
    def show_students():
        records = view_all()
        output.delete(1.0, END)
        for rec in records:
            output.insert(END, f"{rec}\n")

    view_button = Button(frame, text="View Students", font=("Arial", 12), command=show_students, bg="#2196F3", fg="white", relief=RAISED)
    view_button.grid(row=6, column=1, pady=10)

    # Delete by ID
    Label(frame, text="Delete ID", font=("Arial", 12), bg="#f4f4f9").grid(row=7, column=0, sticky=W, pady=5, padx=10)
    delete_entry = Entry(frame, font=("Arial", 12))
    delete_entry.grid(row=7, column=1, pady=5, padx=10)

    delete_button = Button(frame, text="Delete Student", font=("Arial", 12), command=lambda: delete_data(delete_entry.get()), bg="#f44336", fg="white", relief=RAISED)
    delete_button.grid(row=8, column=1, pady=10)

    # Update by ID
    Label(frame, text="Update ID", font=("Arial", 12), bg="#f4f4f9").grid(row=9, column=0, sticky=W, pady=5, padx=10)
    update_id_entry = Entry(frame, font=("Arial", 12))
    update_id_entry.grid(row=9, column=1, pady=5, padx=10)

    Label(frame, text="New Name", font=("Arial", 12), bg="#f4f4f9").grid(row=10, column=0, sticky=W, pady=5, padx=10)
    update_name_entry = Entry(frame, font=("Arial", 12))
    update_name_entry.grid(row=10, column=1, pady=5, padx=10)

    Label(frame, text="New Age", font=("Arial", 12), bg="#f4f4f9").grid(row=11, column=0, sticky=W, pady=5, padx=10)
    update_age_entry = Entry(frame, font=("Arial", 12))
    update_age_entry.grid(row=11, column=1, pady=5, padx=10)

    Label(frame, text="New Course", font=("Arial", 12), bg="#f4f4f9").grid(row=12, column=0, sticky=W, pady=5, padx=10)
    update_course_entry = Entry(frame, font=("Arial", 12))
    update_course_entry.grid(row=12, column=1, pady=5, padx=10)

    Label(frame, text="New Email", font=("Arial", 12), bg="#f4f4f9").grid(row=13, column=0, sticky=W, pady=5, padx=10)
    update_email_entry = Entry(frame, font=("Arial", 12))
    update_email_entry.grid(row=13, column=1, pady=5, padx=10)

    def update_student():
        try:
            student_id = int(update_id_entry.get().strip())
            name = update_name_entry.get().strip()
            age = int(update_age_entry.get().strip())
            course = update_course_entry.get().strip()
            email = update_email_entry.get().strip()

            if not validate_email(email):
                messagebox.showerror("Invalid Email", "Please enter a valid email address.")
                return

            update_data(student_id, name, age, course, email)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure all fields are filled correctly.")

    update_button = Button(frame, text="Update Student", font=("Arial", 12), command=update_student, bg="#FF9800", fg="white", relief=RAISED)
    update_button.grid(row=14, column=1, pady=10)

    # Output Text Box
    output = Text(frame, height=10, width=50, font=("Arial", 12), wrap=WORD)
    output.grid(row=15, column=0, columnspan=2, pady=10, padx=10)

    root.mainloop()

main_window()
