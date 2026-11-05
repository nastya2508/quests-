import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests

API_URL = "http://127.0.0.1:5000/items"
CACHE_FILE = "cache.csv"

data_list = []


def load_data():
    global data_list
    data_list = []
    try:
        response = requests.get(API_URL, timeout=3)
        if response.status_code == 200:
            data_list = response.json()
            save_to_cache(data_list)
            status_var.set("Дані завантажено з сервера")
        else:
            raise Exception()
    except:
        status_var.set("Офлайн-режим (робота з кешем)")
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data_list.append(row)
        else:
            messagebox.showwarning("Увага", "Сервер недоступний і кеш відсутній")
            
    refresh_table(data_list)


def save_to_cache(items):
    with open(CACHE_FILE, "w", encoding="utf-8", newline="") as f:
        if not items:
            return
        fieldnames = items[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)


def refresh_table(items):
    for row in tree.get_children():
        tree.delete(row)
    for item in items:
        tree.insert(
            "",
            tk.END,
            values=(
                item.get("id"),
                item.get("name"),
                item.get("category"),
                item.get("quantity"),
                item.get("price"),
                item.get("location"),
                item.get("created_at"),
            ),
        )


def clear_form():
    for entry in entries.values():
        entry.delete(0, tk.END)
    status_var.set("Форму очищено")


def add_item():
    name = entries["name"].get().strip()
    category = entries["category"].get().strip()
    qty = entries["quantity"].get().strip()
    price = entries["price"].get().strip().replace(",", ".")
    loc = entries["location"].get().strip()

    if not name or not category:
        status_var.set("Помилка: Назва та категорія обов'язкові")
        messagebox.showerror("Помилка", "Заповніть назву та категорію!")
        return

    item_data = {
        "name": name,
        "category": category,
        "quantity": qty if qty else "0",
        "price": price if price else "0.0",
        "location": loc
    }

    try:
        response = requests.post(API_URL, json=item_data, timeout=3)
        if response.status_code == 201:
            status_var.set("Товар успішно додано через API!")
            clear_form()
            load_data()
        else:
            err = response.json().get("error", "Помилка валідації")
            status_var.set(f"Помилка 400: {err}")
            messagebox.showerror("Помилка 400", err)
    except:
        status_var.set("Помилка: Немає зв'язку з сервером")
        messagebox.showerror("Помилка", "Не вдалося з'єднатися з сервером!")


def update_item():
    selected = tree.selection()
    if not selected:
        status_var.set("Оберіть рядок для оновлення")
        messagebox.showwarning("Увага", "Оберіть рядок у таблиці!")
        return

    target_id = tree.item(selected, "values")[0]
    name = entries["name"].get().strip()
    category = entries["category"].get().strip()
    qty = entries["quantity"].get().strip()
    price = entries["price"].get().strip().replace(",", ".")
    loc = entries["location"].get().strip()

    if not name or not category:
        status_var.set("Помилка: заповніть назву та категорію")
        return

    item_data = {
        "name": name,
        "category": category,
        "quantity": qty,
        "price": price,
        "location": loc
    }

    try:
        response = requests.put(f"{API_URL}/{target_id}", json=item_data, timeout=3)
        if response.status_code == 200:
            status_var.set("Товар оновлено через API!")
            clear_form()
            load_data()
        else:
            err = response.json().get("error", "Помилка")
            status_var.set(f"Помилка: {err}")
            messagebox.showerror("Помилка", err)
    except:
        status_var.set("Помилка зв'язку з сервером")
        messagebox.showerror("Помилка", "Сервер не відповідає")


def delete_item():
    selected = tree.selection()
    if not selected:
        status_var.set("Оберіть рядок для видалення")
        messagebox.showwarning("Увага", "Оберіть рядок!")
        return

    if messagebox.askyesno("Підтвердження", "Видалити цей товар через API?"):
        target_id = tree.item(selected, "values")[0]
        try:
            response = requests.delete(f"{API_URL}/{target_id}", timeout=3)
            if response.status_code == 200:
                load_data()
                clear_form()
                status_var.set("Товар видалено!")
            else:
                messagebox.showerror("Помилка", "Не вдалося видалити товар")
        except:
            messagebox.showerror("Помилка", "Сервер не відповідає")


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
        r for r in data_list if q in str(r.get("name", "")).lower() or q in str(r.get("category", "")).lower()
    ]
    refresh_table(filtered)


def export_csv_from_server():
    try:
        response = requests.get(API_URL, timeout=3)
        if response.status_code == 200:
            items = response.json()
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                with open(file_path, "w", encoding="utf-8", newline="") as f:
                    if items:
                        writer = csv.DictWriter(f, fieldnames=items[0].keys())
                        writer.writeheader()
                        for row in items:
                            writer.writerow(row)
                status_var.set("Експорт успішно виконано!")
    except:
        messagebox.showerror("Помилка", "Не вдалося отримати дані з сервера для експорту.")


root = tk.Tk()
root.title("Облік товарів (Клієнт)")
root.geometry("850x550")


menubar = tk.Menu(root)

sync_menu = tk.Menu(menubar, tearoff=0)
sync_menu.add_command(label="Синхронізувати зараз", command=load_data)
sync_menu.add_command(label="Експорт CSV", command=export_csv_from_server)
menubar.add_cascade(label="Синхронізація", menu=sync_menu)

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