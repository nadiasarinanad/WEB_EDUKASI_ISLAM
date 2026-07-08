from app import bcrypt, get_db_connection

def migrate_table(table, id_col, pass_col):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT {id_col}, {pass_col} FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        pwd = row[pass_col]
        if pwd and not pwd.startswith('$2b$'):
            hashed = bcrypt.generate_password_hash(pwd).decode('utf-8')
            cursor.execute(f"UPDATE {table} SET {pass_col} = %s WHERE {id_col} = %s", (hashed, row[id_col]))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Tabel {table} selesai.")

migrate_table('jemaah', 'id_jemaah', 'password')
migrate_table('ustadz', 'id_ustadz', 'password')
migrate_table('admin', 'id_admin', 'password')
print("Migrasi hash selesai.")