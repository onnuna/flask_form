import flask
import csv
from flask import url_for

app=flask.Flask(__name__, template_folder='templates')

class Osoba:
    def __init__(self, imie, nazwisko, wiek, plec):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek
        self.plec = plec

    def __str__(self):
        return f"{self.imie} {self.nazwisko}, Wiek: {self.wiek}, Płeć: {self.plec}"
    
class Osoby:
    def __init__(self, filename):
        self.filename = filename
        self.osoby = self.load_data()

def load_data(self):
    osoby = []
    with open(self.filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if len(row) == 4:
                osoba = Osoba(row[0], row[1])
                osoba.wiek = row[2]
                osoba.plec = row[3]
                osoby.append(osoba)
    return osoby

def save_data(self):
    with open(self.filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for osoba in self.osoby:
            writer.writerow([osoba.imie, osoba.nazwisko, osoba.wiek, osoba.plec])
            
def add_person(self, osoba):
    self.osoby.append(osoba)
    self.save_data()

def edit_person(self, index, new_osoba):
    if 0 <= index < len(self.osoby):
        self.osoby[index] = new_osoba
        self.save_data()

def delete_person(self, index):
    if 0 <= index < len(self.osoby):
        del self.osoby[index]
        self.save_data()

def display_people(self):
    for i, osoby in enumerate(self.osoby, 1):
        print(f"{i}. {osoby}")

app = flask.Flask(__name__)
database = Osoby("db/base.csv")

@app.route('/')
def home():
    return flask.render_template("index.html")

@app.route('/add/<data>', methods=['POST'])
def add_user(data):
    wyjscie = ''
    for d in data.split('&'):
        wyjscie += d.split('=')[1] + ';'
    wyjscie = wyjscie[:-1] + '\n'
    f = open('db/base.csv', 'a')
    f.write(wyjscie)
    f.close()
    return ''

@app.route('/list')
def list(data=None):
    list_lines = ''
    with open('db/base.csv') as f:
        for line in f.readlines():
            list_lines += f'<li>{line}</li>'
        for osoba in database.osoby:
            list_lines += f'<li>{line.split(";")[0]} {line.split(";")[1]} <button data-action="edit" data-id="{line}">Edytuj</button><button data-action="del"  data-id="{line}">Usuń</button></li>'
            list_lines.append(f'<tr><td>{osoba.imie}</td><td>{osoba.nazwisko}</td><td>{osoba.wiek}</td><td>{osoba.plec}</td><td><button data-action="edit" data-id="{osoba.imie};{osoba.nazwisko};{osoba.wiek};{osoba.plec}">Edytuj</button><button data-action="del" data-id="{osoba.imie};{osoba.nazwisko};{osoba.wiek};{osoba.plec}">Usuń</button></td></tr>')
    return flask.render_template("list.html", list_values = list_lines)

@app.route('/del/<data>', methods=['POST'])
def deletef(data):
    imie, nazwisko, wiek, plec = data.split(';')
    deleted_osoba = Osoba(imie, nazwisko)
    deleted_osoba.wiek = wiek
    deleted_osoba.plec = plec
    database.delete_osoba(database.osoby.index(deleted_osoba))
    list_lines = []
    list_lines = ''
    newlines = ''
    with open('db/base.csv') as f:
        for line in f.readlines():
            if line.strip() == data:
                continue
            newlines += line
            list_lines += f'<li>{line.split(";")[0]} {line.split(";")[1]} <button data-action="edit" data-id="{line}">Edytuj</button><button data-action="del"  data-id="{line}">Usuń</button></li>'
        for osoba in database.osoby:
            list_lines.append(f'<tr><td>{osoba.imie}</td><td>{osoba.nazwisko}</td><td>{osoba.wiek}</td><td>{osoba.plec}</td><td><button data-action="edit" data-id="{osoba.imie};{osoba.nazwisko};{osoba.wiek};{osoba.plec}">Edytuj</button><button data-action="del" data-id="{osoba.imie};{osoba.nazwisko};{osoba.wiek};{osoba.plec}">Usuń</button></td></tr>')
    f = open('db/base.csv', 'w')
    f.write(newlines)
    f.close()
    return list_lines

@app.route('/edit/<data>', methods=['POST'])
def editform(data):
    imie, nazwisko, wiek, plec = data.split(';')
    return flask.render_template("edit.html", name=imie, lastname=nazwisko, age=wiek, gender=plec)

@app.route('/updatedb/<data>', methods=['POST'])
def updatedb(data):
    edited = None
    name = None
    lastname = None
    age = None
    gender = None
    for d in data.split('&'):
        tmp = d.split('=')
        if tmp[0] == 'edit':
            edited = tmp[1]
        elif tmp[0] == 'imie':
            name = tmp[1]
        elif tmp[0] == 'nazwisko':
            lastname = tmp[1]
        elif tmp[0] == 'wiek':
            age = tmp[1]
        elif tmp[0] == 'plec':
            gender = tmp[1]
    edited_osoba = Osoby(name, lastname)
    edited_osoba.wiek = age
    edited_osoba.plec = gender
    database.edit_posoba(database.osoby.index(edited_osoba), edited_osoba)
    list_lines = ''
    newlines = ''
    with open('db/base.csv') as f:
        for line in f.readlines():
            if line.strip() == edited:
                newlines += f'{name};{lastname}\n'
                list_lines += f'<li>{name} {lastname} <button data-action="edit" data-id="{name};{lastname}">Edytuj</button><button data-action="del"  data-id="{name};{lastname}">Usuń</button></li>'
            #    continue
            else:
                newlines += line
                list_lines += f'<li>{line.split(";")[0]} {line.split(";")[1]} <button data-action="edit" data-id="{line}">Edytuj</button><button data-action="del"  data-id="{line}">Usuń</button></li>'
        for osoba in database.osoby:
            list_lines.append(f'<tr><td>{osoba.imie}</td><td>{osoba.nazwisko}</td><td>{osoba.wiek}</td><td>{osoba.plec}</td><td><button data-action="edit" data-id="{osoba.imie};{osoba.nazwisko};{osoba.wiek};{osoba.plec}">Edytuj</button><button data-action="del" data-id="{osoba.imie};{osoba.nazwisko};{osoba.wiek};{osoba.plec}">Usuń</button></td></tr>')
    f = open('db/base.csv', 'w')
    f.write(newlines)
    f.close()
    return list_lines
