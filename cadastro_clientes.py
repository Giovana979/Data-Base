import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conexão com o banco
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="ecommerce"
    )

# Funções de banco
def inserir():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    data_nascimento = entry_data_nascimento.get()
    telefone = entry_telefone.get()

    if not nome or not email or not telefone:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO clientes (nome, email, telefone, senha, data_nascimento) VALUES (%s, %s, %s, %s, %s)",
                   (nome, email, telefone, senha, data_nascimento))
    conexao.commit()
    cursor.close()
    conexao.close()
    listar()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cadastro realizado.")

def atualizar():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um cliente.")
        return

    id_cliente = tree.item(selecionado)["values"][0]
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    data_nascimento = entry_data_nascimento.get()
    telefone = entry_telefone.get()

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE clientes SET nome=%s, email=%s, senha=%s, data_nascimento=%s, telefone=%s WHERE id=%s",
                   (nome, email, senha, data_nascimento, telefone, id_cliente))
    conexao.commit()
    cursor.close()
    conexao.close()
    listar()
    limpar_campos()
    messagebox.showinfo("Atualizado", "Cadastro atualizado.")

def remover():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um cliente.")
        return

    id_pessoa = tree.item(selecionado)["values"][0]

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id_pessoa,))
    conexao.commit()
    cursor.close()
    conexao.close()
    listar()
    limpar_campos()
    messagebox.showinfo("Removido", "Cadastro removido.")

def listar():
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    cursor.close()
    conexao.close()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)

def iniciar():

# Interface
    global entry_nome, entry_email, entry_telefone, tree

    janela = tk.Toplevel()
    janela.title("Cadastro de Clientes")
    janela.geometry("600x400")

    # Campos
    tk.Label(janela, text="Nome").grid(row=0, column=0)
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=0, column=1)

    tk.Label(janela, text="Email").grid(row=1, column=0)
    entry_email = tk.Entry(janela)
    entry_email.grid(row=1, column=1)

    tk.Label(janela, text="Telefone").grid(row=2, column=0)
    entry_telefone = tk.Entry(janela)
    entry_telefone.grid(row=2, column=1)

    # Botões
    tk.Button(janela, text="Inserir", command=inserir).grid(row=3, column=0, pady=10)
    tk.Button(janela, text="Atualizar", command=atualizar).grid(row=3, column=1)
    tk.Button(janela, text="Remover", command=remover).grid(row=3, column=2)

    # Tabela
    tree = ttk.Treeview(janela, columns=("ID", "Nome", "Email", "Telefone"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Email", text="Email")
    tree.heading("Telefone", text="Telefone")
    tree.heading("Senha", text="Senha")
    tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    listar()
