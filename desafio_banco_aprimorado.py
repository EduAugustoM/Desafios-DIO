import textwrap

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco


class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario


class Banco:
    def __init__(self):
        self.LIMITE_SAQUES = 3
        self.AGENCIA = "0001"
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.usuarios = []
        self.contas = []

    def exibir_menu(self):
        menu_texto = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(menu_texto))

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.numero_saques = 0
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente números): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/UF): ")

        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_usuario)

        print("=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf):
        usuarios_filtrados = [usuario for usuario in self.usuarios if usuario.cpf == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n=== Conta criada com sucesso! ===")
            numero_conta = len(self.contas) + 1
            nova_conta = Conta(self.AGENCIA, numero_conta, usuario)
            self.contas.append(nova_conta)
        else:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        
    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero_conta}
                Titular:\t{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

    def main(self):
        while True:
            opcao = self.exibir_menu()

            if opcao == "d":
                valor = float(input("Informe o valor do depósito: "))
                self.depositar(valor)

            elif opcao == "s":
                valor = float(input("Informe o valor do saque: "))
                self.sacar(valor)

            elif opcao == "e":
                self.exibir_extrato()

            elif opcao == "nu":
                self.criar_usuario()

            elif opcao == "nc":
                self.criar_conta()

            elif opcao == "lc":
                self.listar_contas()

            elif opcao == "q":
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    banco = Banco()
    banco.main()
