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
    
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT idProdutos, nome, preco, Categoria_idCategoria FROM Produtos")
    produtos = cursor.fetchall()
    
    for prod in produtos:
        tree.insert("", tk.END, values=prod)
    
    cursor.close()
    conexao.close()

def iniciar():
    
    root = tk.Tk()
    root.title("Exemplo Treeview")
    root.geometry("500x300")

   
    colunas = ("ID", "Nome", "Preço", "Categoria")

   
    tree = ttk.Treeview(root, columns=colunas, show="headings")

    
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

   
    carregar_produtos(tree)

   
    root.mainloop()


if __name__ == "__main__":
    iniciar()
