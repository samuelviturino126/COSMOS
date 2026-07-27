import tkinter as tk
from tela_login_classe import TelaLogin
from tela_adm_classe import TelaAdministrador, TelatividadesADM
from tela_bolsistas_classe import TelaBolsista, TelaRegistros

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento")
        self.state('zoomed')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #Usa Strings como Chave do Dicionário para evitar importar as telas nos outros arquivos
        for F in (TelaLogin, TelaAdministrador, TelaBolsista, TelaRegistros):
            frame = F(container, self)
            # F.__name__ pega o nome da classe como uma string (ex: "TelaLogin")
            self.frames[F.__name__] = frame 
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("TelaLogin")

    #Usa o nome da tela para mostrar o frame novo nas outras
    def mostrar_tela(self, nome_da_tela, *args):
        frame = self.frames[nome_da_tela] # Busca o frame usando a string
        if nome_da_tela in ("TelaBolsista", "TelaRegistros") and args:
            id, nome = args
            frame.carregar_dados_e_construir_ui(id, nome) 
        elif nome_da_tela in ("TelaLogin"):
            frame.recarregarbotoes()
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()