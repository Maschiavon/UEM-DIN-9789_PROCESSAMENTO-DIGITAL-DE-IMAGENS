import numpy as np
import PySimpleGUI as sg
import os, io
from PIL import Image
import math

file_types = [("All files (*.*)", "*.*"),
              ("PNG (*.png)", "*.png"),
              ("JPG (*.jpg)", "*.jpg"),
              ("JPEG (*.jpeg)", "*.jpeg")]

def tela():
    sg.ChangeLookAndFeel("DarkBlue14")
    # Layout
    layout = [  [sg.Text("Trabalho 2 de PROCESSAMENTO DIGITAL DE IMAGENS (RA107115)", font="Roboto")],
                [sg.Text("Insira as informações:", font="Roboto")],
                [
                    sg.Text("M (0 <= m < 360):", font="Roboto"), sg.Input(default_text="0", size=(10, 0), key="txtM"),
                    sg.Text("X:", font="Roboto"), sg.Input(default_text="0", size=(10, 0), key="txtX"),
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
    janela = sg.Window('Alteração de faixa de Matizes em uma imagem no Sistema HSV', layout, icon=r'./ic.ico')
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
                height, width =  imagem.size

                # Limitando altura maxima
                width = (864 if width > 864 else width)
                height = (512 if height > 512 else height)
                imagem_resized = imagem.resize([width, height])

                # Salvando a imagem na memoria em binario
                bio = io.BytesIO()
                imagem_resized.save(bio, format="PNG")

                # Mostrando a imagem na janela
                janela["-IMAGE-"].update(data=bio.getvalue())

        if event == "Transformar Imagem":
            if imagem is not None:
                hsv = np.array(imagem.convert('HSV')) # Transforma a imagem HSV

                m = float(values["txtM"])
                x = float(values["txtX"])

                # Conversão inpropriada
                v_inf = int(math.ceil(255 * (m - x) / 360))
                v_sup = int(math.floor(255 * (m + x) / 360))

                # Se Extourar 256
                v_inf = v_inf % 255
                v_sup = v_sup % 255

                # Se for Negativo trata
                v_sup = (v_sup+255 if v_sup < 0 else v_sup)
                v_inf = (v_inf+255 if v_inf < 0 else v_inf)

                # print(v_inf, v_sup)

                a = hsv[..., 0]
                a_bool = ((v_inf <= a) & (a <= v_sup) if v_inf <= v_sup else (v_inf <= a) | (a <= v_sup))
                a[a_bool] += 128

                # Monstando o HSV a partir da matriz e convertendo para RGB
                nova_imagem = (Image.fromarray(hsv,'HSV')).convert('RGB')

                # Limitando altura maxima
                width, height = imagem.size
                width = (864 if width > 864 else width)
                height = (512 if height > 512 else height)
                nova_imagem_resized = nova_imagem.resize([width,height])

                # Salvando a imagem na memoria em binario
                bio = io.BytesIO()
                nova_imagem_resized.save(bio, format="PNG")

                # Mostrando a imagem na janela
                janela["-IMAGE-"].update(data=bio.getvalue())

        if event == "Salvar Imagem":
            if (imagem is not None) and (nova_imagem is not None):
                # Salvando a imagem no local da pasta da imagem original
                tam_formato = len(imagem.format)
                tam_nome = len(imagem.filename)
                tam_f = tam_nome - tam_formato - 1
                nome_final = imagem.filename[:tam_f] + "_M" + str(m) + "_X" + str(x) + ".png"
                nova_imagem.save(nome_final)

    janela.close()

if __name__ == '__main__':
    tela()
