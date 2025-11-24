from conectar import conectar
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from pathlib import Path
import tkinter as tk


fonte_personalizada = ("Arial", 14, "bold")
class TelaLogin(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        # Caminhos
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH / "telas" / "tela_login" / "imagens"
        self.imagens = {} #dicionario para guardar as refs das imagens
        
        # O Canvas agora é criado dentro do Frame (self)
        self.canvas = tk.Canvas(self, bg="#FFFFFF", height=1080, width=1920,bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        # Janela Login Imagens e Botões
        self.imagens['cosmos'] = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(432.0,540.0,image=self.imagens['cosmos'])
        self.imagens['entrada1'] = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(1396.5,504.5,image=self.imagens['entrada1'])
        self.imagens['entrada2'] = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(1396.5,612.0,image=self.imagens['entrada2'])
        
        #Botões
        self.imagens['botao1'] = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(self,image=self.imagens['botao1'] ,borderwidth=0,highlightthickness=0,command=lambda: self.login(),relief="flat")
        self.button_1.place(x=1337.0,y=691.0,width=119.0,height=37.0)
        
        # Vincula a tecla ENTER (<Return>) ao método login() para a janela principal (Fallback)
        self.bind('<Return>', lambda event: self.login())
        
        #Textos
        self.canvas.create_text(1350.0,349.0,anchor="nw",text="Login",fill="#000000",font=("Ubuntu Bold", 40 * -1))
        self.canvas.create_text(1238.0,453.0,anchor="nw",text="Usuário",fill="#000000",font=("Inter Medium", 16 * -1))
        
        #Entradas
        self.entrada_nome = Entry(self,bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0,font=("Inter Medium", 16))
        self.entrada_senha = Entry(self,bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0,show="*",font=("Inter Medium", 16))
        
        self.entrada_nome.place(x=1250.0,y=485.0,width=287.0,height=40.0)
        self.entrada_senha.place(x=1253.0,y=595.0, width=287.0,height=40.0)
        self.canvas.create_text(1238.0,558.0,anchor="nw",text="Senha",fill="#000000",font=("Inter Medium", 16 * -1))

        # 🟢 CORREÇÃO: Vincula a tecla Enter diretamente aos campos de entrada para garantir a captura do evento.
        self.entrada_nome.bind('<Return>', lambda event: self.login())
        self.entrada_senha.bind('<Return>', lambda event: self.login())
        
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def login(self):
        nome = self.entrada_nome.get().strip()
        senha = self.entrada_senha.get()

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            # Certifique-se de que a coluna "nomeinst" e "senha" correspondem às suas colunas no banco de dados
            cursor.execute("SELECT id, nome, tipo FROM usuarios WHERE nomeinst = %s AND senha = %s", (nome, senha))
            usuario = cursor.fetchone()
            conexao.close()

            if usuario:
                messagebox.showinfo("Login", f"Bem-vindo, {usuario[1]}!")
                if usuario[2] == 'admin':
                    self.controlador.mostrar_tela("TelaAdministrador")
                else:
                    self.controlador.mostrar_tela("TelaBolsista", usuario[0], usuario[1])
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        self.entrada_nome.unbind('<Return>')
        self.entrada_senha.unbind('<Return>')