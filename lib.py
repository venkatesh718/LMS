import sqlite3
import tkinter as tk
from tkinter import messagebox

# Initialize the Database
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            available INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()


# Add a Book
def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    year = entry_year.get().strip()

    if title and author and year.isdigit():
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, int(year)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book added successfully!")
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        view_books()
    else:
        messagebox.showerror("Error", "Please enter valid book details.")


# View All Books
def view_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    listbox_books.delete(0, tk.END)
    for row in rows:
        status = "Available" if row[4] else "Borrowed"
        listbox_books.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {status}")


# Search Books and Select First Match
def search_books():
    search_query = entry_search.get().strip()

    if not search_query:
        messagebox.showerror("Error", "Please enter a book title, author, or year to search.")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year LIKE ?",
                   ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    rows = cursor.fetchall()
    conn.close()

    listbox_books.delete(0, tk.END)

    if rows:
        for row in rows:
            status = "Available" if row[4] else "Borrowed"
            listbox_books.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {status}")

        # Select the first matching book
        listbox_books.selection_set(0)
        listbox_books.activate(0)
        listbox_books.see(0)

        messagebox.showinfo("Success", f"Found {len(rows)} book(s) matching '{search_query}'")
    else:
        messagebox.showwarning("Not Found", f"No books found matching '{search_query}'")


# Borrow a Book
def borrow_book():
    try:
        selected = listbox_books.get(listbox_books.curselection())
        book_id = selected.split(" | ")[0]

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET available = 0 WHERE id = ? AND available = 1", (book_id,))
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Book borrowed successfully!")
        else:
            messagebox.showwarning("Warning", "Book is already borrowed!")
        conn.commit()
        conn.close()
        view_books()
    except:
        messagebox.showerror("Error", "Please select a book to borrow.")


# Return a Book
def return_book():
    try:
        selected = listbox_books.get(listbox_books.curselection())
        book_id = selected.split(" | ")[0]

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book returned successfully!")
        view_books()
    except:
        messagebox.showerror("Error", "Please select a book to return.")


# Delete a Book
def delete_book():
    try:
        selected = listbox_books.get(listbox_books.curselection())
        book_id = selected.split(" | ")[0]

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book deleted successfully!")
        view_books()
    except:
        messagebox.showerror("Error", "Please select a book to delete.")


# GUI Setup
root = tk.Tk()
root.title("Library Management System")

# Input Fields
tk.Label(root, text="Title").grid(row=0, column=0)
entry_title = tk.Entry(root)
entry_title.grid(row=0, column=1)

tk.Label(root, text="Author").grid(row=1, column=0)
entry_author = tk.Entry(root)
entry_author.grid(row=1, column=1)

tk.Label(root, text="Year").grid(row=2, column=0)
entry_year = tk.Entry(root)
entry_year.grid(row=2, column=1)

# Buttons
tk.Button(root, text="Add Book", command=add_book).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Borrow Book", command=borrow_book).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Return Book", command=return_book).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Delete Book", command=delete_book).grid(row=6, column=0, columnspan=2)

# Search Field
tk.Label(root, text="Search").grid(row=7, column=0)
entry_search = tk.Entry(root)
entry_search.grid(row=7, column=1)
tk.Button(root, text="Search", command=search_books).grid(row=7, column=2)

# Books List
listbox_books = tk.Listbox(root, width=50, height=10)
listbox_books.grid(row=8, column=0, columnspan=3)

# Initialize Database and Load Books
init_db()
view_books()

# Run the Application
root.mainloop()
