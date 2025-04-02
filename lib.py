import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")

        # Initialize database
        self.init_database()

        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Books tab
        self.books_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.books_frame, text="Books")
        self.setup_books_tab()

        # Members tab
        self.members_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.members_frame, text="Members")
        self.setup_members_tab()

        # Loans tab
        self.loans_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.loans_frame, text="Loans")
        self.setup_loans_tab()

    def init_database(self):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # Create tables
        c.execute('''CREATE TABLE IF NOT EXISTS books
                    (id INTEGER PRIMARY KEY,
                     title TEXT NOT NULL,
                     author TEXT NOT NULL,
                     quantity INTEGER)''')

        c.execute('''CREATE TABLE IF NOT EXISTS members
                    (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     email TEXT UNIQUE,
                     phone TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS loans
                    (id INTEGER PRIMARY KEY,
                     book_id INTEGER,
                     member_id INTEGER,
                     loan_date TEXT,
                     return_date TEXT,
                     returned INTEGER DEFAULT 0,
                     FOREIGN KEY (book_id) REFERENCES books (id),
                     FOREIGN KEY (member_id) REFERENCES members (id))''')

        conn.commit()
        conn.close()

    def setup_books_tab(self):
        # Book entry frame
        entry_frame = ttk.LabelFrame(self.books_frame, text="Add New Book")
        entry_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(entry_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(entry_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Author:").grid(row=0, column=2, padx=5, pady=5)
        self.author_entry = ttk.Entry(entry_frame)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(entry_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(entry_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(entry_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected Book", command=self.delete_book).pack(side=tk.LEFT, padx=5)

        # Books list
        list_frame = ttk.LabelFrame(self.books_frame, text="Books List")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.books_tree = ttk.Treeview(list_frame, columns=("ID", "Title", "Author", "Quantity"), show="headings")
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("Quantity", text="Quantity")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)

        self.books_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_books()

    def setup_members_tab(self):
        # Member entry frame
        entry_frame = ttk.LabelFrame(self.members_frame, text="Add New Member")
        entry_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(entry_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.member_name_entry = ttk.Entry(entry_frame)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5)
        self.member_email_entry = ttk.Entry(entry_frame)
        self.member_email_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(entry_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.member_phone_entry = ttk.Entry(entry_frame)
        self.member_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(entry_frame, text="Add Member", command=self.add_member).grid(row=2, column=0, pady=10)
        ttk.Button(entry_frame, text="Delete Selected Member", command=self.delete_member).grid(row=2, column=1,
                                                                                                pady=10)

        # Members list
        list_frame = ttk.LabelFrame(self.members_frame, text="Members List")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.members_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.members_tree.heading("ID", text="ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Email", text="Email")
        self.members_tree.heading("Phone", text="Phone")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)

        self.members_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_members()

    def setup_loans_tab(self):
        # Loan entry frame
        entry_frame = ttk.LabelFrame(self.loans_frame, text="New Loan")
        entry_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(entry_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        self.loan_book_entry = ttk.Entry(entry_frame)
        self.loan_book_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Member ID:").grid(row=0, column=2, padx=5, pady=5)
        self.loan_member_entry = ttk.Entry(entry_frame)
        self.loan_member_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(entry_frame, text="Create Loan", command=self.create_loan).grid(row=1, column=0, columnspan=2,
                                                                                   pady=10)
        ttk.Button(entry_frame, text="Return Book", command=self.return_book).grid(row=1, column=2, columnspan=2,
                                                                                   pady=10)

        # Loans list
        list_frame = ttk.LabelFrame(self.loans_frame, text="Active Loans")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.loans_tree = ttk.Treeview(list_frame,
                                       columns=("ID", "Book", "Member", "Loan Date", "Return Date", "Status"),
                                       show="headings")
        self.loans_tree.heading("ID", text="ID")
        self.loans_tree.heading("Book", text="Book")
        self.loans_tree.heading("Member", text="Member")
        self.loans_tree.heading("Loan Date", text="Loan Date")
        self.loans_tree.heading("Return Date", text="Return Date")
        self.loans_tree.heading("Status", text="Status")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.loans_tree.yview)
        self.loans_tree.configure(yscrollcommand=scrollbar.set)

        self.loans_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_loans()

    def add_book(self):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
                      (self.title_entry.get(), self.author_entry.get(), self.quantity_entry.get()))
            conn.commit()
            conn.close()
            self.refresh_books()
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_book_entries()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def delete_book(self):
        try:
            selected_item = self.books_tree.selection()[0]
            book_id = self.books_tree.item(selected_item)['values'][0]

            # Check if book has any active loans
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM loans WHERE book_id = ? AND returned = 0", (book_id,))
            active_loans = c.fetchone()[0]

            if active_loans > 0:
                messagebox.showerror("Error", "Cannot delete book with active loans!")
                conn.close()
                return

            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
                c.execute("DELETE FROM books WHERE id = ?", (book_id,))
                conn.commit()
                conn.close()
                self.refresh_books()
                messagebox.showinfo("Success", "Book deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select a book to delete")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

    def add_member(self):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO members (name, email, phone) VALUES (?, ?, ?)",
                      (self.member_name_entry.get(), self.member_email_entry.get(), self.member_phone_entry.get()))
            conn.commit()
            conn.close()
            self.refresh_members()
            messagebox.showinfo("Success", "Member added successfully!")
            self.clear_member_entries()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add member: {str(e)}")

    def delete_member(self):
        try:
            selected_item = self.members_tree.selection()[0]
            member_id = self.members_tree.item(selected_item)['values'][0]

            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            # Check if member has any active loans
            c.execute("SELECT COUNT(*) FROM loans WHERE member_id = ? AND returned = 0", (member_id,))
            active_loans = c.fetchone()[0]

            if active_loans > 0:
                messagebox.showerror("Error", "Cannot delete member with active loans!")
                conn.close()
                return

            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?"):
                c.execute("DELETE FROM members WHERE id = ?", (member_id,))
                conn.commit()
                conn.close()
                self.refresh_members()
                messagebox.showinfo("Success", "Member deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select a member to delete")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to delete member: {str(e)}")

    def create_loan(self):
        try:
            book_id = self.loan_book_entry.get()
            member_id = self.loan_member_entry.get()
            loan_date = datetime.now().strftime("%Y-%m-%d")
            return_date = None  # Can be implemented with a calendar widget

            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (?, ?, ?, ?)",
                      (book_id, member_id, loan_date, return_date))
            conn.commit()
            conn.close()
            self.refresh_loans()
            messagebox.showinfo("Success", "Loan created successfully!")
            self.clear_loan_entries()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to create loan: {str(e)}")

    def return_book(self):
        try:
            selected_item = self.loans_tree.selection()[0]
            loan_id = self.loans_tree.item(selected_item)['values'][0]

            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("UPDATE loans SET returned = 1, return_date = ? WHERE id = ?",
                      (datetime.now().strftime("%Y-%m-%d"), loan_id))
            conn.commit()
            conn.close()
            self.refresh_loans()
            messagebox.showinfo("Success", "Book returned successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select a loan to return")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def refresh_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")  # Ensure quantity column is fetched
        rows = c.fetchall()

        print("Books Data from Database:")
        for row in rows:
            print(row)  # Debug print to check if quantity exists
            self.books_tree.insert("", "end", values=row)  # Insert into treeview

        conn.close()

    def refresh_members(self):
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM members")
        for row in c.fetchall():
            self.members_tree.insert("", "end", values=row)
        conn.close()

    def refresh_loans(self):
        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("""
            SELECT l.id, b.title, m.name, l.loan_date, l.return_date,
                   CASE WHEN l.returned = 1 THEN 'Returned' ELSE 'Active' END as status
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN members m ON l.member_id = m.id
        """)
        for row in c.fetchall():
            self.loans_tree.insert("", "end", values=row)
        conn.close()

    def clear_book_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def clear_member_entries(self):
        self.member_name_entry.delete(0, tk.END)
        self.member_email_entry.delete(0, tk.END)
        self.member_phone_entry.delete(0, tk.END)

    def clear_loan_entries(self):
        self.loan_book_entry.delete(0, tk.END)
        self.loan_member_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()