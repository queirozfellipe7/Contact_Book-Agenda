import tkinter as tk
from tkinter import *
import sqlite3

#Inicia o Banco de dados
#Start the Database
path = r"./Agenda"
conn = sqlite3.connect(path+r'/agenda.db')
cursor = conn.cursor()

#Inicia dados da interface grafica
#Start graphical interface data
root = Tk()
root.title("Contacts book")

#Cria a tabela agenda no banco de dados
#Create the agenda table in the database
def criar_banco():
    try:
        esaporra = """CREATE TABLE agenda (nome TEXT NOT NULL, telefone TEXT, endereco TEXT);"""
        cursor.execute(esaporra)
    except sqlite3.Error as error:
        return 0
#Adiciona os dados do contato no banco de dados   
#Add the contact's data to the database    
def adicionar():
    cursor.execute(""" INSERT INTO agenda (nome, telefone, endereco) VALUES (?,?,?) """, (nome.get(), telefone.get(), endereco.get()))
    conn.commit()
    selection = "O contato de "+str(nome.get())+ " foi adicionado "
    label.config(text = selection)
#Pelo nome remove um usuario do banco de dados 
#By name removes a user from the database
def remover():
    if(nome.get()==""):
        selection = "Informe nome do contato a ser removido "
        label.config(text= selection)
    else:
        selection ="o Contato "+ nome.get()+ " foi removido "
        label.config(text= selection)
        cursor.execute(""" DELETE FROM agenda WHERE nome = ?""", (nome.get(),))
        conn.commit()
#pelo nome atualiza os dados do usuario 
#by name updates user data
def atualizar():
    if(telefone.get()!=""):
        cursor.execute(""" UPDATE agenda SET telefone = ? WHERE nome = ? """, (telefone.get(),nome.get()))
        selection ="o Telefone de "+ nome.get()+ " foi atualizado "
        label.config(text= selection)
        conn.commit()
    elif(endereco!=""):
        cursor.execute("""UPDATE agenda SET endereco = ? WHERE nome = ?""", (endereco.get(),nome.get()))
        selection ="o endereco de "+ nome.get()+ " foi atualizado "
        label.config(text= selection)
        conn.commit()
#Pelo nome procura os dados do usuario no banco de dados
#By name searches the user's data in the database
def procurar():
    porra=nome.get()
    sql_select = """select * from agenda where nome = ?"""
    cursor.execute(sql_select,(porra,))
    records = cursor.fetchall()
    for row in records:
        selection ="Nome: "+ row[0]+ "\nTelefone: "+row[1]+"\nEndereço: "+ row[2]
        label.config(text= selection)
#Lista todos os contatos do banco de dados
#List all contacts in the database
def listar():
    cursor.execute("""SELECT * FROM agenda;""")
    tostring =""
    records = cursor.fetchall()
    for linha in records:
            tostring= tostring+"Nome: "+str(linha[0])+"\n"+"Telefone: "+str(linha[1])+"\n"+"Endereço: "+str(linha[2])+"\n\n"
    selection = tostring
    label.config(text= selection)

if __name__ == '__main__':
        #Variaveis nome,endereco,telefone 
        #Variables name, address, telephone
        nome = tk.StringVar()
        endereco = tk.StringVar()
        telefone = tk.StringVar()

        #Execucao da interfacegrafica
        #Execution of the interface

        toolbar = Frame(root)
        toolbar.grid(row=4, columnspan=2)
        toolbare = Frame(root)
        toolbare.grid(row=5, columnspan=3)

        lbl1= tk.Label(root, text="Nome:")
        lbl2= tk.Label(root, text="Endereço:")
        lbl3= tk.Label(root, text="Telefone:")
        lbl1.grid(row=1, sticky=W)
        lbl2.grid(row=2, sticky=W)
        lbl3.grid(row=3, sticky=W)
            
        en1 = tk.Entry(root, textvariable=nome)
        en2 = tk.Entry(root, textvariable=endereco)
        en3 = tk.Entry(root, textvariable=telefone)

        en1.grid(row=1, column=1, sticky=W+E)
        en2.grid(row=2, column=1, sticky=W+E)
        en3.grid(row=3, column=1, sticky=W+E)

        Button(toolbar, text="Adicionar",command=adicionar).grid(row=0,column=0)
        Button(toolbar, text="Atualizar",command=atualizar).grid(row=0,column=2)
        Button(toolbar, text="Remover",command=remover).grid(row=0,column=1)
        Button(toolbar, text="Procurar",command=procurar).grid(row=0,column=3)
        Button(toolbar, text="Listar",command=listar).grid(row=0,column=4)

        label = Label(toolbare)
        label.grid(row=1,column=0)


        criar_banco()
        root.mainloop()