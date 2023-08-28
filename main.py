from tkinter import *
import sqlite3
from tkinter import messagebox

def rightFrameBuilder():
    # Adicionando scrollbar ao aplicativo utilizando o widget canvas
    global canva

    canva = Canvas(rightFrame, bg='lavender')
    canva.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = Scrollbar(rightFrame, orient=VERTICAL, command=canva.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canva.configure(yscrollcommand=scrollbar.set)
    canva.bind('<Configure>', lambda e: canva.configure(scrollregion = canva.bbox('all')))

    global actualRightFrame

    actualRightFrame = Frame(canva, bg='lavender', width=300, height=100)

    canva.create_window((0,0), window=actualRightFrame, anchor='nw', width=1025)

    actualRightFrame.columnconfigure(0, weight=1)

    # Criando conexão com a database

    conn = sqlite3.connect('prontuarios.db')

    cursor = conn.cursor()

    cursor.execute('SELECT *, oid FROM prontuarios')
    records = cursor.fetchall()

    for index, record in enumerate(records):
        # Configurando cada row do actRightframe
        actualRightFrame.rowconfigure(index, weight=0)
        
        # Criando frame para comportar prévia de prontuário
        recordFrame = Frame(actualRightFrame, width=450, height=100)

        # Configurando recordFrame
        recordFrame.rowconfigure(0, weight=1)
        recordFrame.rowconfigure(1, weight=1)

        recordFrame.columnconfigure(0, weight=1)
        recordFrame.columnconfigure(1, weight=1)
        recordFrame.columnconfigure(2, weight=1)
        recordFrame.columnconfigure(3, weight=1)

        # Adicionando Frame na tela
        recordFrame.grid(row=index, sticky='new', padx=5, pady=5)

        # Criando as Labels para mostrar o prontuário
        nomePetLabel = Label(recordFrame, text=str(record[0]), width=20)
        nomeProprietarioLabel = Label(recordFrame, text=str(record[2]), width=20)
        especieLabel = Label(recordFrame, text=str(record[6]), width=20)
        racaLabel = Label(recordFrame, text=str(record[8]), width=20)
        sexoLabel = Label(recordFrame, text=str(record[7]), width=20)
        pesoLabel = Label(recordFrame, text=str(record[9]), width=20)

        # Colocando as labels dentro do recordFrame
        nomePetLabel.grid(row=0, column=0, sticky='nw')
        nomeProprietarioLabel.grid(row=1, column=0, sticky='sw')
        especieLabel.grid(row=0, column=1, sticky='n')
        racaLabel.grid(row=1, column=1, sticky='s')
        sexoLabel.grid(row=0, column=2, sticky='ne')
        pesoLabel.grid(row=1, column=2, sticky='se')

        # Criando e adicionando botão de acesso
        oid = record[11]

        accessButton = Button(recordFrame, text='Acessar', width=10, command=lambda oid=oid: accessRecord(oid))
        accessButton.grid(row=0, rowspan=2, column=3, sticky='nsew')

    conn.commit()

    conn.close()

def newRecord():
    def submitNewRecord():
        conn = sqlite3.connect('prontuarios.db')
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO prontuarios VALUES (:nomePet, :idadePet, :nomeProprietario, :celular, :endereco,
                       :cidade, :especie, :sexo, :raca, :peso, :observacoes)""",
                       {
                           'nomePet': nomePet.get(),
                           'idadePet': idadePet.get(),
                           'nomeProprietario': nomeProprietario.get(),
                           'celular': celular.get(),
                           'endereco': endereco.get(),
                           'cidade': cidade.get(),
                           'especie': especie.get(),
                           'sexo': sexo.get(),
                           'raca': raca.get(),
                           'peso': peso.get(),
                           'observacoes': observacoes.get('1.0', 'end-1c')
                       })
        
        conn.commit()

        cursor.execute('SELECT *, oid FROM prontuarios')
        record = cursor.fetchall()

        # Configurando cada row do actRightframe
        actualRightFrame.rowconfigure(len(record) - 1, weight=0)
        
        # Criando frame para comportar prévia de prontuário
        recordFrame = Frame(actualRightFrame, width=450, height=100)

        # Configurando recordFrame
        recordFrame.rowconfigure(0, weight=1)
        recordFrame.rowconfigure(1, weight=1)

        recordFrame.columnconfigure(0, weight=1)
        recordFrame.columnconfigure(1, weight=1)
        recordFrame.columnconfigure(2, weight=1)
        recordFrame.columnconfigure(3, weight=1)

        # Adicionando Frame na tela
        recordFrame.grid(row=len(record) - 1, sticky='new', padx=5, pady=5)

        # Criando as Labels para mostrar o prontuário
        nomePetLabel = Label(recordFrame, text=str(record[-1][0]), width=20)
        nomeProprietarioLabel = Label(recordFrame, text=str(record[-1][2]), width=20)
        especieLabel = Label(recordFrame, text=str(record[-1][6]), width=20)
        racaLabel = Label(recordFrame, text=str(record[-1][8]), width=20)
        sexoLabel = Label(recordFrame, text=str(record[-1][7]), width=20)
        pesoLabel = Label(recordFrame, text=str(record[-1][9]), width=20)

        # Colocando as labels dentro do recordFrame
        nomePetLabel.grid(row=0, column=0, sticky='nw')
        nomeProprietarioLabel.grid(row=1, column=0, sticky='sw')
        especieLabel.grid(row=0, column=1, sticky='n')
        racaLabel.grid(row=1, column=1, sticky='s')
        sexoLabel.grid(row=0, column=2, sticky='ne')
        pesoLabel.grid(row=1, column=2, sticky='se')

        # Criando e adicionando botão de acesso
        oid = record[-1][11]

        accessButton = Button(recordFrame, text='Acessar', width=10, command=lambda oid=oid: accessRecord(oid))
        accessButton.grid(row=0, rowspan=2, column=3, sticky='nsew')

        conn.commit()
        conn.close()

        addRecord.destroy()

    addRecord = Tk()
    addRecord.title('Adicionar prontuário')
    addRecord.iconbitmap('img_ico\\add_icon.ico')
    #addRecord.geometry('700x450')
    addRecord.resizable(False, False)

    # Configurando o espaço da janela
    addRecord.columnconfigure(0, weight=3)
    addRecord.columnconfigure(1, weight=7)

    for row in range(11):
        addRecord.rowconfigure(row, weight=1)

    # Criando as Entry Widgets para coletar as informações
    nomePet = Entry(addRecord, width=50)
    idadePet = Entry(addRecord, width=50)
    nomeProprietario = Entry(addRecord, width=50)
    celular = Entry(addRecord, width=50)
    endereco = Entry(addRecord, width=50)
    cidade = Entry(addRecord, width=50)
    especie = Entry(addRecord, width=50)
    sexo = Entry(addRecord, width=50)
    raca = Entry(addRecord, width=50)
    peso = Entry(addRecord, width=50)
    observacoes = Text(addRecord, width=50, height=10, font=('Segoe UI', '9'))

    # Criando as Labels para identificar cada Entry
    nomePetLabel = Label(addRecord, text='Nome do Pet:', anchor='w', justify='left', width=20)
    idadePetLabel = Label(addRecord, text='Idade do Pet:', anchor='w', justify='left', width=20)
    nomeProprietarioLabel = Label(addRecord, text='Nome do(a) Proprietário(a):', anchor='w', justify='left', width=20)
    celularLabel = Label(addRecord, text='Celular:', anchor='w', justify='left', width=20)
    enderecoLabel = Label(addRecord, text='Endereço:', anchor='w', justify='left', width=20)
    cidadeLabel = Label(addRecord, text='Cidade:', anchor='w', justify='left', width=20)
    especieLabel = Label(addRecord, text='Espécie:', anchor='w', justify='left', width=20)
    sexoLabel = Label(addRecord, text='Sexo:', anchor='w', justify='left', width=20)
    racaLabel = Label(addRecord, text='Raça:', anchor='w', justify='left', width=20)
    pesoLabel = Label(addRecord, text='Peso:', anchor='w', justify='left', width=20)
    observacoesLabel = Label(addRecord, text='Observações:', anchor='w', justify='left', width=20)

    # Colocando todos os widgets na tela usando for loops

    entrys = [nomePet, idadePet, nomeProprietario, celular, endereco, cidade, especie, sexo, raca, peso, observacoes]

    for row, entry in enumerate(entrys):
        entry.grid(row=row, column=1, sticky='ew', pady=5, padx=5)

    labels = [nomePetLabel, idadePetLabel, nomeProprietarioLabel, celularLabel, enderecoLabel, cidadeLabel,
              especieLabel, sexoLabel, racaLabel, pesoLabel, observacoesLabel]
    
    for row, label in enumerate(labels):
        label.grid(row=row, column=0, pady=5)

    # Criando o botão para salvar e enviar as informações

    submitButton = Button(addRecord, text='Salvar e enviar', command=submitNewRecord)
    submitButton.grid(row=12, columnspan=2, padx=5, pady=5)

def accessRecord(oid):
    # Criando as funções de funcionalidade: Deletar e Atualizar
    def updateRecord():

        # Criando a função de enviar informações a serem atualizadas
        def submitUpdatedRecord():

            # Estabelecendo conexão com o banco de dados
            conn = sqlite3.connect('prontuarios.db')
            cursor = conn.cursor()

            cursor.execute("""UPDATE prontuarios SET
                           nomePet = :nomePet,
                           idadePet = :idadePet,
                           nomeProprietario = :nomeProprietario,
                           celular = :celular,
                           endereco = :endereco,
                           cidade = :cidade,
                           especie = :especie,
                           sexo = :sexo,
                           raca = :raca,
                           peso = :peso,
                           observacoes = :observacoes
                           WHERE oid = :oid""",
                           {
                               'nomePet': nomePet.get(),
                               'idadePet': idadePet.get(),
                               'nomeProprietario': nomeProprietario.get(),
                               'celular': celular.get(),
                               'endereco': endereco.get(),
                               'cidade': cidade.get(),
                               'especie': especie.get(),
                               'sexo': sexo.get(),
                               'raca': raca.get(),
                               'peso': peso.get(),
                               'observacoes': observacoes.get("1.0",'end-1c'),
                               'oid': oid
                           }
                           )
            
            messagebox.showinfo('Informação', 'Atualização executada com sucesso!')
            updateWindow.destroy()
            
            # Destruindo e reconstruindo right frame

            global rightFrame

            rightFrame.destroy()

            rightFrame = Frame(root, bg='lavender', width=50, height=height)

            rightFrame.grid(row=0, column=1, sticky='nsew')

            rightFrame.columnconfigure(0, weight=1)

            conn.commit()
            conn.close()

            rightFrameBuilder()

        # Criando nova janela e configurando-a
        updateWindow = Tk()
        updateWindow.title('Atualizar prontuário')
        updateWindow.iconbitmap('img_ico\\update_icon.ico')
        updateWindow.resizable(False, False)
        updateWindow.focus_force()

        # Destruindo a janela anterior
        recordWindow.destroy()

        # Configurando o espaço da janela
        updateWindow.columnconfigure(0, weight=3)
        updateWindow.columnconfigure(1, weight=7)

        for row in range(11):
            updateWindow.rowconfigure(row, weight=1)

        # Criando as Entry Widgets para coletar as informações
        nomePet = Entry(updateWindow, width=50)
        idadePet = Entry(updateWindow, width=50)
        nomeProprietario = Entry(updateWindow, width=50)
        celular = Entry(updateWindow, width=50)
        endereco = Entry(updateWindow, width=50)
        cidade = Entry(updateWindow, width=50)
        especie = Entry(updateWindow, width=50)
        sexo = Entry(updateWindow, width=50)
        raca = Entry(updateWindow, width=50)
        peso = Entry(updateWindow, width=50)
        observacoes = Text(updateWindow, width=50, height=10, font=('Segoe UI', '9'))

        # Criando as Labels para identificar cada Entry
        nomePetLabel = Label(updateWindow, text='Nome do Pet:', anchor='w', justify='left', width=20)
        idadePetLabel = Label(updateWindow, text='Idade do Pet:', anchor='w', justify='left', width=20)
        nomeProprietarioLabel = Label(updateWindow, text='Nome do(a) Proprietário(a):', anchor='w', justify='left', width=20)
        celularLabel = Label(updateWindow, text='Celular:', anchor='w', justify='left', width=20)
        enderecoLabel = Label(updateWindow, text='Endereço:', anchor='w', justify='left', width=20)
        cidadeLabel = Label(updateWindow, text='Cidade:', anchor='w', justify='left', width=20)
        especieLabel = Label(updateWindow, text='Espécie:', anchor='w', justify='left', width=20)
        sexoLabel = Label(updateWindow, text='Sexo:', anchor='w', justify='left', width=20)
        racaLabel = Label(updateWindow, text='Raça:', anchor='w', justify='left', width=20)
        pesoLabel = Label(updateWindow, text='Peso:', anchor='w', justify='left', width=20)
        observacoesLabel = Label(updateWindow, text='Observações:', anchor='w', justify='left', width=20)

        # Colocando todos os widgets na tela usando for loops
        entrys = [nomePet, idadePet, nomeProprietario, celular, endereco, cidade, especie, sexo, raca, peso, observacoes]

        for row, entry in enumerate(entrys):
            entry.grid(row=row, column=1, sticky='ew', pady=5, padx=5)

        labels = [nomePetLabel, idadePetLabel, nomeProprietarioLabel, celularLabel, enderecoLabel, cidadeLabel,
                especieLabel, sexoLabel, racaLabel, pesoLabel, observacoesLabel]
        
        for row, label in enumerate(labels):
            label.grid(row=row, column=0, pady=5)
        
        # Utilizando o método insert para mostrar as informações na tela Entry
        nomePet.insert(0, record[0])
        idadePet.insert(0, record[1])
        nomeProprietario.insert(0, record[2])
        celular.insert(0, record[3])
        endereco.insert(0, record[4])
        cidade.insert(0, record[5])
        especie.insert(0, record[6])
        sexo.insert(0, record[7])
        raca.insert(0, record[8])
        peso.insert(0, record[9])
        observacoes.insert(INSERT, record[10])

        # Criando o botão para salvar e enviar as informações
        submitUpdateButton = Button(updateWindow, text='Salvar e enviar', command=submitUpdatedRecord)
        submitUpdateButton.grid(row=12, columnspan=2, padx=5, pady=5)

    def deleteRecord():
        response = messagebox.askyesno('Deletar prontuário', 'Você tem certeza?')
        if response == 1:
            conn = sqlite3.connect('prontuarios.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM prontuarios WHERE oid = ' + str(oid))

            messagebox.showinfo('Aviso', 'Prontuário deletado com sucesso!')

            # Destruindo e reconstruindo right frame

            global rightFrame

            rightFrame.destroy()

            rightFrame = Frame(root, bg='lavender', width=50, height=height)

            rightFrame.grid(row=0, column=1, sticky='nsew')

            rightFrame.columnconfigure(0, weight=1)

            conn.commit()
            conn.close()

            recordWindow.destroy()

            rightFrameBuilder()

    # Estabelecendo conexão com database
    conn = sqlite3.connect('prontuarios.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM prontuarios WHERE oid = ' + str(oid))
    record = cursor.fetchone()

    # Configurando nova tela acessada
    recordWindow = Tk()
    recordWindow.title(f'Prontuário de {record[0]}')
    recordWindow.iconbitmap('img_ico\\enter_icon.ico')
    recordWindow.resizable(False, False)

    # Configurando espaço da nova tela
    recordWindow.columnconfigure(0, weight=3)
    recordWindow.columnconfigure(1, weight=7)

    for row in range(11):
        recordWindow.rowconfigure(row, weight=1)

    # Adicionando conteúdo na nova tela

    # Criando as Labels para identificar cada informação
    nomePetLabel = Label(recordWindow, text='Nome do Pet:', anchor='w', justify='left', width=22)
    idadePetLabel = Label(recordWindow, text='Idade do Pet:', anchor='w', justify='left', width=22)
    nomeProprietarioLabel = Label(recordWindow, text='Nome do(a) Proprietário(a):', anchor='w', justify='left', width=25)
    celularLabel = Label(recordWindow, text='Celular:', anchor='w', justify='left', width=22)
    enderecoLabel = Label(recordWindow, text='Endereço:', anchor='w', justify='left', width=22)
    cidadeLabel = Label(recordWindow, text='Cidade:', anchor='w', justify='left', width=22)
    especieLabel = Label(recordWindow, text='Espécie:', anchor='w', justify='left', width=22)
    sexoLabel = Label(recordWindow, text='Sexo:', anchor='w', justify='left', width=22)
    racaLabel = Label(recordWindow, text='Raça:', anchor='w', justify='left', width=22)
    pesoLabel = Label(recordWindow, text='Peso:', anchor='w', justify='left', width=22)
    observacoesLabel = Label(recordWindow, text='Observações:', anchor='w', justify='left', width=22)

    # Criando as labels para mostrar cada informação
    nomePetInfo = Label(recordWindow, text=record[0], anchor='w', justify='left', width=22)
    idadePetInfo = Label(recordWindow, text=record[1], anchor='w', justify='left', width=22)
    nomeProprietarioInfo = Label(recordWindow, text=record[2], anchor='w', justify='left', width=22)
    celularInfo = Label(recordWindow, text=record[3], anchor='w', justify='left', width=22)
    enderecoInfo = Label(recordWindow, text=record[4], anchor='w', justify='left', width=22)
    cidadeInfo = Label(recordWindow, text=record[5], anchor='w', justify='left', width=22)
    especieInfo = Label(recordWindow, text=record[6], anchor='w', justify='left', width=22)
    sexoInfo = Label(recordWindow, text=record[7], anchor='w', justify='left', width=22)
    racaInfo = Label(recordWindow, text=record[8], anchor='w', justify='left', width=22)
    pesoInfo = Label(recordWindow, text=str(record[9]), anchor='w', justify='left', width=22)
    observacoesInfo = Label(recordWindow, text=record[10], anchor='w', justify='left', width=35)
    
    # Adicionando as Labels através de um for loop
    labels = [nomePetLabel, idadePetLabel, nomeProprietarioLabel, celularLabel, enderecoLabel, cidadeLabel,
              especieLabel, sexoLabel, racaLabel, pesoLabel, observacoesLabel]
    
    for row, label in enumerate(labels):
        label.grid(row=row, column=0, pady=5)

    info = [nomePetInfo, idadePetInfo, nomeProprietarioInfo, celularInfo, enderecoInfo, cidadeInfo,
              especieInfo, sexoInfo, racaInfo, pesoInfo, observacoesInfo]
    
    for row, info in enumerate(info):
        info.grid(row=row, column=1, pady=5, sticky='ew')

    # Adicionando os botões: Deletar e Atualizar
    buttonFrame = Frame(recordWindow, width=50)
    buttonFrame.grid(row=12, columnspan=2)

    buttonFrame.rowconfigure(0, weight=1)
    buttonFrame.columnconfigure(0, weight=1)
    buttonFrame.columnconfigure(1, weight=1)

    deleteButton = Button(buttonFrame, text='Deletar prontuário', command=deleteRecord)
    updateButton = Button(buttonFrame, text='Atualizar prontuário', command=updateRecord)

    deleteButton.grid(row=0, column=0, padx=5, pady=5)
    updateButton.grid(row=0, column=1, padx=5, pady=5)

    conn.commit()
    conn.close()

# Cria a janela e define suas configurações principais
root = Tk()
root.title('MaraVet')
root.iconbitmap('img_ico\\vet_icon.ico')

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')
root.state('zoomed')

# Criando todos os contâineres principais
leftFrame = Frame(root, bg='gray', width=50, height=height)

rightFrame = Frame(root, bg='lavender', width=50, height=height)

# Colocando os contâineres principais no layout
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=7)

leftFrame.grid(row=0, column=0, sticky='nsew')
rightFrame.grid(row=0, column=1, sticky='nsew')

# Configurando cada contâiner

# Configurando leftFrame
leftFrame.rowconfigure(0, weight=1)

leftFrame.columnconfigure(0, weight=1)

leftFrame.grid_propagate(False)

rightFrame.columnconfigure(0, weight=1)

# Criando os contâineres principais do rightFrame através de um for loop #rightFrameConstructor
rightFrameBuilder()

# Criando os botões: Adicionar
addRecord = Button(leftFrame, text='Adicionar novo prontuário', command=newRecord, height=10)

# Adicionando o botão de funcionalidade principal
addRecord.grid(row=0, sticky='new', padx=10, pady=10)

root.mainloop()