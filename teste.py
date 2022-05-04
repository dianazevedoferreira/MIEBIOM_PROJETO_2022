# import do tkinter
from tkinter import *
# import do módulo ttk (para conseguirmos usar o scrollbar e a listbox)
from tkinter.ttk import *
# import do conector ao mysql (para conseguirmos ligar à BD e executar queries)
import mysql.connector

# para abrir a janela
window = Tk()
window.title("Adicionar Pedido") # mudar o nome da janela
window.geometry('450x400') # configurar o tamanho da janela

# CONEXÃO À BASE DE DADOS MYSQL (no host, user, password e database devem usar os valores definidos para a vossa BD local)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mydb"
)

# EPISODIO
# criar a label do episódio
lbl_ep = Label(window, text="Nº Episódio")
lbl_ep.grid(column=0, row=0)
# criar a entry para o utilizador inserir o nº de episódio
txt_ep = Entry(window,width=15)
txt_ep.grid(column=1, row=0)

# MODULO
# criar a label do módulo
lbl_mod = Label(window, text="Módulo")
lbl_mod.grid(column=0, row=1)
# criar a combobox do módulo e preenchê-la com a lista de valores possíveis "URG", "CON", "BLO" e "INT"
combo_mod = Combobox(window)
lista_mod = ('URG','CON','BLO','INT')
combo_mod['values'] = lista_mod
combo_mod.grid(column=1, row=1)

# PACIENTES
# ir buscar a lista de pacientes
mycursor = mydb.cursor()
mycursor.execute("SELECT id_paciente FROM pacientes")
pacientes = mycursor.fetchall()
# criar a label dos pacientes
lbl_pac = Label(window, text="Paciente")
lbl_pac.grid(column=0, row=2)
# criar a combobox dos pacientes e preenchê-la com a lista que vem da BD
combo_pac = Combobox(window)
combo_pac['values'] = pacientes
combo_pac.grid(column=1, row=2)

# MÉDICOS
# ir buscar a lista de médicos
mycursor2 = mydb.cursor()
mycursor2.execute("SELECT num_mec FROM medicos")
medicos = mycursor2.fetchall()
# criar a label dos médicos
lbl_med = Label(window, text="Médico")
lbl_med.grid(column=0, row=3)
# criar a combobox dos médicos e preenchê-la com a lista que vem da BD
combo_med = Combobox(window)
combo_med['values'] = medicos
combo_med.grid(column=1, row=3)

# MCDS
# ir buscar a lista de mcds
mycursor3 = mydb.cursor()
mycursor3.execute("SELECT cod FROM mcds")
mcds = mycursor3.fetchall()
# criar a label dos mcds
lbl_mcds = Label(window, text="MCDS")
lbl_mcds.grid(column=0, row=4)
# criar a listbox dos mcds - usamos uma listbox em vez de combobox porque queremos seleccionar mais que do que 1 MCD
# como temos uma lista longa é necessário criar uma scrollbar para poder controlar a lista verticalmente
# este scrollbar tem que ficar à direita da listbox (column=2) funcionando de Norte para Sul (sticky=NS)
scrollbar = Scrollbar(window, orient=VERTICAL)
scrollbar.grid(column=2, row=4, sticky=NS)
# a Listbox recebe como parâmetro o selectmode EXTENDED para podermos seleccionar mais que um exame pressionando a tecla ctrl
# temos que atribuir a propriedade yscrollcommand da listbox à scrollbar para ajustar o tamanho do scroll consoante o tamanho da lista
lb_mcds = Listbox(window, selectmode=EXTENDED, yscrollcommand=scrollbar.set)
# uma listbox tem que ser criada com um índice e o respetivo elemento
# por esse motivo não podemos atribuir a lista de mcds que vem da BD diretamente como fazemos na combobox
# vamos então buscar o tamanho da lista de mcds - len(mcds) - e percorrer num ciclo for de 0 até esse tamanho-1 - função range
for i in range(len(mcds)):
    # inserir cada elemento da lista de mcds na listbox e o respetivo índice
    lb_mcds.insert(i, mcds[i])
lb_mcds.grid(column=1, row=4)
# fazer a correspondência/associação da scrollbar à listbox
scrollbar.config(command=lb_mcds.yview)

# BOTÃO
# criar uma label com text a vazio para posteriormente inserir a mensagem de sucesso
lbl3 = Label(window, text="")
lbl3.grid(column=0, row=6)
# definir a função para associar ao botão de submissão
def clicked():
    # ir buscar os valores que estão atualmente seleccionados na listbox através da função get() e curselection()
    # a função curselection() dá-nos um tuplo com os índices (idx) dos mcds que estão seleccionados p.e (1,6,8)
    # para ir buscar o valor correspondente a cada um destes índices, usamos um ciclo for e a função get() com o respetivo índice
    values = [lb_mcds.get(idx)[0] for idx in lb_mcds.curselection()]
    # criar um ciclo for para fazer o insert na tabela de pedidos de cada um dos mcds seleccionados pelo utilizador
    for v in values:
        mycursor4 = mydb.cursor()
        # omitimos do INSERT a coluna dta_integracao (corresponde à data em que o sistema 2 manda msg para o sistema 1 a confirmar que recebeu a mensagem) porque inicialmente esta é null
        # usamos a função NOW() do MySQL para obter a data e hora atual e inserimos esse valor na coluna dta_pedido
        # para as restantes colunas, usamos o %s para mais tarde fazer o binding com o valor que queremos associar a cada coluna
        sql2 = "INSERT INTO pedidos(dta_pedido, modulo, num_episodio, id_paciente, num_mec, cod_mcd) VALUES(NOW(), %s, %s, %s, %s, %s)"
        # criamos um tuplo com os valores que pretendemos inserir na BD para cada %s
        # o número de elementos do tuplo tem que ser igual ao número de %s que colocamos na nossa query
        # usamos a função get() para extrair o valor preenchido/seleccionado em cada widget da janela
        # para a coluna dos mcds vamos buscar o elemento atual da lista que estamos a percorrer no ciclo for - v
        val = (combo_mod.get(), txt_ep.get(), combo_pac.get(), combo_med.get(), v)
        mycursor4.execute(sql2, val)
        # não esquecer de usar o commit para perpetuar as alterações feitas à BD
        mydb.commit()
    # criar a msg de sucesso e atribuí-la à label que criamos para esse efeito
    res = "MCDs inseridos com sucesso"
    lbl3.configure(text = res)
# criar o botão de submissão e associar à função definida anteriormente
btn = Button(window, text="Submeter", command=clicked)
btn.grid(column=0, row=5)

# para manter a janela aberta ao longo do tempo até esta ser fechada
window.mainloop()
