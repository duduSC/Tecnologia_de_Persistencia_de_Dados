
from mongoengine import Document, StringField, IntField, ListField, ReferenceField, connect

connect(
    db="teste",              # nome do banco
    username="teste",      # usuário criado no MongoDB
    password="senha",      # senha do usuário
    host="177.67.253.61",            # ou IP/hostname do servidor
    port=27017,
    authentication_source="teste"  # normalmente "admin" ou o próprio db
)

class Musica(Document):
    titulo = StringField(required=True, max_length=100)
    duracao = IntField(min_value=1)  # duração em segundos


    def __str__(self):      
        return f"{self.titulo} ({self.duracao}s)"


class Album(Document):
    titulo = StringField(required=True, max_length=100)
    ano = IntField(min_value=1900, max_value=2100)
    musicas = ListField(ReferenceField(Musica))

    def __str__(self):
        return f"{self.titulo} - {self.ano}"


class Artista(Document):
    nome = StringField(required=True, max_length=100)
    albuns = ListField(ReferenceField(Album))

    def __str__(self):
        return f"{self.nome}"


def criar_artista():
    nome = input("Nome do artista: ")
    artista = Artista(nome=nome)
    artista.save()
    print(f"✅ Artista '{nome}' criado com sucesso!")


def criar_album():
    listar_artistas()
    artista_id = input("Digite o ID do artista: ")
    artista = Artista.objects(id=artista_id).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return
    titulo = input("Título do álbum: ")
    ano = int(input("Ano do álbum: "))
    album = Album(titulo=titulo, ano=ano)
    album.save()
    artista.albuns.append(album)
    artista.save()
    print(f"✅ Álbum '{titulo}' criado para o artista {artista.nome}!")


def criar_musica():
    listar_albuns()
    album_id = input("Digite o ID do álbum: ")
    album = Album.objects(id=album_id).first()
    if not album:
        print("⚠️ Álbum não encontrado!")
        return
    titulo = input("Título da música: ")
    duracao = int(input("Duração em segundos: "))
    musica = Musica(titulo=titulo, duracao=duracao)
    musica.save()
    album.musicas.append(musica)
    album.save()
    print(f"✅ Música '{titulo}' adicionada ao álbum {album.titulo}!")


def listar_artistas():
    print("\n🎤 Lista de artistas:")
    for artista in Artista.objects:
        print(f"ID: {artista.id} | Nome: {artista.nome}")


def listar_albuns():
    print("\n📀 Lista de álbuns:")
    for album in Album.objects:
        print(f"ID: {album.id} | {album.titulo} ({album.ano})")


def listar_tudo():
    print("\n📋 Catálogo completo:")
    for artista in Artista.objects:
        print(f"🎤 {artista.nome} (ID: {artista.id})")
        for album in artista.albuns:
            print(f"   📀 {album.titulo} ({album.ano}) (ID: {album.id})")
            for musica in album.musicas:
                print(f"      🎵 {musica.titulo} - {musica.duracao}s (ID: {musica.id})")


def atualizar_artista():
    listar_artistas()
    artista_id = input("Digite o ID do artista a ser atualizado: ")
    artista = Artista.objects(id=artista_id).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return
    novo_nome = input(f"Novo nome para '{artista.nome}': ")
    artista.nome = novo_nome
    artista.save()
    print(f"✅ Nome atualizado para {novo_nome}!")


def deletar_artista():
    listar_artistas()
    artista_id = input("Digite o ID do artista a ser deletado: ")
    artista = Artista.objects(id=artista_id).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return
    for album in artista.albuns:
        for musica in album.musicas:
            musica.delete()
        album.delete()
    artista.delete()
    print("✅ Artista e todos os álbuns e músicas foram removidos!")


def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Criar Artista")
        print("2 - Criar Álbum")
        print("3 - Criar Música")
        print("4 - Listar Artistas")
        print("5 - Listar Catálogo Completo")
        print("6 - Atualizar Artista")
        print("7 - Deletar Artista")
        print("0 - Sair")

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
            listar_tudo()
        elif opcao == "6":
            atualizar_artista()
        elif opcao == "7":
            deletar_artista()
        elif opcao == "0":
            print("👋 Saindo da aplicação...")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()


