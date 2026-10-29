import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

filename = "inventory.csv"
data_list = []


def load_data():
    global data_list
    data_list = []
    try:
        with open(filename, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_list.append(row)
    except FileNotFoundError:
        pass
    refresh_table(data_list)


def save_data():
    with open(filename, "w", encoding="utf-8", newline="") as f:
        fields = [
            "id",
            "name",
            "category",
            "quantity",
            "price",
            "location",
            "created_at",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in data_list:
            writer.writerow(row)
    status_var.set("Дані збережено!")


def refresh_table(items):
    for row in tree.get_children():
        tree.delete(row)
    for item in items:
        tree.insert(
            "",
            tk.END,
            values=(
                item["id"],
                item["name"],
                item["category"],
                item["quantity"],
                item["price"],
                item["location"],
                item["created_at"],
            ),
        )


def clear_form():
    for entry in entries.values():
        entry.delete(0, tk.END)
    status_var.set("Форму очищено")


def add_item():
    item_id = entries["id"].get().strip()
    name = entries["name"].get().strip()
    category = entries["category"].get().strip()
    qty = entries["quantity"].get().strip()
    price = entries["price"].get().strip().replace(",", ".")
    loc = entries["location"].get().strip()

    if not name or not category:
        status_var.set("Помилка: Назва та категорія обов'язкові")
        messagebox.showerror("Помилка", "Заповніть назву та категорію!")
        return

    if not item_id:
        item_id = str(len(data_list) + 1)
    elif any(r["id"] == item_id for r in data_list):
        status_var.set("Помилка: ID вже існує")
        messagebox.showerror("Помилка", "Такий ID вже є!")
        return

    try:
        quantity = int(qty)
        price_val = float(price)
        if quantity < 0 or price_val < 0:
            raise ValueError
    except ValueError:
        status_var.set("Помилка у числових полях")
        messagebox.showerror(
            "Помилка", "Кількість та ціна мають бути числами >= 0!"
        )
        return

    new_row = {
        "id": item_id,
        "name": name,
        "category": category,
        "quantity": str(quantity),
        "price": str(price_val),
        "location": loc,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    data_list.append(new_row)
    refresh_table(data_list)
    clear_form()
    status_var.set(f"Товар '{name}' додано!")


def update_item():
    selected = tree.selection()
    if not selected:
        status_var.set("Оберіть рядок для оновлення")
        messagebox.showwarning("Увага", "Оберіть рядок у таблиці!")
        return

    target_id = tree.item(selected, "values")[0]
    name = entries["name"].get().strip()
    category = entries["category"].get().strip()

    if not name or not category:
        status_var.set("Помилка: заповніть назву та категорію")
        return

    try:
        qty = int(entries["quantity"].get().strip())
        price = float(entries["price"].get().strip().replace(",", "."))
        if qty < 0 or price < 0:
            raise ValueError
    except ValueError:
        status_var.set("Помилка в числах")
        return

    for row in data_list:
        if row["id"] == target_id:
            row["name"] = name
            row["category"] = category
            row["quantity"] = str(qty)
            row["price"] = str(price)
            row["location"] = entries["location"].get().strip()
            break

    refresh_table(data_list)
    status_var.set("Товар оновлено!")


def delete_item():
    selected = tree.selection()
    if not selected:
        status_var.set("Оберіть рядок для видалення")
        messagebox.showwarning("Увага", "Оберіть рядок!")
        return

    if messagebox.askyesno("Підтвердження", "Видалити цей товар?"):
        target_id = tree.item(selected, "values")[0]
        global data_list
        data_list = [r for r in data_list if r["id"] != target_id]
        refresh_table(data_list)
        clear_form()
        status_var.set("Товар видалено!")


def on_select(event):
    selected = tree.selection()
    if not selected:
        return
    vals = tree.item(selected, "values")
    clear_form()
    keys = ["id", "name", "category", "quantity", "price", "location"]
    for i, k in enumerate(keys):
        entries[k].insert(0, vals[i])


def search_data(event):
    q = search_entry.get().lower()
    filtered = [
        r for r in data_list if q in r["name"].lower() or q in r["category"].lower()
    ]
    refresh_table(filtered)


def open_file():
    global filename
    path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if path:
        filename = path
        load_data()
        status_var.set(f"Відкрито: {path}")


def save_as():
    global filename
    path = filedialog.asksaveasfilename(defaultextension=".csv")
    if path:
        filename = path
        save_data()


root = tk.Tk()
root.title("Облік товарів")
root.geometry("850x550")


menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Відкрити...", command=open_file)
file_menu.add_command(label="Зберегти", command=save_data)
file_menu.add_command(label="Зберегти як...", command=save_as)
menubar.add_cascade(label="Файл", menu=file_menu)
root.config(menu=menubar)


top_f = tk.Frame(root, padx=10, pady=5)
top_f.pack(fill=tk.X)
tk.Label(top_f, text="Пошук:").pack(side=tk.LEFT)
search_entry = tk.Entry(top_f, width=25)
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.bind("<KeyRelease>", search_data)

mid_f = tk.Frame(root, padx=10)
mid_f.pack(fill=tk.BOTH, expand=True)

cols = ("id", "name", "category", "quantity", "price", "location", "created_at")
tree = ttk.Treeview(mid_f, columns=cols, show="headings", selectmode="browse")

headers = {
    "id": "ID",
    "name": "Назва",
    "category": "Категорія",
    "quantity": "Кількість",
    "price": "Ціна",
    "location": "Локація",
    "created_at": "Створено",
}
for c, t in headers.items():
    tree.heading(c, text=t)
    tree.column(c, width=100, anchor=tk.CENTER)

scrollbar = ttk.Scrollbar(mid_f, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.bind("<<TreeviewSelect>>", on_select)

form_f = tk.LabelFrame(root, text="Дані товару", padx=10, pady=5)
form_f.pack(fill=tk.X, padx=10, pady=5)

fields = [
    ("ID:", "id"),
    ("Назва:", "name"),
    ("Категорія:", "category"),
    ("Кількість:", "quantity"),
    ("Ціна:", "price"),
    ("Локація:", "location"),
]
entries = {}
for i, (txt, key) in enumerate(fields):
    r, c = i // 2, (i % 2) * 2
    tk.Label(form_f, text=txt).grid(row=r, column=c, sticky=tk.W, padx=5, pady=2)
    e = tk.Entry(form_f, width=22)
    e.grid(row=r, column=c + 1, padx=5, pady=2)
    entries[key] = e

btn_f = tk.Frame(root, padx=10, pady=5)
btn_f.pack(fill=tk.X)
tk.Button(btn_f, text="Додати", width=10, command=add_item).pack(
    side=tk.LEFT, padx=3
)
tk.Button(btn_f, text="Оновити", width=10, command=update_item).pack(
    side=tk.LEFT, padx=3
)
tk.Button(btn_f, text="Видалити", width=10, command=delete_item).pack(
    side=tk.LEFT, padx=3
)
tk.Button(
    btn_f, text="Очистити", width=12, command=clear_form
).pack(side=tk.LEFT, padx=3)

status_var = tk.StringVar(value="Готово")
status_bar = tk.Label(
    root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

load_data()

root.mainloop()