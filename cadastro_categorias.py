import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="ecommerce"
    )

def inserir_categoria():
    nome = entry_nome.get().strip()
    descricao = entry_descr.get("1.0", tk.END).strip()
    if not nome:
        messagebox.showwarning("Atenção", "Informe o nome da categoria.")
        return
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Categoria (nome, descricao) VALUES (%s, %s)", (nome, descricao))
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir: {e}")
    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass
    listar()
    entry_nome.delete(0, tk.END)
    entry_descr.delete("1.0", tk.END)
    messagebox.showinfo("Sucesso", "Categoria cadastrada.")

def listar():
    for item in tree.get_children():
        tree.delete(item)
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT idCategoria, nome, descricao FROM Categoria")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

def iniciar():
    global entry_nome, entry_descr, tree
    janela = tk.Toplevel()
    janela.title("Cadastro de Categoria")
    janela.geometry("520x360")

    tk.Label(janela, text="Nome da Categoria").pack(anchor="w", padx=10, pady=(10,0))
    entry_nome = tk.Entry(janela)
    entry_nome.pack(fill="x", padx=10)

    tk.Label(janela, text="Descrição").pack(anchor="w", padx=10, pady=(10,0))
    entry_descr = tk.Text(janela, height=4)
    entry_descr.pack(fill="x", padx=10)

    tk.Button(janela, text="Cadastrar", command=inserir_categoria).pack(pady=6)

    tree = ttk.Treeview(janela, columns=("ID", "Nome","Descrição"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    listar()
