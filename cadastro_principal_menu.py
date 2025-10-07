import tkinter as tk
from tkinter import messagebox, ttk
from importlib import import_module


try:
    from ttkthemes import ThemedTk
    TkClass = ThemedTk
    tk_theme_kwargs = {"theme": "radiance"}
except Exception:
    TkClass = tk.Tk
    tk_theme_kwargs = {}



def _call_module_start(module_name):
    """Importa um módulo pelo nome e chama .iniciar() se existir, com tratamento de erros."""
    try:
        mod = import_module(module_name)
    except ModuleNotFoundError:
        messagebox.showerror("Erro", f"Módulo '{module_name}' não encontrado.")
        return
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao importar '{module_name}':\n{e}")
        return

    try:
        iniciar = getattr(mod, "iniciar", None)
        if callable(iniciar):
            iniciar()
        else:
            messagebox.showerror("Erro", f"O módulo '{module_name}' não possui função iniciar().")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar {module_name}.iniciar():\n{e}")

def cadastrar_cliente(): _call_module_start("cadastro_clientes")
def cadastrar_produto(): _call_module_start("cadastro_produtos")
def abrir_categorias(): _call_module_start("cadastro_categorias")
def cadastrar_pedido(): _call_module_start("cadastro_pedido")
def consultar_pedidos(): _call_module_start("consulta_pedidos")
def consultar_produto(): _call_module_start("consulta_produto")
def cadastrar_endereco(): _call_module_start("cadastro_endereco")
def cadastro_item_pedido(): _call_module_start("cadastro_itempedido")
def cadastro_pagamento(): _call_module_start("cadastro_pagamento")


def iniciar_menu_principal(id_cliente, nome_cliente):
    """Abre o menu principal do sistema após o login."""
    global root
    root = TkClass(**tk_theme_kwargs)
    root.title("Sistema de Comércio - Menu Principal")
    root.geometry("800x600")

    # Frame de boas-vindas com o nome do usuário logado
    frame_welcome = tk.LabelFrame(root, text="Bem-vindo(a)!", padx=20, pady=20)
    frame_welcome.pack(padx=30, pady=30, fill="both", expand=True)

    label_info = tk.Label(
        frame_welcome,
        text=f"Olá, {nome_cliente}!\n\nSelecione uma opção no menu acima para começar.\nSistema de Gestão de Comércio v1.0",
        justify="left",
        font=("Arial", 11)
    )
    label_info.pack(anchor="w")


    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    menu_cliente = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Cliente", menu=menu_cliente)
    menu_cliente.add_command(label="Cadastrar Cliente", command=cadastrar_cliente)


    menu_produto = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Produto", menu=menu_produto)
    menu_produto.add_command(label="Cadastrar Produto", command=cadastrar_produto)
    menu_produto.add_command(label="Consultar Produto", command=consultar_produto)
    menu_produto.add_command(label="Cadastrar Categoria", command=abrir_categorias)

    menu_pedido = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Pedido", menu=menu_pedido)
    menu_pedido.add_command(label="Cadastrar Pedido", command=cadastrar_pedido)
    menu_pedido.add_command(label="Consultar Pedidos", command=consultar_pedidos)
    menu_pedido.add_command(label="Cadastrar Endereço", command=cadastrar_endereco)
    menu_pedido.add_command(label="Itens do Pedido", command=cadastro_item_pedido)
    menu_pedido.add_command(label="Cadastrar Pagamento", command=cadastro_pagamento)


    def sair():
        if messagebox.askyesno("Sair", "Deseja encerrar a sessão e voltar à tela de login?"):
            root.destroy()
            from login import iniciar_login
            iniciar_login()

    menu_bar.add_command(label="Sair", command=sair)


    try:
        root.iconbitmap("logo.ico")
    except Exception:
        pass 


    root.mainloop()

if __name__ == "__main__":
    
    iniciar_menu_principal(1, "Usuário de Teste")
