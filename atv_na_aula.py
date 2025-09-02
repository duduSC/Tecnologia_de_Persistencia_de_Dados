from mongoengine import connect,Document,StringField,IntField,ReferenceField

connect(
    db="x",
    username= "x",
    password= "x",
    host= "10.0.237.41",
    port= 27017,
    authentication_source= "x"
)

class Pessoa(Document):
    cpf = IntField()
    nome = StringField(required=True,max_length=100)

    def __str__(self):
        return f"{self.nome},{self.cpf} "
    

class Cidade(Document):
    uf= StringField(required= True)
    nome= StringField(required= True)
    pessoas= ReferenceField(Pessoa)

    def __str__(self):
        return f"{self.uf} , {self.nome}, {self.pessoas} "
    

def create_pessoa():
    cpf= int(input("Informe o CPF: "))
    nome = input("Informe o nome: ")
    pessoa = Pessoa(cpf= cpf,nome= nome)
    pessoa.save()
    print(f"{pessoa.nome} adicionado com sucesso!")


def create_cidade():
    uf = input("Informe a UF da cidade: ")
    nome = input("Informe o nome da cidade: ")
    read_pessoa()
    pessoa_id= input("Informe o id da pessoa: ")
    pessoa= Pessoa.objects(id=pessoa_id).first()
    if not pessoa:
        print("Pessoa não encontrada!")
        return
    cidade = Cidade(uf=uf, nome= nome)
    cidade.pessoas.append(pessoa)
    cidade.save()
    print(f"Cidade criada com sucesso!")


def read_pessoa():
    print("Pessoas:")
    for pessoa in Pessoa.objects:
        print(f"ID: {pessoa.id} | CPF: {pessoa.cpf} | Nome:{pessoa.nome}")


def read_cidade():
    print(f"Cidades")
    for cidade in Cidade.objects:
        print(f"Nome:{cidade.nome}\n UF:{cidade.uf}\n")
        for pessoa in cidade.pessoa:
            print(f"Cidadãos: \n Nome: {pessoa.nome} | Cpf: {pessoa.cpf}")

def delete_cidade():
    read_cidade()
    id_cidade = int(input("Digite o id da Pessoa que deseja excluir: "))
    cidade = Pessoa.objects(id=id_cidade).first()
    if not cidade:
        print("Pessoa não encontrada!")
        return
    for pessoa in cidade.pessoas:
        pessoa.delete()
    cidade.delete()


def update_pessoa():
    read_pessoa()
    id_pessoa = int(input("Digite o id da pessoa que irá atualizar: "))
    pessoa = Pessoa.objects(id= id_pessoa).first()
    if not pessoa:
        print("Pessoa não encontrada!")
    novo_nome = input(f"Novo nome para {pessoa.nome}")
    pessoa.nome = novo_nome
    pessoa.save()
    print("Pessoa atualizado com sucesso!")

def update_cidade():
    read_cidade()
    id_cidade = int(input("Digite o id da cidade que irá atualizar: "))
    cidade = cidade.objects(id= id_cidade).first()
    if not cidade:
        print("Cidade não encontrada!")
    novo_nome = input(f"Novo nome para {cidade.nome}")
    cidade.nome = novo_nome
    cidade.save()
    print("cidade atualizado com sucesso!")


def main():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Criar Pessoa")
        print("2 - Criar Cidade")
        print("3 - Listar Pessoa")
        print("4 - Listar Cidade")
        print("5 - Atualizar Pessoa")
        print("6 - Atualizar Cidade")
        print("7 - Deletar Cidade")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            create_pessoa()
        elif opcao == "2":
            create_cidade()
        elif opcao == "3":
            read_pessoa()
        elif opcao == "4":
            read_cidade()
        elif opcao == "5":
            update_pessoa()
        elif opcao == "6":
            update_cidade()
        elif opcao == "7":
            delete_cidade()
        elif opcao == "0":
            print("👋 Saindo da aplicação...")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
    
