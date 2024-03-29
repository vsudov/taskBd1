import sqlite3

class Model:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
    
    def add_record(self, data):
        query = 'INSERT INTO users (name, surname, yearsOld, email) VALUES (?, ?, ?, ?)'
        self.cursor.execute(query, (data['name'], data['surname'], data['yearsOld'], data['email']))
        self.connection.commit()
        print('Данные добавлены.')
    
    def delete_record(self, id):
        query = 'DELETE FROM users WHERE id = ?'
        self.cursor.execute(query, (id,))
        self.connection.commit()
        print('Строка удалена.')
        
    def search_record(self, value):
        query = f"SELECT * FROM users WHERE name = '{value}' OR surname = '{value}' OR email = '{value}'"
        result = self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def show_all_records(self):
        query = 'SELECT * FROM users'
        results = self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        if(rows):
            print('№:\tИмя:\tФамилия:\tВозраст:\tЭл. почта:')
            for row in rows:
                print(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4]))
        else:
            print('Записей нет.')

class Presenter:
    model = Model()
    login = 'test'
    password = '123456'
    
    def add(self):
        name = input('Введите имя:\t')
        surname = input('Введите фамилию:\t')
        yearsOld = int(input('Введите возраст:\t'))
        email = input('Введите эл. почту:\t')
        
        data = {
            'name': name,
            'surname': surname,
            'yearsOld': yearsOld,
            'email': email
        }
        
        self.model.add_record(data)
        
    def delete(self, record_id):
        self.model.delete_record(record_id)

    def search(self, value):
        records = self.model.search_record(value)
        if records:
            print('Найдено совпадение:')
            print('№:\tИмя:\tФамилия:\tВозраст:\tЭл. почта:')
            for row in records:
                print(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4]))
        else:
            print('Совпадений не найдено')

    def view_all(self):
        self.model.show_all_records()

    def auth(self):
        isAuth = False
        tries = 0

        while(not(isAuth)):
            login = str(input('Введите логин:\t'))
            password = str(input('Введите пароль:\t'))
            tries+=1
            
            if(tries < 3):
                if(login == self.login and password == self.password):
                    isAuth = True
                    break
                else:
                    print(f'Не правильный логин или пароль! У Вас осталось {3-tries} попыток')
            else:
                break
        return isAuth
    

presenter = Presenter()

if presenter.auth():
    while True:
        print('1 - Добавить запись\n2 - Удалить запись\n3 - Найти запись\n4 - Показать все записи\n5 - Выход')
        comand = int(input('Выберите команду:\t'))
        
        if(comand == 5):
            print('Выход выполнен.')
            break
        elif(comand == 1):
            presenter.add()
        elif(comand == 2):
            presenter.view_all()
            choice = int(input('Выберите строку для удаления:\t'))
            presenter.delete(choice)
        elif(comand == 3):
            searchValue = input('Введите текст для поиска:\t')
            presenter.search(searchValue)
        elif(comand == 4):
            presenter.view_all()
        else:
            print('Неизвестная команда!')
else:
    print('В доступе отказано!')
