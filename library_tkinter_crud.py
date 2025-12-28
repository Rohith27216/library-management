import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

DATA_FILE = "library_data.json"


# ---------------------------------------------------------
# Load & Save Data
# ---------------------------------------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"books": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------
# GUI Application
# ---------------------------------------------------------
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - CRUD")
        self.root.geometry("700x500")

        self.data = load_data()

        # Entry fields
        tk.Label(root, text="Book ID").place(x=40, y=20)
        self.book_id = tk.Entry(root, width=30)
        self.book_id.place(x=150, y=20)

        tk.Label(root, text="Title").place(x=40, y=60)
        self.title = tk.Entry(root, width=30)
        self.title.place(x=150, y=60)

        tk.Label(root, text="Author").place(x=40, y=100)
        self.author = tk.Entry(root, width=30)
        self.author.place(x=150, y=100)

        # Buttons
        tk.Button(root, text="Add Book", width=12, command=self.create_book).place(x=40, y=150)
        tk.Button(root, text="Update Book", width=12, command=self.update_book).place(x=150, y=150)
        tk.Button(root, text="Delete Book", width=12, command=self.delete_book).place(x=260, y=150)
        tk.Button(root, text="Clear Fields", width=12, command=self.clear_fields).place(x=370, y=150)

        # Table
        self.tree = ttk.Treeview(root, columns=("ID", "Title", "Author"), show="headings")
        self.tree.heading("ID", text="Book ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")

        self.tree.place(x=40, y=220, width=620, height=250)

        self.tree.bind("<ButtonRelease-1>", self.select_book)

        self.refresh_table()

    # -----------------------------------------------------
    # CRUD FUNCTIONS
    # -----------------------------------------------------
    def create_book(self):
        book_id = self.book_id.get()
        title = self.title.get()
        author = self.author.get()

        if not book_id or not title or not author:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        # Check duplicate ID
        for book in self.data["books"]:
            if book["id"] == book_id:
                messagebox.showerror("Error", "Book ID already exists!")
                return

        self.data["books"].append({
            "id": book_id,
            "title": title,
            "author": author
        })

        save_data(self.data)
        messagebox.showinfo("Success", "Book added!")
        self.refresh_table()
        self.clear_fields()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in self.data["books"]:
            self.tree.insert("", tk.END, values=(book["id"], book["title"], book["author"]))

    def select_book(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")
        if values:
            self.book_id.delete(0, tk.END)
            self.title.delete(0, tk.END)
            self.author.delete(0, tk.END)

            self.book_id.insert(0, values[0])
            self.title.insert(0, values[1])
            self.author.insert(0, values[2])

    def update_book(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a book to update!")
            return

        book_id = self.book_id.get()
        title = self.title.get()
        author = self.author.get()

        for book in self.data["books"]:
            if book["id"] == book_id:
                book["title"] = title
                book["author"] = author
                save_data(self.data)
                messagebox.showinfo("Success", "Book updated!")
                self.refresh_table()
                return

        messagebox.showerror("Error", "Book not found!")

    def delete_book(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a book to delete!")
            return

        values = self.tree.item(selected, "values")
        book_id = values[0]

        for book in self.data["books"]:
            if book["id"] == book_id:
                self.data["books"].remove(book)
                save_data(self.data)
                messagebox.showinfo("Success", "Book deleted!")
                self.refresh_table()
                self.clear_fields()
                return

    def clear_fields(self):
        self.book_id.delete(0, tk.END)
        self.title.delete(0, tk.END)
        self.author.delete(0, tk.END)


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

