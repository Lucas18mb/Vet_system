from tkinter import *
import sqlite3

conn = sqlite3.connect('prontuarios.db')

cursor = conn.cursor()

# Criando a table que irá ser utilizada para armazenar as informações
if __name__ == '__main__':

    cursor.execute(""" CREATE TABLE prontuarios (
                nomePet text,
                idadePet text,
                nomeProprietario text,
                celular text,
                endereco text,
                cidade text,
                especie text,
                sexo text,
                raca text,
                peso real,
                observacoes text
    )
    """)