import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5433,
    user="ecommerce_user",
    password="ecommerce_pass",
    dbname="ecommerce_db",
)
print("Conectou com sucesso!")
conn.close()