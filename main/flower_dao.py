from database import get_connection

# -----------------------------
# SELECT ALL FLOWERS
# -----------------------------
def get_all_flowers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower")
    data = cur.fetchall()
    conn.close()
    return data

# -----------------------------
# GET FLOWER BY ID
# -----------------------------
def get_flower_by_id(flower_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower WHERE flower_id=%s", (flower_id,))
    data = cur.fetchone()
    conn.close()
    return data

# -----------------------------
# ADD FLOWER
# -----------------------------
def add_flower(name, category_id, price, desc, qty, reorder_level, supplier_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = """INSERT INTO flower 
             (name, category_id, unit_price, description, quantity, reorder_level, supplier_id)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, (name, category_id, price, desc, qty, reorder_level, supplier_id))
    conn.commit()
    conn.close()


# -----------------------------
# UPDATE FLOWER
# -----------------------------
def update_flower(flower_id, name, category_id, price, desc, qty, reorder_level, supplier_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = """UPDATE flower SET 
                name=%s, category_id=%s, unit_price=%s,
                description=%s, quantity=%s, reorder_level=%s,
                supplier_id=%s
             WHERE flower_id=%s"""
    cur.execute(sql, (name, category_id, price, desc, qty, reorder_level, supplier_id, flower_id))
    conn.commit()
    conn.close()


# -----------------------------
# DELETE FLOWER
# -----------------------------
def delete_flower(flower_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM flower WHERE flower_id=%s", (flower_id,))
    conn.commit()
    conn.close()
