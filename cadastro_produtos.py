import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(host="localhost", user="root", password="12345", database="ecommerce")

def carregar_categorias():
    conexao = conectar(); cursor = conexao.cursor()
    cursor.execute("SELECT idCategoria, nome FROM Categoria")
    res = cursor.fetchall(); cursor.close(); conexao.close()
    return res

def inserir_produto():
    nome = entry_nome.get().strip(); descricao = entry_descr.get("1.0", tk.END).strip()
    preco = entry_preco.get().strip(); imagem = entry_imagem.get().strip()
    peso = entry_peso.get().strip() or "0"; estoque = entry_estoque.get().strip() or "0"
    categoria = combo_categoria.get().strip()

    if not nome or not preco or not categoria:
        messagebox.showwarning("Atenção", "Preencha Nome, Preço e Categoria.")
        return
    try:
        preco = float(preco); peso = float(peso); estoque = int(estoque)
    except ValueError:
        messagebox.showerror("Erro", "Preço/Peso/Estoque inválido.")
        return

    categoria_id = dict_categorias.get(categoria)
    if categoria_id is None:
        messagebox.showerror("Erro", "Categoria inválida.")
        return

    try:
        conexao = conectar(); cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO Produtos (nome, descricao, preco, imagem, peso, estoque, Categoria_idCategoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, descricao, preco, imagem, peso, estoque, categoria_id))
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir produto: {e}")
    finally:
        try: cursor.close(); conexao.close()
        except: pass

    listar()
    entry_nome.delete(0, tk.END); entry_preco.delete(0, tk.END); entry_estoque.delete(0, tk.END); entry_imagem.delete(0, tk.END)
    combo_categoria.set("")
    messagebox.showinfo("Sucesso", "Produto cadastrado.")

def listar():
    for i in tree.get_children(): tree.delete(i)
    try:
        conexao = conectar(); cursor = conexao.cursor()
        cursor.execute("""
            SELECT p.idProdutos, p.nome, p.preco, c.nome, p.estoque
            FROM Produtos p
            LEFT JOIN Categoria c ON p.Categoria_idCategoria = c.idCategoria
        """)
        for r in cursor.fetchall(): tree.insert("", "end", values=r)
    finally:
        try: cursor.close(); conexao.close()
        except: pass

def iniciar():
    global entry_nome, entry_descr, entry_preco, entry_imagem, entry_peso, entry_estoque, combo_categoria, dict_categorias, tree
    janela = tk.Toplevel(); janela.title("Produtos"); janela.geometry("780x520")

    tk.Label(janela, text="Nome").grid(row=0, column=0, sticky="w"); entry_nome = tk.Entry(janela, width=50); entry_nome.grid(row=0, column=1, padx=5, pady=2)
    tk.Label(janela, text="Descrição").grid(row=1, column=0, sticky="w"); entry_descr = tk.Text(janela, height=4, width=38); entry_descr.grid(row=1, column=1, padx=5, pady=2)
    tk.Label(janela, text="Preço").grid(row=2, column=0, sticky="w"); entry_preco = tk.Entry(janela, width=20); entry_preco.grid(row=2, column=1, sticky="w", padx=5)
    tk.Label(janela, text="Imagem (caminho)").grid(row=3, column=0, sticky="w"); entry_imagem = tk.Entry(janela, width=50); entry_imagem.grid(row=3, column=1, padx=5, pady=2)
    tk.Label(janela, text="Peso (kg)").grid(row=4, column=0, sticky="w"); entry_peso = tk.Entry(janela, width=15); entry_peso.grid(row=4, column=1, sticky="w", padx=5)
    tk.Label(janela, text="Estoque").grid(row=5, column=0, sticky="w"); entry_estoque = tk.Entry(janela, width=10); entry_estoque.grid(row=5, column=1, sticky="w", padx=5)
    tk.Label(janela, text="Categoria").grid(row=6, column=0, sticky="w")
    categorias = carregar_categorias(); dict_categorias = {nome: id for id, nome in categorias}
    combo_categoria = ttk.Combobox(janela, values=list(dict_categorias.keys()), width=47); combo_categoria.grid(row=6, column=1, padx=5, pady=2)
    tk.Button(janela, text="Cadastrar", command=inserir_produto).grid(row=7, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(janela, columns=("ID","Nome","Preço","Categoria","Estoque"), show="headings", height=12)
    for c in ("ID","Nome","Preço","Categoria","Estoque"): tree.heading(c, text=c)
    tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    listar()
