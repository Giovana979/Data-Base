import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(host="localhost", user="root", password="12345", database="ecommerce")

def carregar_clientes():
    conexao = conectar(); cursor = conexao.cursor()
    cursor.execute("SELECT idClientes, nome FROM Clientes")
    res = cursor.fetchall(); cursor.close(); conexao.close()
    return res

def inserir_endereco():
    cliente = combo_cliente.get()
    rua = entry_rua.get().strip()
    numero = entry_numero.get().strip()
    bairro = entry_bairro.get().strip()
    cidade = entry_cidade.get().strip()
    estado = entry_estado.get().strip()
    cep = entry_cep.get().strip()

    if not cliente or not rua or not cidade:
        messagebox.showwarning("Atenção", "Preencha Cliente, Rua e Cidade.")
        return

    cliente_id = dict_clientes.get(cliente)
    try:
        conexao = conectar(); cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO Endereco (rua, numero, bairro, cidade, estado, cep, Clientes_idClientes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (rua, numero, bairro, cidade, estado, cep, cliente_id))
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir endereço: {e}")
    finally:
        try: cursor.close(); conexao.close()
        except: pass

    listar(); messagebox.showinfo("Sucesso", "Endereço cadastrado.")

def listar():
    for i in tree.get_children(): tree.delete(i)
    try:
        conexao = conectar(); cursor = conexao.cursor()
        cursor.execute("""SELECT idEndereco, rua, numero, bairro, cidade, estado, cep, Clientes_idClientes FROM Endereco""")
        for r in cursor.fetchall(): tree.insert("", "end", values=r)
    finally:
        try: cursor.close(); conexao.close()
        except: pass

def iniciar():
    global combo_cliente, dict_clientes, entry_rua, entry_numero, entry_bairro, entry_cidade, entry_estado, entry_cep, tree
    janela = tk.Toplevel(); janela.title("Endereços"); janela.geometry("820x460")

    tk.Label(janela, text="Cliente").grid(row=0, column=0, sticky="w")
    clientes = carregar_clientes(); dict_clientes = {nome: id for id, nome in clientes}
    combo_cliente = ttk.Combobox(janela, values=list(dict_clientes.keys()), width=60); combo_cliente.grid(row=0, column=1, padx=5, pady=2, sticky="w")
    tk.Label(janela, text="Rua").grid(row=1, column=0, sticky="w"); entry_rua = tk.Entry(janela, width=60); entry_rua.grid(row=1, column=1, padx=5, pady=2)
    tk.Label(janela, text="Número").grid(row=2, column=0, sticky="w"); entry_numero = tk.Entry(janela, width=15); entry_numero.grid(row=2, column=1, sticky="w", padx=5)
    tk.Label(janela, text="Bairro").grid(row=3, column=0, sticky="w"); entry_bairro = tk.Entry(janela, width=40); entry_bairro.grid(row=3, column=1, padx=5, pady=2, sticky="w")
    tk.Label(janela, text="Cidade").grid(row=4, column=0, sticky="w"); entry_cidade = tk.Entry(janela, width=35); entry_cidade.grid(row=4, column=1, sticky="w", padx=5)
    tk.Label(janela, text="Estado (UF)").grid(row=5, column=0, sticky="w"); entry_estado = tk.Entry(janela, width=10); entry_estado.grid(row=5, column=1, sticky="w", padx=5)
    tk.Label(janela, text="CEP").grid(row=6, column=0, sticky="w"); entry_cep = tk.Entry(janela, width=15); entry_cep.grid(row=6, column=1, sticky="w", padx=5)

    tk.Button(janela, text="Cadastrar Endereço", command=inserir_endereco).grid(row=7, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(janela, columns=("ID","Rua","Numero","Bairro","Cidade","Estado","CEP","ClienteID"), show="headings")
    for c in ("ID","Rua","Numero","Bairro","Cidade","Estado","CEP","ClienteID"): tree.heading(c, text=c)
    tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    listar()
