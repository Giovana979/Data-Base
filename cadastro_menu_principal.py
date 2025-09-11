import tkinter as tk
from tkinter import messagebox
# Funções de exemplo
def cadastrar_cliente():
 import cadastro_clientes
 cadastro_clientes.iniciar()
 # messagebox.showinfo("Cadastro", "Cadastro de Cliente iniciado.")
def cadastrar_produto():
 import cadastro_produtos
 cadastro_produtos.iniciar()
def abrir_categorias():
 import cadastro_categoria
 cadastro_categoria.iniciar()
def cadastrar_pedido():
 import cadastro_pedidos
 cadastro_pedidos.iniciar()
def consultar_pedidos():
 import consulta_pedidos
 consulta_pedidos.iniciar()
def sair():
 root.quit()
# Janela principal
root = tk.Tk()
root.title("Sistema de Comércio")
root.geometry("800x600")
# Barra de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
# Menu "Cadastros"
menu_cadastros = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Cadastros", menu=menu_cadastros)
menu_cadastros.add_command(label="Cadastrar Cliente", command=cadastrar_cliente)
menu_cadastros.add_command(label="Cadastrar Produto", command=cadastrar_produto)
menu_cadastros.add_command(label="Cadastrar Categoria", command=abrir_categorias)
menu_cadastros.add_command(label="Cadastrar Pedido", command=cadastrar_pedido)
menu_cadastros.add_command(label="Consultar Pedidos", command=consultar_pedidos)
# Menu "Sair"
menu_bar.add_command(label="Sair", command=sair)