from database import get_connection

# -----------------------------
# SELECT ALL
# -----------------------------
def get_all_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name, description FROM category ORDER BY name")
    data = cur.fetchall()
    conn.close()
    return data

# -----------------------------
# ADD CATEGORY
# -----------------------------
def add_category(name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO category (name, description) VALUES (%s, %s)", (name, description))
    conn.commit()
    conn.close()

# -----------------------------
# UPDATE CATEGORY
# -----------------------------
def update_category(category_id, name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE category SET name=%s, description=%s WHERE category_id=%s", (name, description, category_id))
    conn.commit()
    conn.close()

# -----------------------------
# DELETE CATEGORY
# -----------------------------
def delete_category(category_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM category WHERE category_id=%s", (category_id,))
    conn.commit()
    conn.close()
