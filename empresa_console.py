import mysql.connector

conexao = mysql.connector.connect(
 host="localhost",
 user="root",
 password="12345",
 database="ecommerce" # ex: "meu_banco"
)

cursor = conexao.cursor()

cursor.execute("SELECT * FROM ")
resultados = cursor.fetchall()
for linha in resultados:
 print(linha)

cursor.close()
conexao.close()

try:
 conexao = mysql.connector.connect(
 host="localhost",
 user="root",
 password="12345",
 database="ecommerce"
 )
 print("Conexão bem-sucedida!")
except mysql.connector.Error as erro:
 print(f"Erro ao conectar: {erro}")
