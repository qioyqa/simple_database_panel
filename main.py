import sqlite3 as sq

class DataBase:
    def __init__(self):
        self.__name = None
        self.__value = None
        self.__user_id = None
        self.__new_user_id = None

    @classmethod
    def __validate(cls, name: str = "", score: int = 0,new_user_id: int = 0, user_id: int = 0) -> bool:
        if isinstance(name, str) and isinstance(score, int) and isinstance(user_id, int) and isinstance(new_user_id, int):
            return True
        else:   raise ValueError()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if self.__validate(name):
            self.__name = name

    @property
    def score(self):
        return self.__value

    @score.setter
    def score(self, score: int):
        if self.__validate(score=score):
            self.__value = score

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        if self.__validate(user_id=user_id):
            self.__user_id = user_id

    @property
    def new_user_id(self):
        return self.__new_user_id 

    @new_user_id.setter
    def new_user_id(self, new_user_id: int):
        if self.__validate("",0,new_user_id,0):
            self.__new_user_id = new_user_id

    def drop_db(self):
        return "DROP TABLE IF EXISTS users"
    
    def creating_db(self):
        return """CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER,
            name TEXT,
            score INTEGER
        )"""

    def insert_db(self):
        return "INSERT INTO users (user_id, name, score) VALUES (?, ?, ?)", (self.__user_id, self.__name, self.__value)

    def delete_db(self):
        return "DELETE FROM users WHERE user_id = ?", (self.__user_id,)
    
    def select_all(self):
        return "SELECT * FROM users"

    def select_by_userid(self):
        return "SELECT * FROM users WHERE user_id = ?", (self.__user_id,)

    def select_by_name(self):
        return "SELECT * FROM users WHERE name = ?", (self.__name,)

    def select_by_score(self):
        return "SELECT * FROM users WHERE score = ?", (self.__value,)

    def sum_by_id(self):
        return ("select user_id, sum(score) as sum_score from users where user_id = ? group by user_id", (self.__user_id,))

    def update(self):
        return ("UPDATE users SET name = ?, score = ?,user_id = ? WHERE user_id = ?"), (self.__name, self.__value,self.__new_user_id, self.__user_id)

db = DataBase()

with sq.connect("test.db") as con:
    cur = con.cursor()
    
    while True:
        print("\nВыберите действие:")
        print("[1] Создать таблицу users")
        print("[2] Вставить пользователя")
        print("[3] Удалить пользователя по user_id")
        print("[4] Просмотреть все записи")
        print("[5] Найти пользователя по user_id")
        print("[6] Найти пользователя по имени")
        print("[7] Найти пользователя по score")
        print("[8] Суммирование по id")
        print("[9] Удалить базу данных")
        print("[10] Обновить базу данных")
        print("[11] Выход")

        choose = input(">>> ")

        match choose:
            case "1":
                cur.execute(db.creating_db())
                print("✅ Таблица создана.")

            case "2":
                temp = input("Введите имя, счет и id пользователя через пробел: ").split()
                db.name = temp[0]
                db.score = int(temp[1])
                db.user_id = int(temp[2])
                query, params = db.insert_db()
                cur.execute(query, params)
                con.commit()
                print("✅ Пользователь добавлен.")

            case "3":
                db.user_id = int(input("Введите user_id для удаления: "))
                query, params = db.delete_db()
                cur.execute(query, params)
                con.commit()
                print("✅ Пользователь удалён.")

            case "4":
                query = db.select_all()
                cur.execute(query)
                items = cur.fetchall()

                if items:
                    for i in items:
                        print(i)
                else: print("❌ Пользователь не найден.")

            case "5":
                db.user_id = int(input("Введите user_id для поиска: "))
                query, params = db.select_by_userid()
                cur.execute(query, params)
                result = cur.fetchone()
                print(result if result else "❌ Пользователь не найден.")

            case "6":
                db.name = input("Введите имя для поиска: ")
                query, params = db.select_by_name()
                cur.execute(query, params)
                results = cur.fetchall()

                if results:
                    for row in results:
                        print(row)
                else:
                    print("❌ Пользователи не найдены.")

            case "7":
                db.score = int(input("Введите score для поиска: "))
                query, params = db.select_by_score()
                cur.execute(query, params)
                results = cur.fetchall()

                if results:
                    for row in results:
                        print(row)
                else:
                    print("❌ Пользователи не найдены.")

            case "8":
                db.user_id = int(input("Введите id для суммирования: "))
                query, params = db.sum_by_id()
                cur.execute(query, params)
                result = cur.fetchone()

                if result:
                    print(f"User_id: {result[0]}, Sum of scores: {result[1]}")
                else:
                    print("❌ Пользователи не найдены.")

            case "9":
                cur.execute(db.drop_db())
                print("✅ База данных удалена" )
            
            case "10":
                cur.execute(db.select_all())
                items = cur.fetchall()

                if items:
                    for i in items:
                        print(i)
                else: print("❌ Пользователи не найдены.")

                temp = input("Введите новые данные пользователя: имя/рекорд/id пользователя и id пользователя для подверженого изменению").split()
                db.name = temp[0]
                db.score = int(temp[1])
                db.new_user_id = int(temp[2])
                db.user_id = int(temp[3])

                query, params = db.update()
                cur.execute(query, params)
                result = cur.fetchall() 
                print(f"Данные обновленны на: имя: {db.name}, рекорд: {db.score}, id пользвателя {db.user_id}")

            case "11":
                print("👋 Выход из программы.")
                break
            case _:
                print("❗ Неверный выбор. Попробуйте снова.")
