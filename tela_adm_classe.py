import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import *
from conectar import conectar
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
import psycopg2
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io

# NOTA: A classe TelaCadUsuario2 é chamada por TelaAdministrador
# A classe TelaCadUsuarios foi removida por estar quebrada e sem uso.

class TelaAdministrador(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH / "telas" / "tela_adm_nova" / "imagens"
        self.imagens = {}

        # --- DADOS ---
        # CORREÇÃO: Coleta os dados ANTES de desenhar os widgets
        self.coletar_dados_adm() 

        # --- CANVAS ---
        self.canvastelaprincipaladm = tk.Canvas(self, bg="#FFFFFF", height=1080, width=1920,bd=0, highlightthickness=0, relief="ridge")
        self.canvastelaprincipaladm.place(x=0, y=0)
        
        # --- Textos ---
        self.canvastelaprincipaladm.create_text(375.0,497.0,anchor="nw",text="Atividades mais registradas por setor",fill="#000000",font=("Ubuntu Bold", 40 * -1))
        self.canvastelaprincipaladm.create_text(376.0,123.0,anchor="nw",text="Olá, Everton!",fill="#2C3638",font=("Ubuntu Bold", 24 * -1))
        self.canvastelaprincipaladm.create_text(1243.0,899.1416015625,anchor="nw",text="Processamento técnico",fill="#2C3638",font=("Ubuntu Medium", 24 * -1))
        self.canvastelaprincipaladm.create_text(830.0,899.1416015625,anchor="nw",text="Reprografia",fill="#2C3638",font=("Ubuntu Medium", 24 * -1))
        self.canvastelaprincipaladm.create_text(424.0,899.1416015625,anchor="nw",text="Atendimento",fill="#2C3638",font=("Ubuntu Medium", 24 * -1))
        
        # --- Imagens de Fundo (Estáticas) ---
        self.imagens['quadradomenor'] = PhotoImage(file=self.relative_to_assets("quadradomenor.png"))
        self.canvastelaprincipaladm.create_image(763.0,333.0,image=self.imagens['quadradomenor'])
        self.canvastelaprincipaladm.create_image(1162.0,333.0,image=self.imagens['quadradomenor'])
        
        self.imagens['quadradomaior'] = PhotoImage(file=self.relative_to_assets("quadradomaior.png"))
        self.canvastelaprincipaladm.create_image(560.0,797.0,image=self.imagens['quadradomaior'])
        self.canvastelaprincipaladm.create_image(966.0,797.0,image=self.imagens['quadradomaior'])
        self.canvastelaprincipaladm.create_image(1379.0,797.0,image=self.imagens['quadradomaior'])
        
        # Placeholders dos gráficos (imagens estáticas)
        self.image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.image_6 = self.canvastelaprincipaladm.create_image(1378.8583984375,777.8583984375,image=self.image_image_6)
        self.image_image_7 = PhotoImage(file=self.relative_to_assets("image_7.png"))
        self.image_7 = self.canvastelaprincipaladm.create_image(965.8583984375,777.8583984375,image=self.image_image_7)
        self.image_image_8 = PhotoImage(file=self.relative_to_assets("image_8.png"))
        self.image_8 = self.canvastelaprincipaladm.create_image(559.8584289550781,777.8583984375,image=self.image_image_8)
        
        # Header
        self.image_image_9 = PhotoImage(file=self.relative_to_assets("retangulogrande.png"))
        self.image_9 = self.canvastelaprincipaladm.create_image(961.0,43.0,image=self.image_image_9)
        self.image_image_10 = PhotoImage(file=self.relative_to_assets("usuario.png"))
        self.image_10 = self.canvastelaprincipaladm.create_image(420.0,42.5,image=self.image_image_10)

        # --- Botões ---
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: print("button_1 clicked"),relief="flat",background="white")
        self.button_1.place(x=1486.0,y=22.0,width=34.0,height=34.0)

        # CORREÇÃO: Botão aponta para o método correto
        self.botao_atividades_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.botao_atividades = Button(self,image=self.botao_atividades_image_2,borderwidth=0,highlightthickness=0,command=lambda:(print("oi")),relief="flat",background="white")
        self.botao_atividades.place(x=1041.0,y=33.5,width=81.0,height=19.0)

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=self.abrir_tela_cad_usuario,relief="flat",background="white")
        self.button_3.place(x=1152.0,y=33.5,width=69.0,height=19.0)

        # CORREÇÃO: Botão aponta para o método correto
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(self,image=self.button_image_4,borderwidth=0,highlightthickness=0,command=self.abrir_tela_atividades,relief="flat",background="white")
        self.button_4.place(x=1251.0,y=22.0,width=214.0,height=42.0)

        # --- Contadores Dinâmicos ---
        self.image_image_11 = PhotoImage(file=self.relative_to_assets("image_11.png"))
        self.image_11 = self.canvastelaprincipaladm.create_image(763.0,273.0,image=self.image_image_11)
        
        # CORREÇÃO: Usa a variável 'self.atividades_do_mes'
        self.canvastelaprincipaladm.create_text(750.0, 315.0, anchor="ne", text=f"{self.atividades_do_mes}", fill="#2C3638", font=("Ubuntu Bold", 40 * -1))
        self.canvastelaprincipaladm.create_text(627.0,371.0,anchor="nw",text="Registros de atividades nesse mês!",fill="#2C3638",font=("Ubuntu Medium", 24 * -1))

        self.image_image_12 = PhotoImage(file=self.relative_to_assets("image_12.png"))
        self.image_12 = self.canvastelaprincipaladm.create_image(1162.0,273.0,image=self.image_image_12)
        
        # CORREÇÃO: Usa a variável 'self.atividades_do_dia'
        self.canvastelaprincipaladm.create_text(1150.0, 315.0, anchor="ne", text=f"{self.atividades_do_dia}", fill="#2C3638", font=("Ubuntu Bold", 40 * -1))
        self.canvastelaprincipaladm.create_text(1026.0,371.0,anchor="nw",text="Registros das atividade de hoje!",fill="#2C3638",font=("Ubuntu Medium", 24 * -1))
        
        # --- Gráficos Dinâmicos ---
        # CORREÇÃO: Chama o método para desenhar os gráficos
        self.graficos() 

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    # CORREÇÃO: Novo método para o botão "Atividades"
    def abrir_tela_atividades(self):
        # Este método assume que seu controlador tem "TelatividadesADM" registrada
        TelatividadesADM(self)

    # CORREÇÃO: Novo método para o botão "Cadastrar"
    def abrir_tela_cad_usuario(self):
        # Abre o popup Toplevel para cadastrar usuário
        TelaCadUsuario2(self)
        
    def coletar_dados_adm(self):
        conexao = conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    SELECT COUNT(id)
                    FROM atividades_realizadas
                    WHERE EXTRACT(MONTH FROM data) = EXTRACT(MONTH FROM CURRENT_DATE)
                    AND EXTRACT(YEAR FROM data) = EXTRACT(YEAR FROM CURRENT_DATE)
                """)
                resultado = cursor.fetchone()
                self.atividades_do_mes = resultado[0] if resultado else 0
                cursor.execute("""
                    SELECT COUNT(id)
                    FROM atividades_realizadas
                    WHERE data::date = CURRENT_DATE
                """)
                resultado = cursor.fetchone()
                self.atividades_do_dia = resultado[0] if resultado else 0
            except Exception as e:
                messagebox.showerror("Erro de Banco", f"Não foi possível buscar os dados: {e}")
                self.atividades_do_mes = "Erro"
                self.atividades_do_dia = "Erro"
            finally:
                conexao.close()
        else:
            self.atividades_do_mes = "Erro"
            self.atividades_do_dia = "Erro"
            
    def voltar(self):
        print("oi")
    
    def graficos(self):
        # --- Este é um GRÁFICO DE EXEMPLO ---
        # Você precisará buscar os dados reais do banco
        
        # Dados do gráfico 
        self.labels = ['A', 'B', 'C', 'D'] # Labels de exemplo
        self.sizes = [15, 30, 45, 10]     # Valores de exemplo
        self.colors = ['#555555', '#888888', '#AAAAAA', '#CCCCCC']

        # Cria a figura do gráfico
        fig, ax = plt.subplots(figsize=(3.7, 2.19), dpi=100) 
        ax.pie(self.sizes, labels=self.labels, colors=self.colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal') 

        # Salva a figura em memória como imagem
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)

        # Carrega a imagem com PIL
        img = Image.open(buf)
        
        # CORREÇÃO: Salva a imagem em self.imagens para evitar garbage collection
        self.imagens['grafico_atendimento'] = ImageTk.PhotoImage(img)

        # CORREÇÃO: Usa create_image para desenhar no canvas nas coordenadas corretas
        # (coordenadas do placeholder image_8)
        self.canvastelaprincipaladm.create_image(
            559.85, 
            777.85, 
            image=self.imagens['grafico_atendimento']
        )

        plt.close(fig) # Evita vazamento de memória
    
class TelatividadesADM(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        # --- 1. Configurações da Janela (Popup) ---
        self.title("Cadastrar Nova Atividade Padrão")
        # O canvas original tinha 770x640, vamos usar isso
        self.geometry("770x640") 
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        # --- 2. Caminhos e Imagens ---
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH / "telas" / "tela_atividades" / "imagens"
        self.imagens = {}
        
        # --- 3. Canvas Principal ---
        # O canvas agora preenche o Toplevel
        self.canvas_tela_atividade = tk.Canvas(self,bg = "#FFFFFF",height = 640,width = 770,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas_tela_atividade.pack() # Usar pack() para preencher
        
        # --- 4. Elementos Gráficos (Textos e Imagens de Fundo) ---
        # (Todas as coordenadas .create_ e .place() podem ser mantidas,
        # pois o canvas e a janela agora têm o mesmo tamanho)
        
        #Textos
        self.canvas_tela_atividade.create_text( 100.0, 241.0, anchor="nw", text="Descrição:", fill="#000000", font=("Inter", 25 * -1))
        self.canvas_tela_atividade.create_text(100.0,151.0,anchor="nw",text="Setor:",fill="#000000",font=("Inter", 25 * -1))
        self.canvas_tela_atividade.create_text(420.0,151.0,anchor="nw",text="Tipo:",fill="#000000",font=("Inter", 25 * -1))
        self.canvas_tela_atividade.create_text(100.0, 61.0, anchor="nw", text="Nova atividade", fill="#000000", font=("Inter Medium", 25 * -1))

        # Imagens de fundo para entradas
        self.tela_atividade_entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.tela_atividade_entry_bg_1 = self.canvas_tela_atividade.create_image(383.5,121.0,image=self.tela_atividade_entry_image_1)
        
        self.tela_atividade_entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.tela_atividade_entry_bg_2 = self.canvas_tela_atividade.create_image(383.0,383.0,image=self.tela_atividade_entry_image_2)
        
        self.tela_atividade_image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.tela_atividade_image_1 = self.canvas_tela_atividade.create_image(223.0,206.0,image=self.tela_atividade_image_image_1)

        self.tela_atividade_image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.tela_atividade_image_2 = self.canvas_tela_atividade.create_image(543.0, 206.0, image=self.tela_atividade_image_image_2)

        # --- 5. Widgets (Botões, Entradas, Comboboxes) ---
        # (Eles são colocados sobre o canvas, com 'self' como master)
        
        # Botão Cadastrar (button_1)
        self.tela_atividade_button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.tela_atividade_button_1 = Button(self,image=self.tela_atividade_button_image_1,borderwidth=0,highlightthickness=0,command=self.cadastrar_atividade,relief="flat",background="white")
        self.tela_atividade_button_1.place(x=548.0,y=537.0,width=119.0,height=40.0)
        
        # Botão Fechar (X) (button_2)
        # CORREÇÃO: Removido 'controlador', comando agora é 'self.destroy'
        self.tela_atividade_button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.tela_atividade_button_2 = Button(self,image=self.tela_atividade_button_image_2,borderwidth=0,highlightthickness=0,command=self.destroy,relief="flat",background="white")
        self.tela_atividade_button_2.place(x=690.0,y=17.0,width=54.8,height=54.8)
        
        # Botão Cancelar (button_3)
        # CORREÇÃO: Comando agora é 'self.destroy'
        self.tela_atividade_button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.tela_atividade_button_3 = Button(self, image=self.tela_atividade_button_image_3, borderwidth=0, highlightthickness=0, command=self.destroy, relief="flat",background="white")
        self.tela_atividade_button_3.place(x=410.0, y=534.0, width=122.0, height=43.0)

        # Entry (Nome)
        self.nome_nova_atividade = Entry(self, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0, font=("Inter", 16))
        self.nome_nova_atividade.place(x=105.0,y=101.0,width=557.0,height=40.0)

        # Text (Descrição)
        self.entry_descricao_atividade = Text(self, bd=0, bg="#FFFFFF",fg="#000716",highlightthickness=0, font=("Inter", 16))
        self.entry_descricao_atividade.place(x=105.0,y=286.0,width=556.0,height=194.0)

        # Combobox Setor
        self.combobox_width = 250
        self.combobox_height = 45
        self.combobox_x = 223 - self.combobox_width / 2
        self.combobox_y = 206 - self.combobox_height / 2
        self.setor_atividade = ttk.Combobox(self, values=["Processamento Técnico", "Reprografia", "Atendimento", "Acervo e Midias Digitais", "Selecione"], state="readonly")
        self.setor_atividade.current(4)
        self.setor_atividade.place(x=self.combobox_x, y=self.combobox_y, width=self.combobox_width, height=self.combobox_height)

        # Combobox Tipo
        self.combobox_x2 = 543 - self.combobox_width / 2
        self.combobox_y2 = 206 - self.combobox_height / 2
        self.tipo_atividade = ttk.Combobox(self,values=["Horas", "Quantidade", "Selecione"],state="readonly")
        self.tipo_atividade.current(2)
        self.tipo_atividade.place(x=self.combobox_x2, y=self.combobox_y2, width=self.combobox_width, height=self.combobox_height)

        # --- 6. Tornar a Janela Modal ---
        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
        
    def cadastrar_atividade(self):
        conexao = conectar()
        if not conexao:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")
            return

        self.nome = self.nome_nova_atividade.get()
        self.tipo = self.tipo_atividade.get()
        self.setor = self.setor_atividade.get()
        self.descricao = self.entry_descricao_atividade.get("1.0", "end-1c").strip()
        
        cursor = conexao.cursor()

        if not self.nome or self.tipo == "Selecione" or not self.tipo or self.setor == "Selecione" or not self.setor:
            messagebox.showerror("Erro!", "Preencha todas as lacunas obrigatórias (Nome, Tipo, Setor)")
            conexao.close()
            return # Mantém o popup aberto para correção
        
        try:
            # (Assumindo que sua tabela NÃO tem 'descricao', como no código original)
            cursor.execute(
                "INSERT INTO atividades_padrao (nome, tipo, setor) VALUES (%s, %s, %s)",
                (self.nome, self.tipo, self.setor)
            )
            # Se sua tabela TIVER 'descricao', use esta query:
            # cursor.execute(
            #    "INSERT INTO atividades_padrao (nome, tipo, setor, descricao) VALUES (%s, %s, %s, %s)",
            #    (self.nome, self.tipo, self.setor, self.descricao)
            # )
            
            conexao.commit()
            messagebox.showinfo("Feito!", "Atividade Cadastrada!")
            
            # Limpa os campos
            self.nome_nova_atividade.delete(0, 'end')
            self.tipo_atividade.current(2)
            self.setor_atividade.current(4)
            self.entry_descricao_atividade.delete("1.0", 'end')
            
            # Fecha o popup
            self.destroy() 
            
        except Exception as e:
            messagebox.showerror("Erro de Banco", f"Erro ao cadastrar atividade: {e}")
        finally:
            conexao.close()
class TelaCadUsuario2(Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Novo Registro de Usuario")
        self.geometry("780x538")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)
        self.imagens = {}
        
        OUTPUT_PATH = Path(__file__).parent
        # CORREÇÃO: Typo no nome da variável
        self.ASSETS_PATH = OUTPUT_PATH / "telas" / "tela_cad_usuario" 
        
        self.canvas = Canvas(self, bg="#FFFFFF", height=538, width=780, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack()
        
        # Textos
        self.canvas.create_text(100.0,340.0,anchor="nw",text="Senha:",fill="#000000",font=("Inter", 25 * -1))
        self.canvas.create_text(100.0,250.0,anchor="nw",text="Login:",fill="#000000",font=("Inter", 25 * -1))
        self.canvas.create_text(341.0,250.0,anchor="nw",text="Tipo de usuário",fill="#000000",font=("Inter", 25 * -1))
        self.canvas.create_text(101.0,61.0,anchor="nw",text="Nome",fill="#000000",font=("Inter Medium", 25 * -1))
        self.canvas.create_text(100.0,151.0,anchor="nw",text="E-mail institucional",fill="#000000",font=("Inter Medium", 25 * -1))

        # Botões
        # CORREÇÃO: O 'command' agora chama o cadastro
        self.imagens['botao_1'] = PhotoImage(file=self._relative_to_assets("button_1.png"))
        self.button_1 = Button(self, image=self.imagens['botao_1'],borderwidth=0,highlightthickness=0,command=self.cadastrar_bolsista,relief="flat",background="white")
        self.button_1.place(x=548.0,y=458.0,width=119.0,height=40.0)
        
        self.imagens['botao_2']  = PhotoImage(file=self._relative_to_assets("button_2.png"))
        self.button_2 = Button(self,image=self.imagens['botao_2'] ,borderwidth=0,highlightthickness=0,command=lambda: self.destroy(),relief="flat",background="white") # Botão 2 (Cancelar?) fecha o popup
        self.button_2.place(x=384.0,y=458.0,width=142.0,height=40.0)
        
        self.imagens['botao_3']  = PhotoImage(file=self._relative_to_assets("button_3.png"))
        self.button_3 = Button(self,image=self.imagens['botao_3'] ,borderwidth=0,highlightthickness=0,command=lambda: self.destroy(),relief="flat",background="white") # Botão X (fechar)
        self.button_3.place(x=690.0,y=17.0,width=54.8,height=54.8)
        
        # Entradas (Campos de texto)
        # CORREÇÃO: Trocado Text por Entry para campos de uma linha
        
        # Entry 1 (Nome)
        self.imagens['entrada_1']  = PhotoImage(file=self._relative_to_assets("entry_1.png"))
        self.canvas.create_image(383.5,121.0,image=self.imagens['entrada_1'])
        self.entry_nome = Entry(self, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0, font=("Inter", 16))
        self.entry_nome.place(x=105.0,y=100.0,width=557.0,height=40.0)
        
        # Entry 2 (Email)
        self.imagens['entrada_2'] = PhotoImage(file=self._relative_to_assets("entry_2.png"))
        self.canvas.create_image(383.5,211.0,image=self.imagens['entrada_2'])
        self.entry_email = Entry(self, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0, font=("Inter", 16))
        self.entry_email.place(x=105.0,y=190.0,width=557.0,height=40.0)
        
        # Entry 4 (Login)
        self.imagens['entrada_4'] = PhotoImage(file=self._relative_to_assets("entry_4.png"))
        self.canvas.create_image(198.5,305.0,image=self.imagens['entrada_4'])
        self.entry_login = Entry(self, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0, font=("Inter", 16))
        self.entry_login.place(x=105.0,y=284.0,width=187.0,height=40.0)
        
        # Entry 5 (Tipo) - Idealmente uma Combobox
        self.imagens['entrada_5'] = PhotoImage(file=self._relative_to_assets("entry_5.png"))
        self.canvas.create_image(504.0,305.0,image=self.imagens['entrada_5'])
        self.entry_tipo = Entry(self, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0, font=("Inter", 16))
        self.entry_tipo.place(x=346.0,y=284.0,width=316.0,height=40.0)
        
        # Entry 3 (Senha)
        self.imagens['entrada_3'] = PhotoImage(file=self._relative_to_assets("entry_3.png"))
        self.canvas.create_image(384.0,400.0,image=self.imagens['entrada_3'])
        self.entry_senha = Entry(self, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0, show="*", font=("Inter", 16))
        self.entry_senha.place(x=106.0,y=379.0,width=556.0,height=40.0)

        # Configuração Modal
        # CORREÇÃO: Removido 'self.' duplicado
        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def _relative_to_assets(self,path: str) -> Path:
        # CORREÇÃO: Typo no nome da variável
        return self.ASSETS_PATH / Path(path)
    
    def cadastrar_bolsista(self):
        conexao = conectar()
        if not conexao:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")
            return
            
        cursor = conexao.cursor()
        
        # CORREÇÃO: Pega os dados dos widgets Entry
        self.nome_usuario = self.entry_nome.get()
        self.email_usuario = self.entry_email.get()
        self.login_usuario = self.entry_login.get() # 'login' é o 'nomeinst' no DB
        self.tipo_usuario = self.entry_tipo.get()
        self.senha_usuario = self.entry_senha.get()
        
        if not self.nome_usuario or not self.email_usuario or not self.login_usuario or not self.tipo_usuario or not self.senha_usuario:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            conexao.close()
            return
        
        try:
            # CORREÇÃO: Variáveis corretas e typo 'email_suario'
            cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo, nomeinst) VALUES (%s, %s, %s, %s, %s)", 
                           (self.nome_usuario, self.email_usuario, self.senha_usuario, self.tipo_usuario, self.login_usuario))
            conexao.commit()
            messagebox.showinfo("Feito!", "Usuário Cadastrado!")
            
            # Limpa os campos e fecha
            self.entry_nome.delete(0, 'end')
            self.entry_email.delete(0, 'end')
            self.entry_login.delete(0, 'end')
            self.entry_tipo.delete(0, 'end')
            self.entry_senha.delete(0, 'end')
            self.destroy()
            
        except Exception as e:
             messagebox.showerror("Erro de Banco", f"Erro ao cadastrar usuário: {e}")
        finally:
            conexao.close()

# --- Bloco __main__ (Removido) ---
# Este arquivo deve ser importado pelo seu main.py,
# e não executado diretamente.