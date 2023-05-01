import numpy as np
import PySimpleGUI as sg
import os, io
from PIL import Image

file_types = [("PNG (*.png)", "*.png"),
              ("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

def tela():
    sg.ChangeLookAndFeel("DarkAmber")
    # Layout
    layout = [  [sg.Text("Trabalho 1 de PROCESSAMENTO DIGITAL DE IMAGENS (RA107115)", font="Roboto")],
                [sg.Text("Insira as informações:", font="Roboto")],
                [
                    sg.Text("T:", font="Roboto"), sg.Input(default_text="120", size=(10, 0), key="txtT"),
                    sg.Text("Brilho:", font="Roboto"), sg.Input(default_text="100", size=(10, 0), key="txtBrilho"),
                    sg.Text("Acima:", font="Roboto"),
                    sg.Radio("True", "group1", key="radioBtnTrue", font="Roboto", default=True),
                    sg.Radio("False", "group1", key="radioBtnFalse", font="Roboto")
                ],
                [
                    sg.Text("Arquivo de Imagem:",  font="Roboto"),
                    sg.Input(size=(25, 1), key="-FILE-"),
                    sg.FileBrowse(button_text="Buscar Imagem",file_types=file_types),
                    sg.Button("Carregar Imagem"),
                    sg.Button("Transformar Imagem"),
                    sg.Button("Salvar Imagem")
                ],
                [sg.Image(key="-IMAGE-")]
              ]
    # Janela
    janela = sg.Window('Programa de Limiarização e Alteração Local de Brilho', layout, icon=r'./ic.ico')
    imagem = None
    while True:
        # Extrair os dados da tela
        event, values = janela.Read()

        # Função para sair do programa
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "Carregar Imagem":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                imagem = Image.open(values["-FILE-"]) # Objeto PIL Image
                width, height = imagem.size

                # Limitando altura maxima
                width = (864 if width > 864 else width)
                height = (512 if height > 512 else height)
                imagem2 = imagem.resize([width,height])

                # Salvando a imagem na memoria em binario
                bio = io.BytesIO()
                imagem2.save(bio, format="PNG")

                # Mostrando a imagem na janela
                janela["-IMAGE-"].update(data=bio.getvalue())

        if event == "Transformar Imagem":
            if imagem is not None:
                matriz = np.array(imagem.convert('L')) # Transforma a imagem para tons de cinza
                matriz = matriz.astype(int) # int32

                Acima = values["radioBtnTrue"]
                t = int(values["txtT"])
                brilho = int(values["txtBrilho"])
                if Acima:
                    # Soma o brilho no intervalo dos valores maiores ou iguais a t
                    matriz[matriz >= t] += brilho
                else:
                    # Soma o brilho no intervalo dos valores menores que t
                    matriz[matriz < t] += brilho

                matriz = np.minimum(np.maximum(matriz, 0), 255) # Limita o valor maximo para 255 e o minimo para 0
                matriz = matriz.astype(np.uint8) # Volta a matriz para o tipo uint8 do numpy
                pil_image= Image.fromarray(matriz) # Transforma de volta pra imagem PIL

                # Limitando altura maxima
                width, height = imagem.size
                width = (864 if width > 864 else width)
                height = (512 if height > 512 else height)
                pil_image2 = pil_image.resize([width,height])

                # Salvando a imagem na memoria em binario
                bio = io.BytesIO()
                pil_image2.save(bio, format="PNG")

                # Mostrando a imagem na janela
                janela["-IMAGE-"].update(data=bio.getvalue())

        if event == "Salvar Imagem":
            if imagem is not None:
                # Salvando a imagem no local da pasta da imagem original
                tam_formato = len(imagem.format)
                tam_nome = len(imagem.filename)
                tam_f = tam_nome - tam_formato
                nome_final = imagem.filename[:tam_f] + "_Brilho" + str(brilho) + "_T" + str(t) + "_Acima" + str(Acima) + ".png"
                pil_image.save(nome_final)

    janela.close()

if __name__ == '__main__':
    tela()
