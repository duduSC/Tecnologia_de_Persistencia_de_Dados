from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

host="177.67.253.61"
username="x"
password="x"
authSource="x"
port = 27017
mongo_db_name= "x"


client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{mongo_db_name}",authSource=authSource,serverSelectionTimeoutMS=5000)


# try:
#     client.admin.command('ping')
#     print("Conexão com o MongoDB bem-sucedida!")
#     db = client[mongo_db_name]
#     motoboys = db["motoboys"]
#     print("Coleção acessada.")

# except ConnectionFailure as e:
#     print(f" Falha na conexão com o servidor: {e}")
# except Exception as e:
#     print(f" Ocorreu um erro: {e}")

# finally:
#     if 'client' in locals() and client:
#         client.close()
#         print("Conexão fechada.")


db = client[mongo_db_name]
collection = db["motoboys"]

def create_motoboy():
    try:
        _id= int(input("Insira um id para o motoboy: "))
        _cpf = str(input("Insira o cpf do motoboy: "))
        _nome = str(input("Insira o nome do motoboy: "))
        _telefone = str(input("Insira o telefone do motoboy: "))

        motoboy = {
            "_id": _id,
            "cpf": _cpf,
            "nome":_nome,
            "telefone":_telefone
        }
        collection.insert_one(motoboy)
        print("Motoboy adicionado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao inserir : {e}")

def read_motoboys():
    try:
        for motoboy in collection.find():
            print(f"ID: {motoboy['_id']}")
            print(f"CPF: {motoboy['nome']}")
            print(f"Nome: {motoboy['nome']}")
            print(f"Telefone: {motoboy['telefone']}")
    except Exception as e:
        print(f"Erro ao visualizar : {e}")
        
        

def update_motoboy():
    campos_atualizaveis= ["_id","nome","telefone"]
    try:
        _id = int(input("ID do motoboy a atualizar: "))
        campo = input("Campo a atualizar: ")
        if campo in campos_atualizaveis:
            valor = input("Insira o novo valor: ")
        
            collection.update_one({"_id": _id}, {"$set": {campo: valor}})
            print("Motoboy atualizado com sucesso!")
        else:
            print("Campo invalido!")
    except Exception as e:
        print(f"Erro ao atualizar: {e}")
    

def delete_motoboy():
    try:
        _id = int(input("Insira o id do motoboy que será deletado: "))
        collection.delete_one({"_id":_id})
        print("Motoboy excluido com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir: {e}")
        
def main():
    
    while True:
        print("\n--- Menu CRUD Motoboys ---")
        print("1. Inserir motoboy")
        print("2. Listar motoboy")
        print("3. Atualizar motoboy")
        print("4. Deletar motoboy")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                create_motoboy()
            case "2":
                read_motoboys()
            case "3":
                update_motoboy()
            case "4":
                delete_motoboy()
            case "5":
                break
            case _:
                print("Valor invalido!")
                continue
            
if __name__ == "__main__":
    main()