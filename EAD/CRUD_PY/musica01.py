from pymongo import MongoClient
from bson.objectid import ObjectId

# Constantes para a conexão com o MongoDB
MONGO_USER = "matricula"
MONGO_PASSWORD = "matricula"
MONGO_HOST = "10.0.237.41" # {"acesso_interno": "10.0.237.41", "acesso_externo": "177.67.253.61"}  
MONGO_PORT = 27017
MONGO_DB_NAME = "matricula"

# Conexão com autenticação usando constantes
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}")

db = client[MONGO_DB_NAME]

# Coleção de artistas (contém álbuns e músicas agregados)
artistas = db["artistas"]

# funcões
def criar_artista():
    nome = input("Nome do Artista: ")
    genero = input("Gênero: ")
    ano_inicio = int(input("Ano de Início: "))
    novo_artista = {"nome": nome, "genero": genero, "ano_inicio": ano_inicio, "albuns": []}
    artistas.insert_one(novo_artista)
    print(f"Artista {nome} adicionado com sucesso!")

def criar_album():
    listar_artistas()
    artista_id = input("ID do Artista: ")
    nome = input("Nome do Álbum: ")
    ano_lancamento = int(input("Ano de Lançamento: "))
    novo_album = {"_id": ObjectId(), "nome": nome, "ano_lancamento": ano_lancamento, "musicas": []}
    
    artistas.update_one(
        {"_id": ObjectId(artista_id)},
        {"$push": {"albuns": novo_album}}
    )
    print(f"Álbum {nome} adicionado ao artista {artista_id} com sucesso!")

def criar_musica():
    listar_albuns_por_artista()
    artista_id = input("ID do Artista: ")
    album_id = input("ID do Álbum: ")
    titulo = input("Título da Música: ")
    duracao = input("Duração (min:seg): ")
    nova_musica = {"_id": ObjectId(), "titulo": titulo, "duracao": duracao}
    
    artistas.update_one(
        {"_id": ObjectId(artista_id), "albuns._id": ObjectId(album_id)},
        {"$push": {"albuns.$.musicas": nova_musica}}
    )
    print(f"Música {titulo} adicionada ao álbum {album_id} com sucesso!")

def listar_artistas():
    print("\nArtistas:")
    for artista in artistas.find():
        print(f"{artista['_id']} - {artista['nome']} ({artista['genero']}, {artista['ano_inicio']})")

def listar_albuns_por_artista():
    listar_artistas()
    artista_id = input("ID do Artista: ")
    artista = artistas.find_one({"_id": ObjectId(artista_id)})
    
    if artista:
        print(f"\nÁlbuns do Artista {artista['nome']}:")
        for album in artista.get("albuns", []):
            print(f"{album['_id']} - {album['nome']} ({album['ano_lancamento']})")
    else:
        print("Artista não encontrado.")

def listar_musicas_por_album():
    listar_albuns_por_artista()
    artista_id = input("ID do Artista: ")
    album_id = input("ID do Álbum: ")
    artista = artistas.find_one({"_id": ObjectId(artista_id), "albuns._id": ObjectId(album_id)})
    
    if artista:
        album = next((album for album in artista.get("albuns", []) if album["_id"] == ObjectId(album_id)), None)
        if album:
            print(f"\nMúsicas do Álbum {album['nome']}:")
            for musica in album.get("musicas", []):
                print(f"{musica['_id']} - {musica['titulo']} ({musica['duracao']})")
        else:
            print("Álbum não encontrado.")
    else:
        print("Artista ou álbum não encontrado.")

def atualizar_artista():
    listar_artistas()
    artista_id = input("ID do Artista a ser atualizado: ")
    novo_nome = input("Novo Nome: ")

    resultado = artistas.update_one({"_id": ObjectId(artista_id)}, {"$set": {"nome": novo_nome}})
    
    if resultado.modified_count > 0:
        print(f"Artista {artista_id} atualizado para {novo_nome}!")
    else:
        print("Nenhum artista foi atualizado. Verifique o ID informado.")

def atualizar_album():
    listar_albuns_por_artista()
    artista_id = input("ID do Artista: ")
    album_id = input("ID do Álbum a ser atualizado: ")
    novo_nome = input("Novo Nome do Álbum: ")

    resultado = artistas.update_one(
        {"_id": ObjectId(artista_id), "albuns._id": ObjectId(album_id)},
        {"$set": {"albuns.$.nome": novo_nome}}
    )
    
    if resultado.modified_count > 0:
        print(f"Álbum {album_id} atualizado para {novo_nome}!")
    else:
        print("Nenhum álbum foi atualizado. Verifique o ID informado.")

def atualizar_musica():
    listar_musicas_por_album()
    artista_id = input("ID do Artista: ")
    album_id = input("ID do Álbum: ")
    musica_id = input("ID da Música a ser atualizada: ")
    novo_titulo = input("Novo Título: ")
    nova_duracao = input("Nova Duração (min:seg): ")

    resultado = artistas.update_one(
        {"_id": ObjectId(artista_id), "albuns._id": ObjectId(album_id), "albuns.musicas._id": ObjectId(musica_id)},
        {"$set": {"albuns.$.musicas.$[m].titulo": novo_titulo, "albuns.$.musicas.$[m].duracao": nova_duracao}},
        array_filters=[{"m._id": ObjectId(musica_id)}]
    )
    
    if resultado.modified_count > 0:
        print(f"Música {musica_id} atualizada para {novo_titulo}!")
    else:
        print("Nenhuma música foi atualizada. Verifique o ID informado.")

def deletar_artista():
    listar_artistas()
    artista_id = input("ID do Artista a ser deletado: ")
    artistas.delete_one({"_id": ObjectId(artista_id)})
    print(f"Artista {artista_id} deletado!")

def deletar_album():
    listar_albuns_por_artista()
    artista_id = input("ID do Artista: ")
    album_id = input("ID do Álbum a ser deletado: ")

    resultado = artistas.update_one(
        {"_id": ObjectId(artista_id)},
        {"$pull": {"albuns": {"_id": ObjectId(album_id)}}}
    )
    
    if resultado.modified_count > 0:
        print(f"Álbum {album_id} deletado!")
    else:
        print("Nenhum álbum foi deletado. Verifique o ID informado.")

def deletar_musica():
    listar_musicas_por_album()
    artista_id = input("ID do Artista: ")
    album_id = input("ID do Álbum: ")
    musica_id = input("ID da Música a ser deletada: ")

    resultado = artistas.update_one(
        {"_id": ObjectId(artista_id), "albuns._id": ObjectId(album_id)},
        {"$pull": {"albuns.$.musicas": {"_id": ObjectId(musica_id)}}}
    )
    
    if resultado.modified_count > 0:
        print(f"Música {musica_id} deletada!")
    else:
        print("Nenhuma música foi deletada. Verifique o ID informado.")

# Menu interativo
def menu_principal():
    while True:
        print("\nMenu Principal\n--------------")
        print("1. Criar Artista")
        print("2. Criar Álbum")
        print("3. Criar Música\n")
        print("4. Listar Artistas")
        print("5. Listar Álbuns por Artista")
        print("6. Listar Músicas por Álbum\n")
        print("7. Atualizar Artista")
        print("8. Atualizar Álbum")
        print("9. Atualizar Música\n")
        print("10. Deletar Artista")
        print("11. Deletar Álbum")
        print("12. Deletar Música\n")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            criar_artista()
        elif opcao == "2":
            criar_album()
        elif opcao == "3":
            criar_musica()
        elif opcao == "4":
            listar_artistas()
        elif opcao == "5":
            listar_albuns_por_artista()
        elif opcao == "6":
            listar_musicas_por_album()
        elif opcao == "7":
            atualizar_artista()
        elif opcao == "8":
            atualizar_album()
        elif opcao == "9":
            atualizar_musica()
        elif opcao == "10":
            deletar_artista()
        elif opcao == "11":
            deletar_album()
        elif opcao == "12":
            deletar_musica()
        elif opcao == "0":
            print("Fim da execução.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executar o menu principal
if __name__ == "__main__":
    menu_principal()

