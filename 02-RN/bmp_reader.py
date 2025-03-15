import os


def decode_bmp(f):
    # Pula para os dados
    f.seek(0x0A)
    data_offset = int.from_bytes(f.read(4), "little")
    f.seek(data_offset)

    # Lê o alfa de cada pixel
    return [min(1, byte) for byte in f.read()[3::4]]


def read(folder="numeros"):
    return [
        decode_bmp(open(os.path.join(folder, filename), "rb"))
        for filename in sorted(os.listdir(folder))
    ]
