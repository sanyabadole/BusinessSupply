#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime
from procedures.add_owner import add_owner as add_owner_proc
from procedures.add_employee import add_employee as add_employee_proc
from procedures.add_worker_role import add_worker_role as add_worker_role_proc
from procedures.add_driver_role import add_driver_role as add_driver_role_proc
from procedures.add_product import add_product as add_product_proc
from procedures.add_business import add_business as add_business_proc
from procedures.add_van import add_van as add_van_proc
from procedures.add_location import add_location as add_location_proc
from procedures.start_funding import start_funding as start_funding_proc
from procedures.hire_employee import hire_employee as hire_employee_proc
from procedures.fire_employee import fire_employee as fire_employee_proc
from procedures.manage_service import manage_service as manage_service_proc
from procedures.takeover_van import takeover_van as takeover_van_proc
from procedures.add_service import add_service as add_service_proc
from procedures.load_van import load_van as load_van_proc
from procedures.refuel_van import refuel_van as refuel_van_proc
from procedures.drive_van import drive_van as drive_van_proc
from procedures.purchase_product import purchase_product as purchase_product_proc
from procedures.remove_driver_role import remove_driver_role as remove_driver_role_proc
from procedures.remove_product import remove_product as remove_product_proc
from procedures.remove_van import remove_van as remove_van_proc

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.style = ttk.Style()
        self.style.configure('Modern.TButton', padding=10, font=('Helvetica', 10))
        self.configure(style='Modern.TButton')

    def on_enter(self, e):
        self.style.configure('Modern.TButton', background='#4a90e2')
        self.configure(style='Modern.TButton')

    def on_leave(self, e):
        self.style.configure('Modern.TButton', background='#357abd')
        self.configure(style='Modern.TButton')

class BusinessSupplyCombinedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Supply Management System")
        self.root.geometry("1200x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TNotebook.Tab', padding=[10, 5], font=('Helvetica', 10))
        self.style.configure('Treeview', background='white', fieldbackground='white', font=('Helvetica', 10))
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(expand=True, fill='both')
        
        # Initialize database connection
        self.init_db()
        
        # Create main menu buttons
        self.create_main_menu()
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Create frames
        self.create_views_frame()
        self.create_procedures_frame()

    def init_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="Bear@6833",
                database="business_supply"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Could not connect to database: {err}")

    def create_main_menu(self):
        # Title with modern styling
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=(0, 30))
        
        title_label = ttk.Label(title_frame, 
                              text="Business Supply Management System",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                 text="Manage your business operations efficiently",
                                 font=('Helvetica', 12))
        subtitle_label.pack(pady=(5, 0))
        
        # Menu buttons with modern styling
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ModernButton(button_frame, 
                    text="View Data",
                    command=lambda: self.show_frame("views")).pack(pady=10, fill='x', padx=20)
        
        ModernButton(button_frame,
                    text="Manage Data",
                    command=lambda: self.show_frame("procedures")).pack(pady=10, fill='x', padx=20)

    def create_views_frame(self):
        views_frame = ttk.Frame(self.root, padding="20")
        self.frames["views"] = views_frame
        
        # Title for views section
        ttk.Label(views_frame, 
                 text="Data Views",
                 font=('Helvetica', 18, 'bold')).pack(pady=(0, 20))
        
        notebook = ttk.Notebook(views_frame)
        notebook.pack(expand=True, fill='both')
        
        views = {
            'display_owner_view': ['Username', 'First Name', 'Last Name', 'Address', 'Businesses'],
            'display_employee_view': ['Username', 'TaxID', 'Salary', 'Hired', 'Experience'],
            'display_driver_view': ['Username', 'LicenseID', 'Successful Trips', 'Number of Vans'],
            'display_location_view': ['Label', 'Long name', 'X Coordinate', 'Y Coordinate', 'Space', 'Number of Vans', 'Van IDs', 'Remaining Capacity'],
            'display_product_view': ['Product Name', 'Location', 'Amount Available', 'Low Price', 'High Price'],
            'display_service_view': ['ID', 'Long Name', 'Home Base', 'Manager Name', 'Revenue']
        }
        
        for view_name, columns in views.items():
            tab = ttk.Frame(notebook, padding="10")
            notebook.add(tab, text=view_name.replace('display_', '').replace('_view', '').title())
            
            # Create a frame for the tree and scrollbar
            tree_frame = ttk.Frame(tab)
            tree_frame.pack(expand=True, fill='both')
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side='right', fill='y')
            
            # Create treeview with scrollbar
            tree = ttk.Treeview(tab, columns=columns, show='headings', yscrollcommand=scrollbar.set)
            scrollbar.config(command=tree.yview)
            
            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')
            
            tree.pack(expand=True, fill='both')
            
            # Add refresh button with modern styling
            ModernButton(tab, 
                        text="Refresh Data",
                        command=lambda t=tree, c=columns, n=view_name: 
                        self.refresh_view(n, t, c)).pack(pady=10)
        
        # Back button with modern styling
        ModernButton(views_frame,
                    text="Back to Main Menu",
                    command=lambda: self.show_frame("main")).pack(pady=20)

    def create_procedures_frame(self):
        procedures_frame = ttk.Frame(self.root, padding="20")
        self.frames["procedures"] = procedures_frame
        
        # Title for procedures section
        ttk.Label(procedures_frame,
                 text="Data Management",
                 font=('Helvetica', 18, 'bold')).pack(pady=(0, 20))
        
        notebook = ttk.Notebook(procedures_frame)
        notebook.pack(expand=True, fill='both')
        
        # User Management Tab
        user_tab = ttk.Frame(notebook, padding="20")
        notebook.add(user_tab, text="User Management")
        self.create_procedure_buttons(user_tab, [
            ("Add Owner", "add_owner"),
            ("Add Employee", "add_employee"),
            ("Add Driver Role", "add_driver_role"),
            ("Add Worker Role", "add_worker_role"),
            ("Remove Driver Role", "remove_driver_role")
        ])

        # Product Management Tab
        product_tab = ttk.Frame(notebook, padding="20")
        notebook.add(product_tab, text="Product Management")
        self.create_procedure_buttons(product_tab, [
            ("Add Product", "add_product"),
            ("Remove Product", "remove_product"),
            ("Purchase Product", "purchase_product")
        ])

        # Van Management Tab
        van_tab = ttk.Frame(notebook, padding="20")
        notebook.add(van_tab, text="Van Management")
        self.create_procedure_buttons(van_tab, [
            ("Add Van", "add_van"),
            ("Remove Van", "remove_van"),
            ("Load Van", "load_van"),
            ("Drive Van", "drive_van"),
            ("Refuel Van", "refuel_van"),
            ("Takeover Van", "takeover_van")
        ])

        # Business Management Tab
        business_tab = ttk.Frame(notebook, padding="20")
        notebook.add(business_tab, text="Business Management")
        self.create_procedure_buttons(business_tab, [
            ("Add Business", "add_business"),
            ("Add Service", "add_service"),
            ("Add Location", "add_location"),
            ("Start Funding", "start_funding"),
            ("Hire Employee", "hire_employee"),
            ("Fire Employee", "fire_employee"),
            ("Manage Service", "manage_service")
        ])

        # Back button with modern styling
        ModernButton(procedures_frame,
                    text="Back to Main Menu",
                    command=lambda: self.show_frame("main")).pack(pady=20)

    def create_procedure_buttons(self, parent, procedures):
        for proc_name, proc_cmd in procedures:
            ModernButton(parent,
                        text=proc_name,
                        command=lambda cmd=proc_cmd: self.execute_procedure(cmd)).pack(pady=5, fill='x')

    def show_frame(self, frame_name):
        self.main_frame.pack_forget()
        for frame in self.frames.values():
            frame.pack_forget()
            
        if frame_name == "main":
            self.main_frame.pack(expand=True, fill='both')
        else:
            self.frames[frame_name].pack(expand=True, fill='both')

    def refresh_view(self, view_name, tree, columns):
        for item in tree.get_children():
            tree.delete(item)
        try:
            self.cursor.execute(f"SELECT * FROM {view_name}")
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Query Error", f"Error refreshing view: {err}")

    def add_owner(self, **kwargs):
        try:
            result = add_owner_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_employee(self, **kwargs):
        try:
            result = add_employee_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def add_worker_role(self, **kwargs):
        try:
            result = add_worker_role_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_driver_role(self, **kwargs):
        try:
            result = add_driver_role_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_product(self, **kwargs):
        try:
            result = add_product_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_business(self, **kwargs):
        try:
            result = add_business_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_van(self, **kwargs):
        try:
            result = add_van_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_location(self, **kwargs):
        try:
            result = add_location_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def start_funding(self, **kwargs):
        try:
            result = start_funding_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def hire_employee(self, **kwargs):
        try:
            result = hire_employee_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fire_employee(self, **kwargs):
        try:
            result = fire_employee_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def manage_service(self, **kwargs):
        try:
            result = manage_service_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def takeover_van(self, **kwargs):
        try:
            result = takeover_van_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def add_service(self, **kwargs):
        try:
            result = add_service_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def load_van(self, **kwargs):
        try:
            result = load_van_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def refuel_van(self, **kwargs):
        try:
            result = refuel_van_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def drive_van(self, **kwargs):
        try:
            result = drive_van_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def purchase_product(self, **kwargs):
        try:
            result = purchase_product_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        
    def remove_driver_role(self, **kwargs):
        try:
            result = remove_driver_role_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def remove_product(self, **kwargs):
        try:
            result = remove_product_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def remove_van(self, **kwargs):
        try:
            result = remove_van_proc(self.cursor, self.conn, **kwargs)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def execute_procedure(self, procedure_name):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Execute {procedure_name}")
        dialog.geometry("400x500")

        inputs = {}
        
        if procedure_name == "add_owner":
            fields = ["username", "first_name", "last_name", "address", "birthdate"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "add_employee":
            fields = ["username", "first_name", "last_name", "address", "birthdate",
                      "taxID", "hired", "experience", "salary"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "add_worker_role":
            fields = ["username"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "add_driver_role":
            fields = ["username", "licenseID", "license_type", "driver_experience"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "add_product":
            fields = ["barcode", "name", "weight"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "add_business":
            fields = ["long_name", "rating", "spent", "location"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "add_van":
            fields = ["id", "tag", "fuel", "capacity", "sales", "driven_by"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "add_location":
            fields = ["label", "x_coord", "y_coord", "space"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "start_funding":
            fields = ["owner", "amount", "long_name", 'fund_date']
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "hire_employee":
            fields = ["username", "id"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "fire_employee":
            fields = ["username", "id"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "manage_service":
            fields = ["username", "service_id"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "takeover_van":
            fields = ["username", "service_id", "van_tag"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "add_service":
            fields = ["id", "long_name", "home_base", "manager"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "load_van":
            fields = ["id", "tag", "barcode", "more_packages", "price"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "refuel_van":
            fields = ["id", "tag", "more_fuel"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "drive_van":
            fields = ["id", "tag", "destination"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        if procedure_name == "purchase_product":
            fields = ["long_name", "id", "tag", "barcode", "quantity"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "remove_driver_role":
            fields = ["username"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "remove_product":
            fields = ["barcode"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()
        
        if procedure_name == "remove_van":
            fields = ["id", "tag"]
            for field in fields:
                tk.Label(dialog, text=field.replace("_", " ")).pack()
                inputs[field] = tk.Entry(dialog)
                inputs[field].pack()

        def run_procedure():
            try:
                if procedure_name == "add_owner":
                    self.add_owner(**{k: v.get().strip() for k, v in inputs.items()})
                # Add more elif statements for other procedures
                if procedure_name == "add_employee":
                    self.add_employee(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "add_worker_role":
                    self.add_worker_role(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "add_driver_role":
                    self.add_driver_role(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "add_product":
                    self.add_product(**{k: v.get().strip() for k, v in inputs.items()})  
                if procedure_name == "add_business":
                    self.add_business(**{k: v.get().strip() for k, v in inputs.items()})  
                if procedure_name == "add_van":
                    self.add_van(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "add_location":
                    self.add_location(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "start_funding":
                    self.start_funding(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "hire_employee":
                    self.hire_employee(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "fire_employee":
                    self.fire_employee(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "manage_service":
                    self.manage_service(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "takeover_van":
                    self.takeover_van(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "add_service":
                    self.add_service(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "load_van":
                    self.load_van(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "refuel_van":
                    self.refuel_van(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "drive_van":
                    self.drive_van(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "purchase_product":
                    self.purchase_product(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "remove_driver_role":
                    self.remove_driver_role(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "remove_product":
                    self.remove_product(**{k: v.get().strip() for k, v in inputs.items()})
                if procedure_name == "remove_van":
                    self.remove_van(**{k: v.get().strip() for k, v in inputs.items()})
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Execute", command=run_procedure).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessSupplyCombinedGUI(root)
    root.mainloop() 