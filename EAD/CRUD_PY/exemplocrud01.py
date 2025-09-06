from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient('10.0.237.41',
                     username='x',
                     password='x',
                     authSource='x',
                     authMechanism='SCRAM-SHA-256',
                     serverSelectionTimeoutMS=5000)

db = client['teste']  # ou outro nome de banco de dados
collection = db['seriados']

def inserir_seriado():
    try:
        _id = int(input("ID do seriado: "))
        nome = input("Nome do seriado: ")
        personagens = input("Personagens (separados por vírgula): ").split(',')
        personagens = [p.strip() for p in personagens]
        pais_origem = input("País de origem: ")
        canal = input("Canal: ")
        ano_ultimo_episodio = int(input("Ano do último episódio: "))

        seriado = {
            "_id": _id,
            "nome": nome,
            "personagens": personagens,
            "pais_origem": pais_origem,
            "canal": canal,
            "ano_ultimo_episodio": ano_ultimo_episodio
        }

        collection.insert_one(seriado)
        print("Seriado inserido com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir: {e}")

def listar_seriados():
    print("\n--- Lista de Seriados ---")
    for seriado in collection.find():
        print(f"ID: {seriado['_id']}")
        print(f"Nome: {seriado['nome']}")
        print(f"Personagens: {', '.join(seriado['personagens'])}")
        print(f"País de Origem: {seriado['pais_origem']}")
        print(f"Canal: {seriado['canal']}")
        print(f"Ano do Último Episódio: {seriado['ano_ultimo_episodio']}\n")

def atualizar_seriado():
    try:
        _id = int(input("ID do seriado a atualizar: "))
        campo = input("Campo a atualizar (nome, personagens, pais_origem, canal, ano_ultimo_episodio): ")

        if campo == "personagens":
            novo_valor = input("Novo valor (personagens separados por vírgula): ").split(',')
            novo_valor = [p.strip() for p in novo_valor]
        elif campo == "ano_ultimo_episodio":
            novo_valor = int(input("Novo valor: "))
        else:
            novo_valor = input("Novo valor: ")

        collection.update_one({"_id": _id}, {"$set": {campo: novo_valor}})
        print("Seriado atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar: {e}")

def deletar_seriado():
    try:
        _id = int(input("ID do seriado a deletar: "))
        collection.delete_one({"_id": _id})
        print("Seriado deletado com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar: {e}")

def menu():
    while True:
        print("\n--- Menu CRUD Seriados ---")
        print("1. Inserir seriado")
        print("2. Listar seriados")
        print("3. Atualizar seriado")
        print("4. Deletar seriado")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            inserir_seriado()
        elif opcao == '2':
            listar_seriados()
        elif opcao == '3':
            atualizar_seriado()
        elif opcao == '4':
            deletar_seriado()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
