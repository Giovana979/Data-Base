import tkinter as tk
from tkinter import ttk

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

# Loop principal SEMPRE no final
root.mainloop()
