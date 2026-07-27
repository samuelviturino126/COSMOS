import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import *
from conectar import conectar
from pathlib import Path
from tkinter import messagebox
import psycopg2
from tkcalendar import DateEntry
from datetime import datetime, date
import sys

# --- CLASSE POPUP (COM MELHORIA) ---
class PopupNovoRegistro(Toplevel):
    def __init__(self, master, id_usuario, nome_usuario):
        # ... (código do __init__ igual ao seu, sem alterações) ...
        super().__init__(master) 
        self.title("Novo Registro de Atividade")
        self.geometry("442x392")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)
        self.id_usuario = id_usuario
        self.nome_usuario = nome_usuario
        self.dadosatv = []
        self.setores = ["Processamento Técnico", "Reprografia", "Atendimento", "Acervo e Midias Digitais", "Selecione"]
        self.imagens = {} 
        self.data_hoje = date.today()
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH / "telas" / "tela_registros_nova" / "imagens"
        self.canvas = Canvas(self, bg="#FFFFFF", height=392, width=442, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack() 
        self.canvas.create_text(35.0, 18.0, anchor="nw", text="Novo registro de atividade", fill="#2C3638", font=("Ubuntu Bold", 24 * -1))
        self.canvas.create_text(35.0, 111.0, anchor="nw", text="Atividade desempenhada", fill="#2C3638", font=("Inter", 14 * -1))
        self.canvas.create_text(35.0, 215.0, anchor="nw", text="Data", fill="#2C3638", font=("Inter", 14 * -1))
        self.canvas.create_text(167.0, 215.0, anchor="nw", text="Quantidade", fill="#2C3638", font=("Inter", 14 * -1))
        self.canvas.create_text(35.0, 135.0, anchor="nw", text="Atividade", fill="#2C3638", font=("Inter", 14 * -1))
        self.canvas.create_text(35.0, 65.0, anchor="nw", text="Setor", fill="#2C3638", font=("Inter", 14 * -1))
        self.combo_setor = ttk.Combobox(self, values=self.setores, state="readonly")
        self.indice_selecione = self.setores.index('Selecione')
        self.combo_setor.current(self.indice_selecione)
        self.combo_setor.place(x=35.0, y=85.0, width=360, height=40.0)
        self.combo_setor.bind("<<ComboboxSelected>>", self.carregar_atividades)
        self.combo_atividade = ttk.Combobox(self, state="readonly")
        self.combo_atividade.place(x=35.0, y=155.0, width=360, height=40.0)
        self.entry_quantidade = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_quantidade.place(x=175.0, y=240.0, width=102.0, height=25.0)
        self.entry_data = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_data.place(x = 49.0, y = 245.0, width=102.0, height=25.0)
        self.data_formatada = self.data_hoje.strftime("%d/%m/%Y")
        self.entry_data.insert(0, self.data_formatada)
        self.entry_image_2 = tk.PhotoImage(file=self._relative_to_assets("entry_2.png"))
        self.canvas.create_image(226.0, 257.0, image=self.entry_image_2)
        self.entry_image_3 = tk.PhotoImage(file=self._relative_to_assets("entry_3.png"))
        self.canvas.create_image(94.0, 257.0, image=self.entry_image_3)
        self.imagens['btn_salvar'] = PhotoImage(file=self._relative_to_assets("button_2.png"))
        botao_salvar = Button(self, image=self.imagens['btn_salvar'], borderwidth=0, highlightthickness=0, command=self.salvar_registro, relief="flat")
        botao_salvar.place(x=233.0, y=319.0, width=154.0, height=42.0)
        self.imagens['btn_cancelar'] = PhotoImage(file=self._relative_to_assets("button_1.png"))
        botao_cancelar = Button(self, image=self.imagens['btn_cancelar'], borderwidth=0, highlightthickness=0, command=self.destroy, relief="flat")
        botao_cancelar.place(x=35.0, y=321.5, width=141.0, height=37.0)
        self.transient(master)
        self.grab_set()
        self.wait_window(self)

    def _relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def salvar_registro(self):
        atividade = self.combo_atividade.get().strip()
        datain = self.entry_data.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        formatos_aceitos = ["%d/%m/%Y", "%d-%m-%Y"]
        data = None
        for formato in formatos_aceitos:
            try:
                data = datetime.strptime(datain, formato).date()
                break 
            except ValueError:
                continue
        if data is None:
            messagebox.showerror("Erro de Data", "Formato inválido. Use DD/MM/AAAA ou DD-MM-AAAA.")
            return
        if data > date.today():
            messagebox.showerror("Erro de Data", "Não é permitido registrar uma atividade com data futura.")
            return
        
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute("SELECT id FROM atividades_padrao WHERE nome = %s;", (atividade,)) 
            resultado_id = cursor.fetchone()
            
            if not resultado_id:
                messagebox.showerror("Erro", "Atividade não encontrada.")
                return

            id_atividade = resultado_id[0]
            cursor.execute("SELECT setor FROM atividades_padrao WHERE id = %s;", (id_atividade, )) 
            resultado_setor = cursor.fetchone()
            
            setor_atividade = resultado_setor[0]
            cursor.execute("INSERT INTO atividades_realizadas (usuario_id, atividade_id, data, inteiro, setor) VALUES (%s, %s, %s, %s, %s)", (self.id_usuario, id_atividade, data, quantidade, setor_atividade))
            conexao.commit()
            messagebox.showinfo("Feito!", "Atividade cadastrada com sucesso.")
            conexao.close()
            self.destroy() 
            
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao salvar registro. Erro: {e}")

    def carregar_atividades(self, event):
        self.setor = self.combo_setor.get().strip()
        self.combo_atividade.set('')
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM atividades_padrao WHERE setor = %s ORDER BY nome ASC;", (self.setor,))
            self.dadosatv = [linha[0] for linha in cursor.fetchall()]
            conexao.close()
            self.combo_atividade['values'] = self.dadosatv
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível carregar as atividades. Erro: {e}")
            self.combo_atividade['values'] = []
            
# --- CLASSE TELA BOLSISTA (COM CORREÇÕES) ---
class TelaBolsista(tk.Frame):
    def __init__(self,master,controlador):
        super().__init__(master)
        self.controlador = controlador
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH / "telas" / "tela_principal_nova" / "imagens" 
        
        #dicionário para imagens estáticas e dinâmicas
        self.imagens = {}
        self.imagens_dinamicas = {} 

        self.canvastelabolsista = Canvas(self,bg = "#F8F8F8",height = 1080,width = 1920,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvastelabolsista.place(x = 0, y = 0)

        #imagens de fundo (Estáticas, não vão mudar)
        self.imagens['ficambotoes'] = PhotoImage(file=self.relative_to_assets("frame_ficambotoes.png"))
        self.imagens['ficamla']= PhotoImage(file=self.relative_to_assets("ficamla.png"))
        self.imagens['barra_atividades']= PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.imagens['retangulao'] = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.imagens['retangulao2'] = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.imagens['calendario'] = PhotoImage(file=self.relative_to_assets("calendario.png"))

        #Posição das imagens estáticas
        self.canvastelabolsista.create_image(961.0,40.0,image=self.imagens['ficambotoes'])
        self.canvastelabolsista.create_image(961.0,40.0,image=self.imagens['ficamla'])
        self.canvastelabolsista.create_image(960.0,601.0,image=self.imagens['barra_atividades'])
        self.canvastelabolsista.create_image(1162.0,333.0,image=self.imagens['retangulao'])
        self.canvastelabolsista.create_image(755.0,331.0,image=self.imagens['retangulao2'])

        #botões estáticos (não mudam)
        self.imagens['novo_registro'] = PhotoImage(file=self.relative_to_assets("novo_registro.png"))
        self.botao_novo_registro = Button(self, image=self.imagens['novo_registro'],borderwidth=0,highlightthickness=0,command=self.abrir_tela_popup,relief="flat")
        self.botao_novo_registro.place(x=1136.0,y=18.0,width=210.0,height=42.0)
        
        self.imagens['botao_registro'] = PhotoImage(file=self.relative_to_assets("botao_registros.png"))
        self.botao_registros = Button(self, image=self.imagens['botao_registro'],borderwidth=0,highlightthickness=0,command=self.abrir_tela_registros,relief="flat")
        self.botao_registros.place(x=1387.0,y=30.0,width=73.0,height=19.0)
        
        self.imagens['botao_sair'] = PhotoImage(file=self.relative_to_assets("sair.png"))
        self.botao_sair = Button(self, image=self.imagens['botao_sair'],borderwidth=0,highlightthickness=0,command=lambda: (self.controlador.mostrar_tela("TelaLogin")),relief="flat")
        self.botao_sair.place(x=1486.0,y=23.5,width=34.0,height=34.0)

    def carregar_dados_e_construir_ui(self, id, nome):

        #apaga tudo que tiver a tag "dinamico"
        #isso vai permitir a gente atualizar as telas e evitar problemas
        self.canvastelabolsista.delete("dinamico")
        self.imagens_dinamicas.clear() #limpa o cache

        #atualizamos os dados
        self.id = id
        self.nome = nome
        self.nomes, self.setores, self.datas = [], [], []
        self.hoje = date.today()
        self.feitas_hoje = self.total_de_atividades_por_dia(self.id, self.hoje) 
        self.feitas_mes = self.total_de_atividades_por_mes(self.id, self.hoje.year, self.hoje.month)
        self.ultimas_atividades_registradas()


        
        # Os itens precisam da tag dinâmico, poderia ser outra
        self.canvastelabolsista.create_text(375.0,497.0,anchor="nw",text="Últimas atividades registradas",fill="#000000",font=("Ubuntu Bold", 40 * -1), tags="dinamico")
        self.canvastelabolsista.create_text(376.0,123.0,anchor="nw",text=f"Olá, {self.nome}!",fill="#2C3638",font=("Ubuntu Bold", 24 * -1), tags="dinamico")
        
        # Contador "Hoje"
        self.canvastelabolsista.create_text(755.0,315.0,anchor="n",text=f"{self.feitas_hoje}",fill="#2C3638",font=("Ubuntu Bold", 40 * -1), tags="dinamico") 
        if self.feitas_hoje == 0:
            self.canvastelabolsista.create_text(755.0,400.0,anchor="n",text="registros hoje",fill="#2C3638",font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            self.canvastelabolsista.create_text(755.0,371.0,anchor="n",text="Você ainda não fez ",fill="#2C3638",font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            
        #Armazenar em 'imagens_dinamicas' ---
            self.imagens_dinamicas['hoje'] = PhotoImage(file=self.relative_to_assets("sem_registros.png"))
            self.canvastelabolsista.create_image(755.0,273.0,image=self.imagens_dinamicas['hoje'], tags="dinamico")
        else:
            self.canvastelabolsista.create_text(760.0,400.0,anchor="n",text="Hoje",fill="#2C3638",font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            self.canvastelabolsista.create_text(760.0,371.0,anchor="n",text="Atividades Registradas ",fill="#2C3638",font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            self.imagens_dinamicas['hoje'] = PhotoImage(file=self.relative_to_assets("com_registros.png"))
            self.canvastelabolsista.create_image(755.0,273.0,image=self.imagens_dinamicas['hoje'], tags="dinamico")

        # Contador "Mês"
        self.canvastelabolsista.create_text(1162.0,315.0,anchor="n",text=f"{self.feitas_mes}",fill="#2C3638",font=("Ubuntu Bold", 40 * -1), tags="dinamico") 
        if self.feitas_mes == 0:
            self.canvastelabolsista.create_text(1060.0,400.0,anchor="nw",text="Registros nesse mês",fill="#2C3638",font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            self.canvastelabolsista.create_text(1060.0,371.0,anchor="nw",text="Você ainda não fez ",fill="#2C3638",font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            self.imagens_dinamicas['mes'] = PhotoImage(file=self.relative_to_assets("sem_registros.png"))
            self.canvastelabolsista.create_image(1162.0,273.0,image=self.imagens_dinamicas['mes'], tags="dinamico")
        else:
            self.canvastelabolsista.create_text(1168.0, 371.0, anchor="n",text="Atividades Registradas", fill="#2C3638", font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            self.canvastelabolsista.create_text(1168.0, 400.0, anchor="n",text="esse mês", fill="#2C3638", font=("Ubuntu Medium", 24 * -1), tags="dinamico")
            self.imagens_dinamicas['mes'] = PhotoImage(file=self.relative_to_assets("com_registros.png"))
            self.canvastelabolsista.create_image(1162.0,273.0,image=self.imagens_dinamicas['mes'], tags="dinamico")

        # Lista de Últimas Atividades
        while len(self.nomes) < 3:
            self.nomes.append("Nenhuma atividade")
            self.setores.append("Sem setor")
            self.datas.append(None)
        
        nomeatividade1, nomeatividade2, nomeatividade3 = self.nomes[0], self.nomes[1], self.nomes[2]
        setoratividade1, setoratividade2, setoratividade3 = self.setores[0], self.setores[1], self.setores[2]
        
        # Atividade 1
        self.imagens_dinamicas['atv1'] = PhotoImage(file=self.relative_to_assets(f"{setoratividade1}.png")) 
        self.canvastelabolsista.create_image(588.0,660.0,image=self.imagens_dinamicas['atv1'], tags="dinamico")
        self.canvastelabolsista.create_text(614.0,650.0,anchor="nw",text=f"{nomeatividade1}",fill="#2C3638",font=("Inter", 16 * -1), tags="dinamico")
        self.canvastelabolsista.create_image(1062.0,660.0,image=self.imagens['calendario'], tags="dinamico") # Imagem estática, mas Posição dinâmica
        data1_formatada = self.datas[0].strftime("%d/%m/%Y") if self.datas[0] else "Sem data"
        self.canvastelabolsista.create_text(1086.0,650.0,anchor="nw",text=data1_formatada,fill="#ABABAB",font=("Inter", 16 * -1), tags="dinamico")
        
        # Atividade 2
        self.imagens_dinamicas['atv2'] = PhotoImage(file = self.relative_to_assets(f"{setoratividade2}.png"))
        self.canvastelabolsista.create_image(588.0,720.0,image = self.imagens_dinamicas['atv2'], tags="dinamico")
        data2_formatada = self.datas[1].strftime("%d/%m/%Y") if len(self.datas) > 1 and self.datas[1] else "Sem data"
        self.canvastelabolsista.create_text(1086.0,710.0,anchor="nw",text=data2_formatada,fill="#ABABAB",font=("Inter", 16 * -1), tags="dinamico")
        self.canvastelabolsista.create_text(614.0,710.0,anchor="nw",text=f"{nomeatividade2}",fill="#2C3638",font=("Inter", 16 * -1), tags="dinamico")
        self.canvastelabolsista.create_image(1062.0,720.0,image=self.imagens['calendario'], tags="dinamico")
        
        # Atividade 3
        self.imagens_dinamicas['atv3'] = PhotoImage(file = self.relative_to_assets(f"{setoratividade3}.png"))
        self.canvastelabolsista.create_image(588.0,780.0,image = self.imagens_dinamicas['atv3'], tags="dinamico")
        self.canvastelabolsista.create_text(614.0,770.0,anchor="nw",text=f"{nomeatividade3}",fill="#2C3638",font=("Inter", 16 * -1), tags="dinamico")
        data3_formatada = self.datas[2].strftime("%d/%m/%Y") if len(self.datas) > 2 and self.datas[2] else "Sem data"
        self.canvastelabolsista.create_text(1086.0,770.0,anchor="nw",text=data3_formatada,fill="#ABABAB",font=("Inter", 16 * -1), tags="dinamico")
        self.canvastelabolsista.create_image(1062.0,780.0,image=self.imagens['calendario'], tags="dinamico")

    def abrir_tela_popup(self):
        # Abre o popup e ESPERA ele fechar (pois é modal)
        PopupNovoRegistro(self, self.id, self.nome)
        #Quando o Pop-up fechar atualiza a tela
        self.carregar_dados_e_construir_ui(self.id, self.nome)
        
    def abrir_tela_registros(self):
        self.controlador.mostrar_tela("TelaRegistros", self.id, self.nome)
        
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    # --- Funções do banco de dados 
    def total_de_atividades_por_dia(self, usuario_id, inicio):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(id) FROM atividades_realizadas WHERE usuario_id = %s AND data = %s", (usuario_id, inicio))
        resultado = cursor.fetchone()[0]
        total = int(resultado) if resultado is not None else 0
        conexao.close()
        return total
    def total_de_atividades_por_mes(self, usuario_id, ano, mes):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(id) FROM atividades_realizadas WHERE usuario_id = %s AND EXTRACT(YEAR FROM data) = %s AND EXTRACT(MONTH FROM data) = %s", (usuario_id, ano, mes))
        resultado = cursor.fetchone()[0]
        total = int(resultado) if resultado is not None else 0
        conexao.close()
        return total
    def ultimas_atividades_registradas(self):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT ar.atividade_id, ar.data, ap.nome, ap.setor FROM atividades_realizadas ar JOIN atividades_padrao ap ON ar.atividade_id = ap.id WHERE ar.usuario_id = %s ORDER BY ar.data DESC, ar.id DESC LIMIT 3", (self.id,))
        self.resultados = cursor.fetchall()
        conexao.close()
        self.ultimos_3ids = [r[0] for r in self.resultados]
        self.datas = [r[1] for r in self.resultados]
        self.nomes = [r[2] for r in self.resultados]
        self.setores = [r[3] for r in self.resultados]


class TelaRegistros(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador 
        self.imagens = {}
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH / "telas" / "tela_todosregistros" / "imagens"
        
        # --- Widgets Estáticos (criados 1x no __init__) ---
        self.canvas_todosregistros = Canvas(self, bg="#F8F8F8", height=1080, width=1920, bd=0, highlightthickness=0, relief="ridge")
        self.canvas_todosregistros.place(x=0, y=0)
        self.imagens['image_1'] = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas_todosregistros.create_image(961.0, 43.0, image=self.imagens['image_1'])
        self.canvas_todosregistros.create_text(376.0, 152.0, anchor="nw", text="Registros de atividades", fill="#000000", font=("Ubuntu Bold", 40 * -1))
        
        # Botão topo (era button_7)
        self.imagens['novoregistro_topo'] = PhotoImage(file=self.relative_to_assets("registrar.png")) 
        self.button_topo = Button(self, image=self.imagens['novoregistro_topo'],borderwidth=0,highlightthickness=0,command=self.abrir_tela_popup,relief="flat")
        self.button_topo.place(x=1255.0, y=22.0, width=210.0, height=42.0)

        # Botão Voltar (era button_8)
        self.imagens['botao_voltar'] = PhotoImage(file=self.relative_to_assets("button_8.png"))
        self.button_voltar = Button(self, image=self.imagens['botao_voltar'], borderwidth=0, highlightthickness=0, command=self.voltar_para_bolsista, relief="flat") 
        self.button_voltar.place(x=1486.0, y=22.0, width=34.0, height=34.0)

        # Imagem usuário
        self.imagens['imagemuser'] = PhotoImage(file=self.relative_to_assets("image_9.png"))
        self.canvas_todosregistros.create_image(420.0, 42.5, image=self.imagens['imagemuser'])

        # --- Área de Filtros ---
        self.imagens['butaofiltros'] = PhotoImage(file=self.relative_to_assets("filtros.png")) 
        self.button_filtros = Button(self, image=self.imagens['butaofiltros'], borderwidth=0, highlightthickness=0, command=self.exibir_atividades, relief="flat")
        self.button_filtros.place(x=376.0, y=248.0, width=208.0, height=42.0)

        self.canvas_todosregistros.create_text(625,235, anchor = "n", text="Mês", fill = "#000000", font = ("Ubuntu Bold", 16 * -1))
        self.imagens['image_12'] = PhotoImage(file=self.relative_to_assets("entrada_usar.png"))
        self.canvas_todosregistros.create_image(700,260,image=self.imagens['image_12'])
        self.entry_mes = tk.Entry(self, font=("Ubuntu", 12), width=5,bd=0,highlightthickness=0 )
        self.entry_mes.place(x=620, y=255, height=20)
        
        self.canvas_todosregistros.create_text(725,235, anchor = "n", text="Ano", fill = "#000000", font = ("Ubuntu Bold", 16 * -1))
        self.imagens['image_15'] = PhotoImage(file=self.relative_to_assets("entrada_usar.png"))
        self.canvas_todosregistros.create_image(800,260,image=self.imagens['image_15'])
        self.entry_ano = tk.Entry(self, font=("Ubuntu", 12), width=7,bd=0,highlightthickness=0)
        self.entry_ano.place(x=717, y=257, height=20)

        # Botão Novo Registro (Meio) (era button_1)
        self.imagens['novoregistro_meio'] = PhotoImage(file=self.relative_to_assets("registrar.png")) 
        self.button_meio = Button(self, image=self.imagens['novoregistro_meio'],borderwidth=0,highlightthickness=0,command=self.abrir_tela_popup,relief="flat")
        self.button_meio.place(x=1336.0, y=248.0, width=210.0, height=42.0)

        # --- Cabeçalho da Lista ---
        self.imagens['image_2'] = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas_todosregistros.create_image(960.0, 332.0, image=self.imagens['image_2'])
        self.canvas_todosregistros.create_text(396.0, 321.0, anchor="nw", text="Atividade", fill="#FFFFFF", font=("Ubuntu Medium", 20 * -1))
        self.canvas_todosregistros.create_text(620.0, 321.0, anchor="nw", text="Quantidade", fill="#FFFFFF", font=("Ubuntu Medium", 20 * -1))
        self.canvas_todosregistros.create_text(856.0, 321.0, anchor="nw", text="Data", fill="#FFFFFF", font=("Ubuntu Medium", 20 * -1))
        self.canvas_todosregistros.create_text(1174.0, 321.0, anchor="nw", text="Opções", fill="#FFFFFF", font=("Ubuntu Medium", 20 * -1))
        
        # --- Área de Rolagem (Container) ---
        self.canvas_rolavel = tk.Canvas(self, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.canvas_rolavel.place(x=376, y=355, width=1150, height=600)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas_rolavel.yview)
        self.scrollbar.place(x=1526, y=355, height=600)
        self.canvas_rolavel.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame de Conteúdo (onde os cards são realmente colocados)
        self.frame_conteudo = tk.Frame(self.canvas_rolavel, bg="#FFFFFF")
        self.canvas_rolavel.create_window((0, 0), window=self.frame_conteudo, anchor="nw", width=1150)
        self.frame_conteudo.bind("<Configure>", lambda e: self.canvas_rolavel.configure(scrollregion=self.canvas_rolavel.bbox("all")))

        # --- Carregar Imagens Estáticas para a Lista ---
        self.imagens['imagem_processamento'] = PhotoImage(file=self.relative_to_assets("processamento.png"))
        self.imagens['imagem_calendario'] = PhotoImage(file=self.relative_to_assets("calendario.png"))
        self.imagens['imagem_apagar'] = PhotoImage(file=self.relative_to_assets("apagar.png"))
    
    def carregar_dados_e_construir_ui(self, id, nome):
        # --- PASSO 1: ATUALIZAR DADOS ---
        self.nome = nome
        self.id = id
        self.resultados = []
        self.hoje = date.today()
        
        # --- PASSO 2: ATUALIZAR WIDGETS ESTÁTICOS ---
        self.entry_mes.delete(0, 'end')
        self.entry_mes.insert(0, str(datetime.now().month))
        self.entry_ano.delete(0, 'end')
        self.entry_ano.insert(0, str(datetime.now().year))
        
        # (O comando do botão voltar é atualizado na sua própria função agora)

        # --- PASSO 3: CARREGAR CONTEÚDO DINÂMICO ---
        self.exibir_atividades()

    def voltar_para_bolsista(self):
        # Esta função garante que os dados (id, nome) estejam corretos
        self.controlador.mostrar_tela("TelaBolsista", self.id, self.nome)

    def abrir_tela_popup(self):
        # Abre o popup e ESPERA ele fechar
        PopupNovoRegistro(self, self.id, self.nome)
        
        # --- MELHORIA 1 (CORRIGIDA) ---
        # Após o popup fechar, recarrega a lista de atividades
        self.exibir_atividades() 

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def exibir_atividades(self):
        # --- PASSO DE LIMPEZA (DINÂMICO) ---
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        try:
            mes = int(self.entry_mes.get())
            ano = int(self.entry_ano.get())
        except (ValueError, IndexError):
            # Se os campos estiverem vazios ao carregar, usa o mês/ano atuais
            mes = datetime.now().month
            ano = datetime.now().year
            self.entry_mes.delete(0, 'end')
            self.entry_mes.insert(0, str(mes))
            self.entry_ano.delete(0, 'end')
            self.entry_ano.insert(0, str(ano))

        self.ultimas_atividades_registradas(self.id, ano, mes)

        if not self.resultados:
            tk.Label(self.frame_conteudo, text="Nenhuma atividade encontrada para o período.", font=("Ubuntu", 14), bg="#FFFFFF").pack(pady=20)
            return
        
        # --- (Re)Construção dos Itens da Lista (sem alteração) ---
        LARGURA_QUANTIDADE = 150
        LARGURA_DATA = 200
        LARGURA_OPCOES = 150

        for i, atividade in enumerate(self.resultados):
            atividade_id, data, nome, setor, quantidade = atividade
            
            row_bg_frame = tk.Frame(self.frame_conteudo, bg="#F0F0F0")
            row_bg_frame.pack(fill="x", pady=(2, 2))
            row_frame = tk.Frame(row_bg_frame, bg="#FFFFFF", height=60)
            row_frame.pack(fill="x", expand=True, padx=1, pady=1)

            setor_label = tk.Label(row_frame, image=self.imagens['imagem_processamento'], bg="#FFFFFF")
            setor_label.pack(side="left", padx=(10, 5), anchor="w")
            
            nome_label = tk.Label(row_frame, text=nome, font=("Inter", 16 * -1), bg="#FFFFFF", fg="#2C3638", anchor="w")
            nome_label.pack(side="left", padx=(5, 5), fill="x", expand=True)

            quantidade_frame = tk.Frame(row_frame, bg="#FFFFFF", width=LARGURA_QUANTIDADE)
            quantidade_frame.pack(side="left", fill="y", padx=(5, 5))
            quantidade_frame.pack_propagate(False) 
            quantidade_label = tk.Label(quantidade_frame, text=f"{quantidade:.0f}".replace('.',','), font=("Inter", 16 * -1), bg="#FFFFFF", fg="#2C3638", anchor="center")
            quantidade_label.pack(fill="both", expand=True)

            data_frame = tk.Frame(row_frame, bg="#FFFFFF", width=LARGURA_DATA)
            data_frame.pack(side="left", fill="y", padx=(5, 5))
            data_frame.pack_propagate(False)
            calendario_label = tk.Label(data_frame, image=self.imagens['imagem_calendario'], bg="#FFFFFF")
            calendario_label.pack(side="left", anchor="center")
            data_label = tk.Label(data_frame, text=data.strftime("%d/%m/%Y"), font=("Inter", 16 * -1), bg="#FFFFFF", fg="#ABABAB", anchor="center")
            data_label.pack(side="left", fill="x", expand=True)

            opcoes_frame = tk.Frame(row_frame, bg="#FFFFFF", width=LARGURA_OPCOES)
            opcoes_frame.pack(side="left", fill="y", padx=(5, 5))
            opcoes_frame.pack_propagate(False)
            botao_apagar = tk.Button(opcoes_frame, image=self.imagens['imagem_apagar'], borderwidth=0, highlightthickness=0, relief="flat", command=lambda a_id=atividade_id: self.confirmar_apagar(a_id))
            botao_apagar.pack(expand=True)

    # --- Funções de Banco (Sem alterações) ---
    def ultimas_atividades_registradas(self, usuario_id, ano, mes):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT ar.id, ar.data, ap.nome, ap.setor, ar.inteiro FROM atividades_realizadas ar JOIN atividades_padrao ap ON ar.atividade_id = ap.id WHERE ar.usuario_id = %s AND EXTRACT(YEAR FROM data) = %s AND EXTRACT(MONTH FROM data) = %s ORDER BY ar.data DESC, ar.id DESC", (usuario_id, ano, mes))
        self.resultados = cursor.fetchall()
        conexao.close()
    
    def confirmar_apagar(self, atividade_id):
        resposta = messagebox.askyesno("Confirmação", "Você tem certeza que deseja apagar esta atividade?")
        if resposta:
            self.apagar_atividade(atividade_id)

    def apagar_atividade(self, atividade_id):
        conexao = conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM atividades_realizadas WHERE id = %s", (atividade_id,))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Atividade apagada com sucesso!")
            self.exibir_atividades() 
        except psycopg2.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao apagar atividade: {e}")
        finally:
            conexao.close()

    def total_de_atividades_por_mes(self, usuario_id, ano, mes):
        # (Seu código original estava como COUNT(*), mas na TelaBolsista estava SUM(inteiro). 
        # Vou manter o COUNT(*) como estava nesta classe, mas revise se a lógica é essa mesma)
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM atividades_realizadas WHERE usuario_id = %s AND EXTRACT(YEAR FROM data) = %s AND EXTRACT(MONTH FROM data) = %s", (usuario_id, ano, mes))
        resultado = cursor.fetchone()[0]
        total = int(resultado) if resultado is not None else 0
        conexao.close()
        return total