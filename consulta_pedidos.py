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

def listar_pedidos():
    for item in tree.get_children():
        tree.delete(item)
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT p.idPedidos, c.nome, p.dataPedido, p.status, p.total
            FROM Pedidos p
            JOIN Clientes c ON p.Clientes_idClientes = c.idClientes
            ORDER BY p.dataPedido DESC
        """)
        pedidos = cursor.fetchall()
    finally:
        try:
            cursor.close(); conexao.close()
        except:
            pass
    for pedido in pedidos:
        tree.insert("", "end", values=pedido)

def iniciar():
    global tree
    janela = tk.Toplevel()
    janela.title("Lista de Pedidos")
    janela.geometry("920x460")

    tree = ttk.Treeview(janela, columns=("ID", "Cliente", "Data", "Status", "Total"), show="headings", height=18)
    for col in ("ID", "Cliente", "Data", "Status", "Total"):
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True, pady=10)

    btn_atualizar = tk.Button(janela, text="Listar Pedidos", command=listar_pedidos)
    btn_atualizar.pack(pady=5)

    listar_pedidos()
