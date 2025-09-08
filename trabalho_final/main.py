from mongoengine import Document,StringField,ReferenceField,ListField,connect,DecimalField,PULL,NULLIFY
import config

connect(
    db=config.DB_NAME,
    username=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=27017,
    authentication_source=config.DB_AUTHENTICAION_SOURCE
)

class Enderecos(Document):
    rua = StringField()
    bairro= StringField()
    numero= StringField() # string pois existem numeros de enderecos com letras por exemplo 18A
    apartamento= StringField() # '' '' ''
    cep= StringField()
    
    def __str__(self):
        return f"Endereço:{self.rua}   Numero: {self.numero}   AP: {self.apartamento}   Bairro: {self.bairro}   CEP: {self.cep}" 
    
class Pedidos(Document):
    valor = DecimalField()
    endereco= ReferenceField("Enderecos",reverse_delete_rule=NULLIFY)
    motoboy = ReferenceField('Motoboys')    
    
    def __str__(self):
        return f"Valor:{self.valor}, endereço:{self.endereco}, {self.motoboy}"

class Motoboys(Document):
    nome= StringField(max_length=200)
    cpf= StringField(max_length=14,required=True)
    telefone = StringField(max_length=15)
    pedidos= ListField(ReferenceField(Pedidos,reverse_delete_rule=PULL))
    
    def __str__(self):
        return f"Nome: {self.nome}, telefone: {self.telefone},cpf: {self.cpf},pedidos: {self.pedidos}"
    
    
# CREATE

def create_endereco():
    try:
        rua= input("Informe a rua: ")
        bairro = input("Informe o bairro: ")
        numero = input("Informe o numero:")
        ap = input("Informe o ap:")
        cep = input("Informe o cep:")
        endereco = Enderecos(rua=rua,bairro=bairro,numero=numero,apartamento=ap)
        endereco.save()
    except Exception as erro:
        print(f"Erro ao inserir endereco no banco, codigo:{erro}")
        
    print(f"Endereco adicionado com sucesso!")


def create_pedido():
    valor = input("Informe o valor da pedido: ")
    while True:
        read_endereco()
        endereco_id = input("Informe o id do endereco: ")
        endereco = Enderecos.objects(id=endereco_id).first()
        if not endereco:
            print("Id do endereco informado nao existe !!\n Tente novamente")
            continue
        else:
            break
    pedido = Pedidos(valor= valor,endereco= endereco)
    pedido.save()
    print(f"Pedido criado com sucesso!")


def create_motoboy():
    try:
        nome= input("Informe nome: ")
        telefone = input("Informe o telefone: ")
        cpf = input("Informe o cpf:")
        motoboy = Motoboys(nome=nome,telefone=telefone,cpf=cpf)
        motoboy.save()
    except Exception as erro:
        print(f"Erro ao inserir endereco no banco, codigo:{erro}")
        
    print(f"Endereco adicionado com sucesso!")


def atribuir_motoboy_pedido():
    while True:
        read_pedido()
        pedido_id= input("Informe o id do pedido: ")
        pedido = Pedidos.objects(id=pedido_id).first()
        if not pedido:
            print("Id do pedido informado nao existe !!\n Tente novamente")
            continue
        break
    while True:
        read_motoboy()
        id_motoboy = input("Digite o id do motoboy que você deseja atribuir ao pedido ")
        motoboy = Motoboys.objects(id= id_motoboy).first()
        if not motoboy:
            print("Motoboy não encontrado!Tente novamente!")
            continue
        break
    pedido.motoboy = motoboy
    motoboy.pedidos.append(pedido)
    pedido.save()
    motoboy.save()
    print(f"O motoboy {motoboy.nome} foi atribuído ao pedido {pedido.id} ")

# READ

def read_endereco():
    print("Endereços:")
    for endereco in Enderecos.objects:
        print(f"ID: {endereco.id} \n Rua: {endereco.rua} \n Número: {endereco.numero}\n AP: {endereco.apartamento}\n Bairro: {endereco.bairro}\n CEP: {endereco.cep}\n \n ")


def read_pedido():
    print(f"pedidos")
    for pedido in Pedidos.objects:
        if not pedido.motoboy:
            print(f"ID: {pedido.id} | valor: {pedido.valor}")
        else:
            print(f"ID: {pedido.id} | valor: {pedido.valor} Entrega feita por:\n         {pedido.motoboy.nome} | {pedido.motoboy.id} \n Endereco: {str(pedido.endereco)}  \n")

def read_motoboy():
    print("Motoboys:")
    for motoboy in Motoboys.objects:
        if motoboy.pedidos:
            for pedido in motoboy.pedidos:
                endereco_info = str(pedido.endereco) if pedido.endereco else "Endereço não definido"
                print(f"ID: {motoboy.id} | nome: {motoboy.nome},CPF: {motoboy.cpf},telefone: {motoboy.telefone} Pedidos:\n          ID do Pedido: {pedido.id}, Endereço: {endereco_info}\n \n")
        else:
            print(f"ID: {motoboy.id} | nome: {motoboy.nome},CPF: {motoboy.cpf},telefone: {motoboy.telefone}\n \n")


# UPDATE
        

#Pedidos: \n ID: {pedido.id}, Endereço: {endereco_info}
def update_endereco():
    while True:
        read_endereco()
        endereco_id = input("Digite o id da endereco que irá atualizar: ")
        endereco = Enderecos.objects(id=endereco_id).first()
        if not endereco:
            print("Id do endereco informado nao existe !!\n Tente novamente")
            continue
        else:
            break  
    endereco = Enderecos.objects(id= endereco_id).first()
    campos_disponiveis = {
        "1" : "rua",
        "2" : "bairro",
        "3" : "numero",
        "4" : "apartamento"
            }
    while True:
        opcao = input("""
              Selecione qual campo deseja atualizar: 
              1 - Rua
              2 - Bairro
              3 - Numero
              4 - Apartamento
              0 - Cancelar \n""")
        if opcao not in campos_disponiveis:
            print("Valor inválido")
            continue
        else:
            break
    campo = campos_disponiveis[opcao]
    novo_valor = input("Informe o novo valor: ")
    setattr(endereco,campo,novo_valor)
    endereco.save()
    print("Endereco atualizado com sucesso!")
    


def update_motoboy():
    read_motoboy()
    id_motoboy = input("Digite o id da motoboy que irá atualizar: ")
    motoboy = Motoboys.objects(id= id_motoboy).first()
    if not motoboy:
        print("motoboy não encontrada!")
        
    campos_disponiveis = {
        "1" : "nome",
        "2" : "telefone"
            }
    while True:
        opcao = input("""
              Selecione qual campo deseja atualizar: 
              1 - Nome
              2 - Telefone
              0 - Cancelar \n""")
        if opcao == 0 :
            print("Operação cancelada!")
            break
        elif opcao not in campos_disponiveis:
            print("Valor inválido")
            continue
        break
    campo = campos_disponiveis[opcao]
    novo_valor = input("Informe o novo valor: ")
    setattr(motoboy,campo,novo_valor)
    motoboy.save()
    print("motoboy atualizado com sucesso!")


def update_pedido():
    read_pedido()
    id_pedido = input("Digite o id da pedido que irá atualizar: ")
    pedido = Pedidos.objects(id= id_pedido).first()
    if not pedido:
        print("pedido não encontrada!")
        
    campos_disponiveis = {
        "1" : "valor",
        "2" : "endereco",
        "3" : "motoboy"
            }
    while True:
        opcao = input("""
              Selecione qual campo deseja atualizar: 
              1 - Valor
              2 - Endereco
              3 - Motoboy
              0 - Cancelar \n""")
        if opcao == 0 :
            print("Operação cancelada!")
            break
        elif opcao not in campos_disponiveis:
            print("Valor inválido")
            continue
        break
    campo = campos_disponiveis[opcao]
    if campo == "endereco":
        read_endereco()
        endereco_id = input("Digite o id do endereço que você deseja trocar pelo atual: ")
        endereco = Enderecos.objects(id=endereco_id).first()
        pedido.endereco = endereco
    elif campo== "motoboy":
        read_motoboy()
        motoboy_id = input("Digite o id do motoboy que você deseja trocar pelo atual: ")
        motoboy = Motoboys.objects(id=motoboy_id).first()
        pedido.motoboy = motoboy    
    else:
        novo_valor = input("Informe o novo valor: ")
        setattr(pedido,campo,novo_valor)
    pedido.save()
    print("Pedido atualizado com sucesso!")


# DELETE

def delete_endereco():
    read_endereco()
    id_endereco = input("Digite o id da endereco que deseja excluir: ")
    endereco = Enderecos.objects(id=id_endereco).first()
    if not endereco:
        print("endereco não encontrada!")
        return
    endereco.delete()
    print("Endereco atualizado com sucesso!")


def delete_pedido():
    read_pedido()
    id_pedido = input("Digite o id da endereco que deseja excluir: ")
    pedido = Pedidos.objects(id=id_pedido).first()
    if not pedido:
        print("endereco não encontrada!")
        return
    pedido.delete()
    print("Pedido atualizado com sucesso!")


def delete_motoboy():
    read_motoboy()
    id_motoboy = input("Digite o id da endereco que deseja excluir: ")
    motoboy = Motoboys.objects(id=id_motoboy).first()
    if not motoboy:
        print("endereco não encontrada!")
        return
    motoboy.delete()
    print("Motoboy atualizado com sucesso!")




def main():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Criar endereço")
        print("2 - Criar motoboy")
        print("3 - Criar pedido")
        print("4 - Atribuir motoboy a um pedido")
        
        print("5 - Listar endereco")
        print("6 - Listar motoboy")
        print("7 - Listar pedido")

        print("8 - Atualizar endereco")
        print("9 - Atualizar motoboy")
        print("10 - Atualizar pedido")

        print("11 - Deletar endereco")
        print("12 - Deletar motoboy")
        print("13 - Deletar pedido")

        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            create_endereco()
        elif opcao == "2":
            create_motoboy()
        elif opcao == "3":
            create_pedido()
        elif opcao == "4":
            atribuir_motoboy_pedido()


        elif opcao == "5":
            read_endereco()
        elif opcao == "6":
            read_motoboy()
        elif opcao == "7":
            read_pedido()
            

        elif opcao == "8":
            update_endereco()
        elif opcao == "9":
            update_motoboy()
        elif opcao == "10":
            update_pedido()
            

        elif opcao == "11":
            delete_endereco()
        elif opcao == "12":
            delete_motoboy()
        elif opcao == "13":
            delete_pedido()
        
        elif opcao == "0":
            print("👋 Saindo da aplicação...")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
    
