import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",  
        database="ecommerce"
    )

def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def autenticar_cliente(email, senha):
    """
    Tenta autenticar um cliente:
    1. Primeiro verifica SHA-256
    2. Se falhar, verifica senha antiga (texto simples) e atualiza para SHA-256
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    senha_hash = gerar_hash_senha(senha)

    # Tenta autenticar com SHA-256
    cursor.execute("""
        SELECT idClientes, nome
        FROM Clientes
        WHERE `e-mail` = %s AND senha = %s
    """, (email, senha_hash))
    cliente = cursor.fetchone()

    # Se não encontrou, tenta senha antiga (texto simples)
    if not cliente:
        cursor.execute("""
            SELECT idClientes, nome
            FROM Clientes
            WHERE `e-mail` = %s AND senha = %s
        """, (email, senha))
        cliente = cursor.fetchone()

        # Se encontrou, atualiza senha para SHA-256
        if cliente:
            cursor.execute("""
                UPDATE Clientes
                SET senha = %s
                WHERE idClientes = %s
            """, (senha_hash, cliente['idClientes']))
            conexao.commit()

    cursor.close()
    conexao.close()
    return cliente

def fazer_login():
    email = entry_email.get().strip()
    senha = entry_senha.get().strip()

    if not email or not senha:
        messagebox.showwarning("Campos obrigatórios", "Preencha o e-mail e a senha.")
        return

    cliente = autenticar_cliente(email, senha)

    if cliente:
        messagebox.showinfo("Login bem-sucedido", f"Bem-vindo(a), {cliente['nome']}!")
        root.destroy()

        try:
            from cadastro_principal_menu import iniciar_menu_principal
            iniciar_menu_principal(cliente["idClientes"], cliente["nome"])
        except Exception as e:
            messagebox.showinfo("Aviso", f"Login OK, mas não foi possível abrir o menu principal.\nErro: {e}")
    else:
        messagebox.showerror("Erro", "E-mail ou senha incorretos.")

def iniciar_login():
    global root, entry_email, entry_senha

    root = tk.Tk()
    root.title("Login - Sistema de E-commerce")
    root.geometry("400x250")
    root.resizable(False, False)

    tk.Label(root, text="E-mail:", font=("Arial", 11)).pack(pady=8)
    entry_email = tk.Entry(root, width=35)
    entry_email.pack()

    tk.Label(root, text="Senha:", font=("Arial", 11)).pack(pady=8)
    entry_senha = tk.Entry(root, width=35, show="*")
    entry_senha.pack()

    tk.Button(root, text="Entrar", command=fazer_login, bg="#4CAF50", fg="white", width=20).pack(pady=20)
    tk.Button(root, text="Sair", command=root.destroy, bg="#E53935", fg="white", width=10).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar_login()
