import tkinter as tk
from tkinter import ttk
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="ecommerce"
    )

def carregar_produtos(tree):
    # Limpa itens existentes
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    # Seleciona as colunas que vamos mostrar
    cursor.execute("SELECT idProdutos, nome, preco, Categoria_idCategoria FROM Produtos")
    produtos = cursor.fetchall()
    
    for prod in produtos:
        tree.insert("", tk.END, values=prod)
    
    cursor.close()
    conexao.close()

def iniciar():
    # Cria a janela principal
    root = tk.Tk()
    root.title("Exemplo Treeview")
    root.geometry("500x300")

    # Definição das colunas
    colunas = ("ID", "Nome", "Preço", "Categoria")

    # Cria a Treeview
    tree = ttk.Treeview(root, columns=colunas, show="headings")

    # Configura cabeçalhos e largura das colunas
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Exibe a Treeview na janela
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Carrega os produtos
    carregar_produtos(tree)

    # Loop principal
    root.mainloop()

# Executa o programa
if __name__ == "__main__":
    iniciar()
