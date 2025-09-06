from mongoengine import (
    Document, EmbeddedDocument,
    StringField, IntField, ListField, EmbeddedDocumentField, connect
)

connect(
    db="x",              # nome do banco
    username="x",      # usuário criado no MongoDB
    password="x",      # senha do usuário
    host="10.0.237.41",            # ou IP/hostname do servidor
    port=27017,
    authentication_source="x"  # normalmente "admin" ou o próprio db
)


class Musica(EmbeddedDocument):
    titulo = StringField(required=True, max_length=100)
    duracao = IntField(min_value=1)

    def __str__(self):
        return f"{self.titulo} ({self.duracao}s)"


class Album(EmbeddedDocument):
    titulo = StringField(required=True, max_length=100)
    ano = IntField(min_value=1900, max_value=2100)
    musicas = ListField(EmbeddedDocumentField(Musica))

    def __str__(self):
        return f"{self.titulo} - {self.ano}"


class Artista(Document):
    nome = StringField(required=True, max_length=100)
    albuns = ListField(EmbeddedDocumentField(Album))

    def __str__(self):
        return f"{self.nome}"


def criar_artista():
    nome = input("Nome do artista: ")
    artista = Artista(nome=nome, albuns=[])
    artista.save()
    print(f"✅ Artista '{nome}' criado com sucesso!")


def criar_album():
    listar_artistas()
    nome_artista = input("Digite o nome do artista: ")
    artista = Artista.objects(nome=nome_artista).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return
    titulo = input("Título do álbum: ")
    ano = int(input("Ano do álbum: "))
    novo_album = Album(titulo=titulo, ano=ano, musicas=[])
    artista.albuns.append(novo_album)
    artista.save()
    print(f"✅ Álbum '{titulo}' adicionado ao artista {artista.nome}!")


def criar_musica():
    listar_tudo()
    nome_artista = input("Digite o nome do artista: ")
    artista = Artista.objects(nome=nome_artista).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return
    titulo_album = input("Digite o título do álbum: ")
    for album in artista.albuns:
        if album.titulo == titulo_album:
            titulo_musica = input("Título da música: ")
            duracao = int(input("Duração em segundos: "))
            nova_musica = Musica(titulo=titulo_musica, duracao=duracao)
            album.musicas.append(nova_musica)
            artista.save()
            print(f"✅ Música '{titulo_musica}' adicionada ao álbum {album.titulo}!")
            return
    print("⚠️ Álbum não encontrado!")


def listar_artistas():
    print("\n🎤 Lista de artistas:")
    for artista in Artista.objects:
        print(f"- {artista.nome}")

def listar_musicas_album():
    listar_tudo()
    nome_artista = input("\nDigite o nome do artista: ")
    artista = Artista.objects(nome=nome_artista).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return

    titulo_album = input("Digite o título do álbum: ")
    for album in artista.albuns:
        if album.titulo == titulo_album:
            print(f"\n🎵 Músicas do álbum '{album.titulo}':")
            if not album.musicas:
                print("   (sem músicas cadastradas)")
            for musica in album.musicas:
                print(f"   - {musica.titulo} ({musica.duracao}s)")
            return

    print("⚠️ Álbum não encontrado!")


def listar_tudo():
    print("\n📋 Catálogo completo:")
    for artista in Artista.objects:
        print(f"🎤 {artista.nome}")
        for album in artista.albuns:
            print(f"   📀 {album.titulo} ({album.ano})")
            for musica in album.musicas:
                print(f"      🎵 {musica.titulo} - {musica.duracao}s")


def atualizar_artista():
    listar_artistas()
    nome_artista = input("Digite o nome do artista a ser atualizado: ")
    artista = Artista.objects(nome=nome_artista).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return
    novo_nome = input(f"Novo nome para '{artista.nome}': ")
    artista.nome = novo_nome
    artista.save()
    print(f"✅ Nome do artista atualizado para {novo_nome}!")


def deletar_artista():
    listar_artistas()
    nome_artista = input("Digite o nome do artista a ser deletado: ")
    artista = Artista.objects(nome=nome_artista).first()
    if not artista:
        print("⚠️ Artista não encontrado!")
        return
    artista.delete()
    print(f"✅ Artista '{nome_artista}' e seus álbuns/músicas foram removidos!")


def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Criar Artista")
        print("2 - Criar Álbum")
        print("3 - Criar Música")
        print("4 - Listar Artistas")
        print("5 - Listar Músicas de um Álbum")
        print("6 - Listar Catálogo Completo")
        print("7 - Atualizar Artista")
        print("8 - Deletar Artista")
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
            listar_musicas_album()
        elif opcao == "6":
            listar_tudo()
        elif opcao == "7":
            atualizar_artista()
        elif opcao == "8":
            deletar_artista()
        elif opcao == "0":
            print("👋 Saindo da aplicação...")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
    
