import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(host="localhost", user="root", password="12345", database="ecommerce")

def carregar_produtos():
    conexao = conectar(); cursor = conexao.cursor()
    cursor.execute("SELECT idProdutos, nome, preco FROM Produtos")
    res = cursor.fetchall(); cursor.close(); conexao.close()
    return res

def atualizar_total():
    total = 0
    for i in tree.get_children():
        total += float(tree.item(i, "values")[4])
    label_total.config(text=f"Total: R$ {total:.2f}")

def adicionar_produto():
    nome = combo_produto.get().strip(); qtd = entry_quantidade.get().strip()
    if not nome or not qtd.isdigit():
        messagebox.showwarning("Atenção", "Selecione produto e quantidade.")
        return
    qtd = int(qtd)
    id_prod, preco = dict_produtos[nome]
    subtotal = preco * qtd
    tree.insert("", "end", values=(id_prod, nome, qtd, f"{preco:.2f}", f"{subtotal:.2f}"))
    atualizar_total()

def remover_item():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Atenção", "Selecione um item.")
        return
    tree.delete(sel); atualizar_total()

def salvar_itens_para_pedido(pedido_id):
    try:
        conexao = conectar(); cursor = conexao.cursor()
        for i in tree.get_children():
            id_prod, nome, qtd, preco_str, subtotal_str = tree.item(i, "values")
            subtotal = float(subtotal_str)
            cursor.execute("INSERT INTO ItemPedido (quantidade, precoTotal, Pedidos_idPedidos, Produtos_idProdutos) VALUES (%s, %s, %s, %s)",
                           (int(qtd), subtotal, pedido_id, id_prod))
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar itens: {e}")
    finally:
        try: cursor.close(); conexao.close()
        except: pass

def iniciar():
    global combo_produto, dict_produtos, entry_quantidade, tree, label_total
    janela = tk.Toplevel(); janela.title("Itens do Pedido"); janela.geometry("760x460")
    produtos = carregar_produtos(); dict_produtos = {nome: (id, float(preco)) for id, nome, preco in produtos}
    tk.Label(janela, text="Produto").grid(row=0, column=0, sticky="w")
    combo_produto = ttk.Combobox(janela, values=list(dict_produtos.keys()), width=60); combo_produto.grid(row=0, column=1, padx=5, pady=2)
    tk.Label(janela, text="Quantidade").grid(row=1, column=0, sticky="w"); entry_quantidade = tk.Entry(janela, width=10); entry_quantidade.grid(row=1, column=1, sticky="w", padx=5)
    tk.Button(janela, text="Adicionar", command=adicionar_produto).grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(janela, text="Remover Item", command=remover_item).grid(row=2, column=2, padx=5, pady=5)

    tree = ttk.Treeview(janela, columns=("IDProd","Produto","Qtd","Preço","Subtotal"), show="headings", height=12)
    for c in ("IDProd","Produto","Qtd","Preço","Subtotal"): tree.heading(c, text=c); tree.column(c, width=120)
    tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    label_total = tk.Label(janela, text="Total: R$ 0.00"); label_total.grid(row=4, column=0, columnspan=3, sticky="e", padx=10, pady=5)
