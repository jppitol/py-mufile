import os
import shutil
from mutagen.easyid3 import EasyID3


def get_album(caminho_arquivo):
    try:
        tags = EasyID3(caminho_arquivo)
        album = tags["album"][0]
        return album
    except Exception:
        return "Unknown Album"


def get_artista(caminho_arquivo):
    try:
        tags = EasyID3(caminho_arquivo)
        artista = tags["artist"][0]
        if '/' in artista:
            artista = artista.split('/')
            return artista[0]
        return artista
    except Exception:
        return "Unknown Artist"


def pack(pasta_principal):
    # criar as pastas de álbuns e mover as músicas para cada pasta dessas
    musicas = [
        i
        for i in os.listdir(pasta_principal)
        if (os.path.isfile(os.path.join(pasta_principal, i)) and i.endswith(".mp3"))
    ]

    for musica in musicas:
        album = get_album(os.path.join(pasta_principal, musica))
        caminho_album = os.path.join(pasta_principal, album)
        if not os.path.exists(caminho_album):
            os.makedirs(caminho_album)
        shutil.move(os.path.join(pasta_principal, musica), caminho_album)

    # criar as pastas de artistas e mover as pastas de álbuns para essas

    albums = [
        i
        for i in os.listdir(pasta_principal)
        if (os.path.isdir(os.path.join(pasta_principal, i)))
    ]

    for album in albums:
        musicas_do_album = [i for i in os.listdir(os.path.join(pasta_principal, album))]
        musica1 = musicas_do_album[0]
        del musicas_do_album
        caminho_musica1 = os.path.join((os.path.join(pasta_principal, album)), musica1)
        del musica1
        artista = get_artista(caminho_musica1)
        if not os.path.exists(os.path.join(pasta_principal, artista)):
            os.makedirs(os.path.join(pasta_principal, artista))
        shutil.move(os.path.join(pasta_principal, album), os.path.join(pasta_principal, artista))

def unpack():
    ...


def organize():
    caminho_pasta_atual = os.path.dirname(os.path.abspath(__file__))
    subpastas = [
        i
        for i in os.listdir(caminho_pasta_atual)
        if os.path.isdir(os.path.join(caminho_pasta_atual, i))
    ]
    if not len(subpastas):
        pack(caminho_pasta_atual)
    else:
        unpack()
        pack(caminho_pasta_atual)


def main():
    print("Please put this file in the directory that contains your songs")
    choice = input("Do you wish to continue? (y/n):").lower()
    match choice:
        case "y":
            organize()
        case "n":
            input("Press Enter to exit:")
        case _:
            print("\nInvalid choice, try again.\n")
            main()


if __name__ == "__main__":
    main()
