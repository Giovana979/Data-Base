import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="ecommerce"
    )

def carregar_pedidos_abertos():
    conexao = conectar()
    cursor = conexao.cursor()
    # assumo que Pedidos possui coluna status e idPedidos
    cursor.execute("SELECT idPedidos, total, status FROM Pedidos WHERE status <> 'PAGO' OR status IS NULL")
    pedidos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pedidos

def registrar_pagamento():
    pedido = combo_pedido.get()
    metodo = combo_metodo.get()
    valor = entry_valor.get().strip()
    if not pedido or not metodo or not valor:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return
    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido.")
        return
    pedido_id = int(pedido.split("-")[0].strip())
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
    INSERT INTO pagamento (Pedidos_idPedidos, tipo, status, valor, data)
    VALUES (%s, %s, %s, %s, %s)
""", (pedido_id, metodo, "CONFIRMADO", valor, datetime.now()))

        cursor.execute("UPDATE Pedidos SET status=%s WHERE idPedidos=%s", ("PAGO", pedido_id))
        conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar pagamento: {e}")
    finally:
        try:
            cursor.close(); conexao.close()
        except:
            pass
    messagebox.showinfo("Sucesso", "Pagamento registrado.")
    carregar_lista_pedidos()

def carregar_lista_pedidos():
    pedidos = carregar_pedidos_abertos()
    combo_pedido['values'] = [f"{p[0]} - R$ {float(p[1]):.2f} ({p[2]})" for p in pedidos]

def iniciar():
    global combo_pedido, combo_metodo, entry_valor

    janela = tk.Toplevel()
    janela.title("Registrar Pagamento")
    janela.geometry("520x220")

    tk.Label(janela, text="Pedido").grid(row=0, column=0, sticky="w")
    combo_pedido = ttk.Combobox(janela, width=40)
    combo_pedido.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(janela, text="Método").grid(row=1, column=0, sticky="w")
    combo_metodo = ttk.Combobox(janela, values=["CARTAO", "BOLETO", "PIX", "DINHEIRO"], width=37)
    combo_metodo.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(janela, text="Valor").grid(row=2, column=0, sticky="w")
    entry_valor = tk.Entry(janela, width=20)
    entry_valor.grid(row=2, column=1, padx=5, pady=2)

    tk.Button(janela, text="Registrar Pagamento", command=registrar_pagamento).grid(row=3, column=0, columnspan=2, pady=10)

    carregar_lista_pedidos()
