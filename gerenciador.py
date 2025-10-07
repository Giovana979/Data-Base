import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="ecommerce"
    )


def inserir_funcionario():
    nome = input("Nome: ")
    cargo = input("Cargo: ")
    salario = float(input("Salário: "))
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO funcionarios (nome, cargo, salario)
        VALUES (%s, %s, %s)
    """, (nome, cargo, salario))
    conexao.commit()
    print("Funcionário inserido com sucesso.")
    cursor.close()
    conexao.close()


def atualizar_funcionario():
    id_func = int(input("ID do funcionário a atualizar: "))
    novo_salario = float(input("Novo salário: "))
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE funcionarios
        SET salario = %s
        WHERE id = %s
    """, (novo_salario, id_func))
    conexao.commit()
    print("Salário atualizado.")
    cursor.close()
    conexao.close()


def remover_funcionario():
    id_func = int(input("ID do funcionário a remover: "))
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        DELETE FROM funcionarios
        WHERE id = %s
    """, (id_func,))
    conexao.commit()
    print("Funcionário removido.")
    cursor.close()
    conexao.close()


def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()
    print("\nLista de Funcionários:")
    for f in funcionarios:
        print(f"ID: {f[0]} | Nome: {f[1]} | Cargo: {f[2]} | Salário: R${f[3]:.2f}")
    cursor.close()
    conexao.close()


def menu():
    while True:
        print("\n=== MENU FUNCIONÁRIOS ===")
        print("1. Inserir funcionário")
        print("2. Atualizar salário")
        print("3. Remover funcionário")
        print("4. Listar funcionários")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            inserir_funcionario()
        elif opcao == "2":
            atualizar_funcionario()
        elif opcao == "3":
            remover_funcionario()
        elif opcao == "4":
            listar_funcionarios()
        elif opcao == "0":
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
