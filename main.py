import sqlite3 as sq

class DataBase:
    def __init__(self):
        self.__name = None
        self.__value = None
        self.__user_id = None

    @classmethod
    def __validate(cls, name: str = "", score: int = 0, user_id: int = 0) -> bool:
        if isinstance(name, str) and isinstance(score, int) and isinstance(user_id, int):
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

    def creating_db(self):
        return """CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score INTEGER
        )"""

    def insert_db(self):
        return "INSERT INTO users (name, score) VALUES (?, ?)", (self.__name, self.__value)

    def delete_db(self):
        return "DELETE FROM users WHERE user_id = ?", (self.__user_id,)

    def select_by_userid(self):
        return "SELECT * FROM users WHERE user_id = ?", (self.__user_id,)

    def select_by_name(self):
        return "SELECT * FROM users WHERE name = ?", (self.__name,)

    def select_by_score(self):
        return "SELECT * FROM users WHERE score = ?", (self.__value,)


db = DataBase()

with sq.connect("test.db") as con:
    cur = con.cursor()
    
    while True:
        print("\nВыберите действие:")
        print("[1] Создать таблицу users")
        print("[2] Вставить пользователя")
        print("[3] Удалить пользователя по user_id")
        print("[4] Найти пользователя по user_id")
        print("[5] Найти пользователя по имени")
        print("[6] Найти пользователя по score")
        print("[7] Выход")

        choose = input(">>> ")

        match choose:
            case "1":
                cur.execute(db.creating_db())
                print("✅ Таблица создана.")
            case "2":
                temp = input("Введите имя и счёт через пробел: ").split()
                db.name = temp[0]
                db.score = int(temp[1])
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
                db.user_id = int(input("Введите user_id для поиска: "))
                query, params = db.select_by_userid()
                cur.execute(query, params)
                result = cur.fetchone()
                print(result if result else "❌ Пользователь не найден.")
            case "5":
                db.name = input("Введите имя для поиска: ")
                query, params = db.select_by_name()
                cur.execute(query, params)
                results = cur.fetchall()
                if results:
                    for row in results:
                        print(row)
                else:
                    print("❌ Пользователи не найдены.")
            case "6":
                db.score = int(input("Введите score для поиска: "))
                query, params = db.select_by_score()
                cur.execute(query, params)
                results = cur.fetchall()
                if results:
                    for row in results:
                        print(row)
                else:
                    print("❌ Пользователи не найдены.")
            case "7":
                print("👋 Выход из программы.")
                break
            case _:
                print("❗ Неверный выбор. Попробуйте снова.")
