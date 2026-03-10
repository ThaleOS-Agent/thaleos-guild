import sqlite3

def save_query(user, query):
    conn = sqlite3.connect("ai_memory.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS queries (user TEXT, query TEXT)")
    cursor.execute("INSERT INTO queries VALUES (?, ?)", (user, query))
    conn.commit()
    conn.close()

def fetch_queries(user):
    conn = sqlite3.connect("ai_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT query FROM queries WHERE user=?", (user,))
    data = cursor.fetchall()
    conn.close()
    return data

# Example usage:
save_query("John", "Predict stock market trends for 2025")
print(fetch_queries("John"))