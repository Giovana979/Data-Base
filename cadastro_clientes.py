import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="ecommerce"
    )

def inserir():
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    senha = entry_senha.get().strip()
    dataNascimento = entry_data_nascimento.get().strip()
    telefone = entry_telefone.get().strip()

    if not nome or not email or not telefone:
        messagebox.showwarning("Campos vazios", "Preencha Nome, Email e Telefone.")
        return

    data_db = None
    if dataNascimento:
        try:
            data_db = datetime.strptime(dataNascimento, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Formato: AAAA-MM-DD")
            return

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO Clientes (nome, `e-mail`, senha, telefone, dataNascimento) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, senha, telefone, data_db)
        )
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir cliente: {e}")
    finally:
        try: cursor.close(); conexao.close()
        except: pass

    listar()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cliente cadastrado.")

def atualizar():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Seleção", "Selecione um cliente.")
        return
    id_cliente = tree.item(sel)["values"][0]
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    senha = entry_senha.get().strip()
    dataNascimento = entry_data_nascimento.get().strip()
    telefone = entry_telefone.get().strip()

    data_db = None
    if dataNascimento:
        try:
            data_db = datetime.strptime(dataNascimento, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Formato: AAAA-MM-DD")
            return

    try:
        conexao = conectar(); cursor = conexao.cursor()
        cursor.execute(
            "UPDATE Clientes SET nome=%s, `e-mail`=%s, senha=%s, telefone=%s, dataNascimento=%s WHERE idClientes=%s",
            (nome, email, senha, telefone, data_db, id_cliente)
        )
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar: {e}")
    finally:
        try: cursor.close(); conexao.close()
        except: pass

    listar(); limpar_campos()
    messagebox.showinfo("Sucesso", "Atualizado.")

def remover():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Seleção", "Selecione um cliente.")
        return
    id_cliente = tree.item(sel)["values"][0]
    try:
        conexao = conectar(); cursor = conexao.cursor()
        cursor.execute("DELETE FROM Clientes WHERE idClientes=%s", (id_cliente,))
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao remover: {e}")
    finally:
        try: cursor.close(); conexao.close()
        except: pass
    listar(); limpar_campos()
    messagebox.showinfo("Sucesso", "Removido.")

def listar():
    for i in tree.get_children(): tree.delete(i)
    try:
        conexao = conectar(); cursor = conexao.cursor()
        cursor.execute("SELECT idClientes, nome, `e-mail`, telefone, dataNascimento FROM Clientes")
        for r in cursor.fetchall():
            tree.insert("", "end", values=r)
    finally:
        try: cursor.close(); conexao.close()
        except: pass

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)

def iniciar():
    global entry_nome, entry_email, entry_senha, entry_telefone, entry_data_nascimento, tree
    janela = tk.Toplevel(); janela.title("Clientes"); janela.geometry("760x460")

    tk.Label(janela, text="Nome").grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(janela, width=40); entry_nome.grid(row=0, column=1, pady=2, padx=5)
    tk.Label(janela, text="Email").grid(row=1, column=0, sticky="w")
    entry_email = tk.Entry(janela, width=40); entry_email.grid(row=1, column=1, pady=2, padx=5)
    tk.Label(janela, text="Telefone").grid(row=2, column=0, sticky="w")
    entry_telefone = tk.Entry(janela, width=20); entry_telefone.grid(row=2, column=1, pady=2, padx=5, sticky="w")
    tk.Label(janela, text="Senha").grid(row=3, column=0, sticky="w")
    entry_senha = tk.Entry(janela, width=20, show="*"); entry_senha.grid(row=3, column=1, pady=2, padx=5, sticky="w")
    tk.Label(janela, text="DataNascimento (AAAA-MM-DD)").grid(row=4, column=0, sticky="w")
    entry_data_nascimento = tk.Entry(janela, width=20); entry_data_nascimento.grid(row=4, column=1, pady=2, padx=5, sticky="w")

    tk.Button(janela, text="Inserir", command=inserir).grid(row=5, column=0, pady=8)
    tk.Button(janela, text="Atualizar", command=atualizar).grid(row=5, column=1)
    tk.Button(janela, text="Remover", command=remover).grid(row=5, column=2)

    tree = ttk.Treeview(janela, columns=("ID","Nome","Email","Telefone","DataNascimento"), show="headings", height=12)
    for c in ("ID","Nome","Email","Telefone","DataNascimento"): tree.heading(c, text=c)
    tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    listar()
