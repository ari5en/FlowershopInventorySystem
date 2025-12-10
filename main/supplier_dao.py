from database import get_connection

# -----------------------------
# SELECT ALL SUPPLIERS
# -----------------------------
def get_all_suppliers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT supplier_id, name, contact, address FROM supplier ORDER BY name")
    data = cur.fetchall()
    conn.close()
    return data

# -----------------------------
# ADD SUPPLIER
# -----------------------------
def add_supplier(name, contact, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO supplier (name, contact, address) VALUES (%s, %s, %s)",
                (name, contact, address))
    conn.commit()
    conn.close()

# -----------------------------
# UPDATE SUPPLIER
# -----------------------------
def update_supplier(supplier_id, name, contact, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE supplier 
                   SET name=%s, contact=%s, address=%s
                   WHERE supplier_id=%s""",
                (name, contact, address, supplier_id))
    conn.commit()
    conn.close()

# -----------------------------
# DELETE SUPPLIER
# -----------------------------
def delete_supplier(supplier_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM supplier WHERE supplier_id=%s", (supplier_id,))
    conn.commit()
    conn.close()
