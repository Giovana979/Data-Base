import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# Função para conectar ao banco
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # coloque sua senha correta
        database="ecommerce"
    )


# Função para listar pedidos no Treeview
def listar_pedidos():
    # limpa a tree
    for item in tree.get_children():
        tree.delete(item)

    # conecta ao banco
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT p.idPedidos, c.nome, p.dataPedido, p.status, p.total
        FROM pedidos p
        JOIN clientes c ON p.idClientes = c.idClientes
    """)
    pedidos = cursor.fetchall()

    conexao.close()

    # insere os pedidos na tree
    for pedido in pedidos:
        tree.insert("", "end", values=pedido)


# ================== INTERFACE GRÁFICA ==================

janela = tk.Tk()
janela.title("Lista de Pedidos")
janela.geometry("700x400")

# Criando o Treeview
tree = ttk.Treeview(
    janela,
    columns=("ID", "Cliente", "Data", "Status", "Total"),
    show="headings"
)

tree.heading("ID", text="ID Pedido")
tree.heading("Cliente", text="Cliente")
tree.heading("Data", text="Data")
tree.heading("Status", text="Status")
tree.heading("Total", text="Total")

tree.pack(fill="both", expand=True, pady=10)

# Botão para atualizar a lista
btn_atualizar = tk.Button(janela, text="Listar Pedidos", command=listar_pedidos)
btn_atualizar.pack(pady=10)

janela.mainloop()
