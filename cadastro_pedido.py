import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",   # coloque a senha correta
        database="ecommerce"
    )

def carregar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT idClientes, nome FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return clientes

def carregar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT idProdutos, nome, preco FROM produtos")
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
    if not tree.get_children():
        messagebox.showwarning("Atenção", "Adicione produtos ao pedido antes de salvar.")
        return

    clientes = carregar_clientes()
    if not clientes:
        messagebox.showwarning("Atenção", "Não há clientes cadastrados.")
        return
    id_cliente = clientes[0][0]

    total_pedido = sum(float(tree.item(item, "values")[4]) for item in tree.get_children())

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql_pedido = "INSERT INTO Pedidos (idClientes, total) VALUES (%s, %s)"
        cursor.execute(sql_pedido, (id_cliente, total_pedido))
        id_pedido = cursor.lastrowid

        sql_item = "INSERT INTO ItensPedido (Pedidos_idPedidos, Produtos_idProdutos, quantidade, subtotal) VALUES (%s, %s, %s, %s)"
        for item in tree.get_children():
            id_produto, produto_nome, quantidade, preco, subtotal = tree.item(item, "values")
            cursor.execute(sql_item, (id_pedido, id_produto, quantidade, subtotal))

        conexao.commit()
        messagebox.showinfo("Sucesso", f"Pedido salvo com sucesso! ID do pedido: {id_pedido}")

        tree.delete(*tree.get_children())
        label_total.config(text="Total: R$ 0.00")

    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar pedido: {e}")
    finally:
        cursor.close()
        conexao.close()


def iniciar():
    global root, combo_produto, entry_quantidade, tree, label_total, dict_produtos

    root = tk.Tk()
    root.title("Cadastro de Pedidos")
    root.geometry("700x500")

    produtos = carregar_produtos()
    dict_produtos = {nome: (id_produto, preco) for id_produto, nome, preco in produtos}

    tk.Label(root, text="Produto:").pack(pady=5)
    combo_produto = ttk.Combobox(root, values=[p[1] for p in produtos])
    combo_produto.pack()

    tk.Label(root, text="Quantidade:").pack(pady=5)
    entry_quantidade = tk.Entry(root)
    entry_quantidade.pack()

    tk.Button(root, text="Adicionar Produto", command=adicionar_produto).pack(pady=10)

    colunas = ("ID", "Produto", "Quantidade", "Preço", "Subtotal")
    tree = ttk.Treeview(root, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
    tree.pack(pady=10, fill="x")

    label_total = tk.Label(root, text="Total: R$ 0.00", font=("Arial", 14))
    label_total.pack(pady=10)

    tk.Button(root, text="Salvar Pedido", command=salvar_pedido).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    iniciar()
