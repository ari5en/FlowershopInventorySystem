import tkinter as tk
from tkinter import ttk, messagebox
from flower_dao import *
from category_dao import *
from supplier_dao import *


class FlowerShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Flower Shop Inventory System 🌸")
        self.root.geometry("1000x650")
        self.root.configure(bg="#E3F2FD")

        # Selected IDs
        self.selected_flower_id = None
        self.selected_category_id = None
        self.selected_supplier_id = None

        # Mapping names to IDs
        self.cat_map, self.cat_reverse = {}, {}
        self.sup_map, self.sup_reverse = {}, {}

        self.style_widgets()
        self.create_widgets()
        self.load_categories()
        self.load_categories_table()
        self.load_suppliers()
        self.load_suppliers_to_combo()
        self.load_flowers()

    # ----------------------------
    # Styling
    # ----------------------------
    def style_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#0D47A1", rowheight=26)
        style.configure("Treeview.Heading", background="#42A5F5", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#90CAF9")], foreground=[("selected", "white")])
        style.configure("TCombobox", padding=5)

    def hover_button(self, btn, enter=True):
        btn["background"] = "#64B5F6" if enter else "#90CAF9"

    # ----------------------------
    # GUI Components
    # ----------------------------
    def create_widgets(self):
        tk.Label(self.root, text="FLOWER INVENTORY MANAGER",
                 bg="#E3F2FD", fg="#0D47A1", font=("Segoe UI", 20, "bold")).pack(pady=10)

        self.tab_control = ttk.Notebook(self.root)
        self.tab_categories = ttk.Frame(self.tab_control)
        self.tab_flowers = ttk.Frame(self.tab_control)
        self.tab_supplier = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_flowers, text="Flower")
        self.tab_control.add(self.tab_categories, text="Category")
        self.tab_control.add(self.tab_supplier, text="Supplier")

        self.tab_control.pack(expand=1, fill="both")

        self.create_category_tab()
        self.create_flower_tab()
        self.create_supplier_tab()

    # ----------------------------
    # Category Tab
    # ----------------------------
    def create_category_tab(self):
        frame = self.tab_categories
        form_frame = tk.LabelFrame(frame, text="🌼 Category Details 🌼",
                                   bg="#BBDEFB", fg="#0D47A1",
                                   font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        form_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(form_frame, text="Category Name:", bg="#BBDEFB", fg="#0D47A1",
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=3)
        self.cat_name_var = tk.Entry(form_frame, width=40)
        self.cat_name_var.grid(row=0, column=1, pady=3)

        tk.Label(form_frame, text="Description:", bg="#BBDEFB", fg="#0D47A1",
                 font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=3)
        self.cat_desc_var = tk.Entry(form_frame, width=40)
        self.cat_desc_var.grid(row=1, column=1, pady=3)

        # Buttons
        btn_frame = tk.Frame(frame, bg="#E3F2FD")
        btn_frame.pack(pady=10)
        buttons = [
            ("Add Category", self.add_category),
            ("Update Category", self.update_category),
            ("Delete Category", self.delete_category),
            ("Clear", self.clear_category_form)
        ]
        for i, (txt, cmd) in enumerate(buttons):
            b = tk.Button(btn_frame, text=txt, command=cmd,
                          width=16, bg="#90CAF9", fg="#0D47A1",
                          font=("Segoe UI", 10, "bold"), bd=2, relief="raised",
                          activebackground="#64B5F6", cursor="hand2")
            b.grid(row=0, column=i, padx=10)
            b.bind("<Enter>", lambda e, btn=b: self.hover_button(btn, True))
            b.bind("<Leave>", lambda e, btn=b: self.hover_button(btn, False))

        # Treeview
        table_frame = tk.Frame(frame, bg="#BBDEFB", bd=2, relief="groove")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)
        self.cat_tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Description"), show="headings")
        for col in ("ID", "Name", "Description"):
            self.cat_tree.heading(col, text=col)
            self.cat_tree.column(col, width=200)
        self.cat_tree.pack(fill="both", expand=True)
        self.cat_tree.bind("<<TreeviewSelect>>", self.fill_category_form)

    # ----------------------------
    # Flower Tab
    # ----------------------------
    def create_flower_tab(self):
        frame = self.tab_flowers

        # Search
        search_frame = tk.Frame(frame, bg="#e3f2fd")
        search_frame.pack(fill="x", padx=15, pady=5)
        tk.Label(search_frame, text="Search:", bg="#e3f2fd", fg="#0d47a1",
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.search_var = tk.Entry(search_frame, width=40)
        self.search_var.pack(side="left", padx=5)
        tk.Button(search_frame, text="Find", command=self.search_flower,
                  bg="#90caf9", fg="#0d47a1", width=10).pack(side="left", padx=5)
        tk.Button(search_frame, text="Clear Search", command=self.load_flowers,
                  bg="#bbdefb", fg="#0d47a1", width=12).pack(side="left", padx=5)

        # Form
        form_frame = tk.LabelFrame(frame, text="🌼 Flower Details 🌼",
                                   bg="#BBDEFB", fg="#0D47A1",
                                   font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        form_frame.pack(fill="x", padx=15)

        labels = ["Flower Name:", "Category:", "Unit Price:", "Description:", "Quantity:", "Reorder Level:", "Supplier:"]
        self.name_var = tk.Entry(form_frame, width=40)
        self.cat_var = ttk.Combobox(form_frame, width=38, state="readonly")
        self.price_var = tk.Entry(form_frame, width=40)
        self.desc_var = tk.Entry(form_frame, width=40)
        self.qty_var = tk.Entry(form_frame, width=40)
        self.reorder_var = tk.Entry(form_frame, width=40)
        self.sup_var = ttk.Combobox(form_frame, width=38, state="readonly")

        fields = [self.name_var, self.cat_var, self.price_var, self.desc_var,
                  self.qty_var, self.reorder_var, self.sup_var]

        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg="#BBDEFB", fg="#0D47A1",
                     font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=3)
            fields[i].grid(row=i, column=1, pady=3)

        # Buttons
        btn_frame = tk.Frame(frame, bg="#E3F2FD")
        btn_frame.pack(pady=10)
        buttons = [
            ("Add Flower", self.add_flower),
            ("Update", self.update_flower),
            ("Delete", self.delete_flower),
            ("Clear", self.clear_flower_form)
        ]
        for i, (txt, cmd) in enumerate(buttons):
            b = tk.Button(btn_frame, text=txt, command=cmd,
                          width=16, bg="#90CAF9", fg="#0D47A1",
                          font=("Segoe UI", 10, "bold"), bd=2, relief="raised",
                          activebackground="#64B5F6", cursor="hand2")
            b.grid(row=0, column=i, padx=10)
            b.bind("<Enter>", lambda e, btn=b: self.hover_button(btn, True))
            b.bind("<Leave>", lambda e, btn=b: self.hover_button(btn, False))

        # Treeview
        table_frame = tk.Frame(frame, bg="#BBDEFB", bd=2, relief="groove")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)
        columns = ("ID", "Name", "Category", "Price", "Description", "Qty", "Reorder", "Supplier")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.column("Supplier", width=140)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.fill_flower_form)

    # ----------------------------
    # Supplier Tab
    # ----------------------------
    def create_supplier_tab(self):
        frame = self.tab_supplier
        form_frame = tk.LabelFrame(frame, text="🌼 Supplier Details 🌼",
                                   bg="#BBDEFB", fg="#0D47A1",
                                   font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        form_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(form_frame, text="Name:", bg="#BBDEFB", fg="#0D47A1", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(form_frame, text="Contact:", bg="#BBDEFB", fg="#0D47A1", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w")
        tk.Label(form_frame, text="Address:", bg="#BBDEFB", fg="#0D47A1", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")

        self.sup_name_var = tk.Entry(form_frame, width=40)
        self.sup_contact_var = tk.Entry(form_frame, width=40)
        self.sup_address_var = tk.Entry(form_frame, width=40)
        self.sup_name_var.grid(row=0, column=1, pady=5)
        self.sup_contact_var.grid(row=1, column=1, pady=5)
        self.sup_address_var.grid(row=2, column=1, pady=5)

        # Buttons
        btn_frame = tk.Frame(frame, bg="#E3F2FD")
        btn_frame.pack(pady=10)
        buttons = [
            ("Add Supplier", self.add_supplier),
            ("Update", self.update_supplier),
            ("Delete", self.delete_supplier),
            ("Clear", self.clear_supplier_form)
        ]
        for i, (txt, cmd) in enumerate(buttons):
            b = tk.Button(btn_frame, text=txt, command=cmd,
                          width=16, bg="#90CAF9", fg="#0D47A1",
                          font=("Segoe UI", 10, "bold"), bd=2, relief="raised",
                          activebackground="#64B5F6", cursor="hand2")
            b.grid(row=0, column=i, padx=10)

        # Treeview
        table_frame = tk.Frame(frame, bg="#BBDEFB", bd=2, relief="groove")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)
        self.sup_tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Contact", "Address"), show="headings")
        for col in ("ID", "Name", "Contact", "Address"):
            self.sup_tree.heading(col, text=col)
            self.sup_tree.column(col, width=200)
        self.sup_tree.pack(fill="both", expand=True)
        self.sup_tree.bind("<<TreeviewSelect>>", self.fill_supplier_form)

    # ----------------------------
    # Loading Data
    # ----------------------------
    def load_categories(self):
        self.cat_map.clear()
        self.cat_reverse.clear()
        names = []
        for cid, cname, desc in get_all_categories():
            self.cat_map[cname] = cid
            self.cat_reverse[cid] = cname
            names.append(cname)
        self.cat_var["values"] = names

    def load_categories_table(self):
        for row in self.cat_tree.get_children():
            self.cat_tree.delete(row)
        # Sort by ID
        categories = sorted(get_all_categories(), key=lambda x: x[0])  # x[0] = category_id
        for cid, cname, desc in categories:
            self.cat_tree.insert("", "end", values=(cid, cname, desc))

    def load_suppliers(self):
        for row in self.sup_tree.get_children():
            self.sup_tree.delete(row)
        # Sort by ID
        suppliers = sorted(get_all_suppliers(), key=lambda x: x[0])  # x[0] = supplier_id
        for sid, name, contact, address in suppliers:
            self.sup_tree.insert("", "end", values=(sid, name, contact, address))

    def load_suppliers_to_combo(self):
        self.sup_map.clear()
        self.sup_reverse.clear()
        names = []
        for sid, name, contact, address in get_all_suppliers():
            self.sup_map[name] = sid
            self.sup_reverse[sid] = name
            names.append(name)
        self.sup_var["values"] = names

    def load_flowers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        flowers = sorted(get_all_flowers(), key=lambda x: x[0])  # x[0] = flower_id
        for f in flowers:
            fid, name, cat_id, price, desc, qty, reorder, supplier_id = f
            cat_name = self.cat_reverse.get(cat_id, "Unknown")
            sup_name = self.sup_reverse.get(supplier_id, "None")
            status = "LOW" if qty <= reorder else "OK"

            self.tree.insert("", "end",
                             values=(fid, name, cat_name, price, desc, qty, status, sup_name))

    # ----------------------------
    # Fill Forms
    # ----------------------------
    def fill_category_form(self, event):
        sel = self.cat_tree.focus()
        if not sel: return
        data = self.cat_tree.item(sel)["values"]
        if not data: return
        self.selected_category_id, name, desc = data
        self.cat_name_var.delete(0, tk.END)
        self.cat_name_var.insert(0, name)
        self.cat_desc_var.delete(0, tk.END)
        self.cat_desc_var.insert(0, desc)

    def fill_supplier_form(self, event):
        sel = self.sup_tree.focus()
        if not sel: return
        data = self.sup_tree.item(sel)["values"]
        if not data: return
        self.selected_supplier_id, name, contact, address = data
        self.sup_name_var.delete(0, tk.END); self.sup_name_var.insert(0, name)
        self.sup_contact_var.delete(0, tk.END); self.sup_contact_var.insert(0, contact)
        self.sup_address_var.delete(0, tk.END); self.sup_address_var.insert(0, address)

    def fill_flower_form(self, event):
        sel = self.tree.focus()
        if not sel: return
        values = self.tree.item(sel)["values"]
        if not values or len(values) < 8: return
        fid, name, cat_name, price, desc, qty, reorder_status, supplier_name = values
        self.selected_flower_id = fid
        self.name_var.delete(0, tk.END); self.name_var.insert(0, name)
        self.cat_var.set(cat_name)
        self.price_var.delete(0, tk.END); self.price_var.insert(0, price)
        self.desc_var.delete(0, tk.END); self.desc_var.insert(0, desc)
        self.qty_var.delete(0, tk.END); self.qty_var.insert(0, qty)
        row = get_flower_by_id(fid)
        if row:
            self.reorder_var.delete(0, tk.END); self.reorder_var.insert(0, row[6])
        self.sup_var.set(supplier_name)

    # ----------------------------
    # CRUD Category
    # ----------------------------
    def add_category(self):
        add_category(self.cat_name_var.get(), self.cat_desc_var.get())
        self.load_categories(); self.load_categories_table()
        self.clear_category_form(); messagebox.showinfo("Success", "Category added!")

    def update_category(self):
        if not self.selected_category_id: messagebox.showerror("Error", "Select a category first"); return
        update_category(self.selected_category_id, self.cat_name_var.get(), self.cat_desc_var.get())
        self.load_categories(); self.load_categories_table()
        self.clear_category_form(); messagebox.showinfo("Updated", "Category updated!")

    def delete_category(self):
        if not self.selected_category_id: messagebox.showerror("Error", "Select a category first"); return
        delete_category(self.selected_category_id)
        self.load_categories(); self.load_categories_table()
        self.clear_category_form(); messagebox.showinfo("Deleted", "Category deleted!")

    def clear_category_form(self):
        self.selected_category_id = None
        self.cat_name_var.delete(0, tk.END); self.cat_desc_var.delete(0, tk.END)

    # ----------------------------
    # CRUD Supplier
    # ----------------------------
    def add_supplier(self):
        add_supplier(self.sup_name_var.get(), self.sup_contact_var.get(), self.sup_address_var.get())
        self.load_suppliers(); self.load_suppliers_to_combo()
        self.clear_supplier_form(); messagebox.showinfo("Success", "Supplier added!")

    def update_supplier(self):
        if not self.selected_supplier_id: messagebox.showerror("Error", "Select a supplier first"); return
        update_supplier(self.selected_supplier_id, self.sup_name_var.get(), self.sup_contact_var.get(), self.sup_address_var.get())
        self.load_suppliers(); self.load_suppliers_to_combo()
        messagebox.showinfo("Updated", "Supplier updated!")

    def delete_supplier(self):
        if not self.selected_supplier_id: messagebox.showerror("Error", "Select a supplier first"); return
        delete_supplier(self.selected_supplier_id)
        self.load_suppliers(); self.load_suppliers_to_combo()
        self.clear_supplier_form(); messagebox.showinfo("Deleted", "Supplier deleted!")

    def clear_supplier_form(self):
        self.selected_supplier_id = None
        self.sup_name_var.delete(0, tk.END)
        self.sup_contact_var.delete(0, tk.END)
        self.sup_address_var.delete(0, tk.END)

    # ----------------------------
    # CRUD Flower
    # ----------------------------
    def add_flower(self):
        try:
            category_id = self.cat_map.get(self.cat_var.get(), None)
            supplier_id = self.sup_map.get(self.sup_var.get(), None)

            add_flower(
                self.name_var.get(),
                category_id,
                float(self.price_var.get()),
                self.desc_var.get(),
                int(self.qty_var.get()),
                int(self.reorder_var.get()),
                supplier_id
            )

            self.load_flowers()
            self.clear_flower_form()
            messagebox.showinfo("Success", "Flower added!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_flower(self):
        if not self.selected_flower_id: messagebox.showerror("Error", "Select a flower first"); return
        category_id = self.cat_map.get(self.cat_var.get())
        supplier_id = self.sup_map.get(self.sup_var.get())
        update_flower(self.selected_flower_id, self.name_var.get(), category_id,
                      float(self.price_var.get()), self.desc_var.get(),
                      int(self.qty_var.get()), int(self.reorder_var.get()), supplier_id)
        self.load_flowers(); messagebox.showinfo("Updated", "Flower updated!")

    def delete_flower(self):
        if not self.selected_flower_id: messagebox.showerror("Error", "Select a flower first"); return
        delete_flower(self.selected_flower_id)
        self.load_flowers(); self.clear_flower_form(); messagebox.showinfo("Deleted", "Flower deleted!")

    def clear_flower_form(self):
        self.selected_flower_id = None
        self.name_var.delete(0, tk.END); self.cat_var.set(""); self.price_var.delete(0, tk.END)
        self.desc_var.delete(0, tk.END); self.qty_var.delete(0, tk.END); self.reorder_var.delete(0, tk.END)
        self.sup_var.set("")

    # ----------------------------
    # Search
    # ----------------------------
    def search_flower(self):
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.load_flowers()
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        for f in get_all_flowers():
            fid, name, cat_id, price, desc, qty, reorder, supplier_id = f
            cat_name = self.cat_reverse.get(cat_id, "Unknown")
            sup_name = self.sup_reverse.get(supplier_id, "None")
            status = "LOW" if qty <= reorder else "OK"
            if (keyword in str(fid).lower() or 
                keyword in name.lower() or 
                keyword in cat_name.lower() or
                keyword in sup_name.lower()):
                self.tree.insert("", "end",
                                 values=(fid, name, cat_name, price, desc, qty, status, sup_name))



if __name__ == "__main__":
    root = tk.Tk()
    app = FlowerShopApp(root)
    root.mainloop()
