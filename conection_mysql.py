import mysql.connector

conexao = mysql.connector.connect(
 host="localhost",
 user="root",
 password="12345",
 database="ecommerce"
)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
 id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100),
 cargo VARCHAR(50),
 salario DECIMAL(10,2)
)
""")

cursor.execute("""
INSERT INTO funcionarios (nome, cargo, salario)
VALUES (%s, %s, %s)
""", ("Ana Souza", "Analista", 5500.00))
conexao.commit()
print("Listar dados e verificar se Ana Souza foi Incluida:")
cursor.execute("SELECT * FROM funcionarios")
for funcionario in cursor.fetchall():
 print(funcionario)
print("====================================================")

cursor.execute("""
UPDATE funcionarios
SET salario = %s
WHERE nome = %s
""", (6000.00, "Ana Souza"))
conexao.commit()
print("Listar dados e verificar se o salario foi alterado:")
cursor.execute("SELECT * FROM funcionarios")
for funcionario in cursor.fetchall():
 print(funcionario)
print("====================================================")

cursor.execute("""
DELETE FROM funcionarios
WHERE nome = %s
""", ("Ana Souza",))
conexao.commit()

cursor.execute("SELECT * FROM funcionarios")
for funcionario in cursor.fetchall():
 print(funcionario)
print("====================================================")

cursor.close()
conexao.close()