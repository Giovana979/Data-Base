import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # coloque a senha correta
        database="ecommerce"
    )

def carregar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT idClientes, nome FROM clientes")  # use minúsculo
    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return clientes

def carregar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT idProdutos, nome, preco FROM produtos")  # use minúsculo
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return produtos

def atualizar_total():
    total = 0
    for item in tree.get_children():
        subtotal = float(tree.item(item, "values")[4])
        total += subtotal
    label_total.config(text=f"Total: R$ {total:.2f}")

def adicionar_produto():
    produto_nome = combo_produto.get()
    quantidade = entry_quantidade.get()
    if not produto_nome or not quantidade.isdigit():
        messagebox.showwarning("Atenção", "Selecione um produto e informe a quantidade.")
        return
    
    quantidade = int(quantidade)
    id_produto, preco = dict_produtos[produto_nome]
    total = preco * quantidade
    tree.insert("", "end", values=(id_produto, produto_nome, quantidade, preco, total))
    atualizar_total()

def salvar_pedido():
    messagebox.showinfo("Pedido", "Função de salvar ainda não implementada!")

# ================== INTERFACE ==================
