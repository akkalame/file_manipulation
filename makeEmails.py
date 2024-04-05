import random
import string

def generar_correo():
    letras = string.ascii_lowercase
    usuario = ''.join(random.choices(letras, k=random.randint(5, 10)))
    dominio = '@gmail.com'
    return usuario + dominio

if __name__ == "__main__":
    cuentas_gmail = [generar_correo() for _ in range(50)]

    with open("direcciones_correo.txt", "w") as archivo:
        for cuenta in cuentas_gmail:
            archivo.write(cuenta + "\n")

    print("Las direcciones de correo electrónico han sido guardadas en el archivo 'direcciones_correo.txt'.")
