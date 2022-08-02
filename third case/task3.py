import hashlib
import pandas as pd


class MicroLib:
    def __init__(self, lib_name):
        self.__lib = lib_name
        self.__users = {}
        self.__signed_in = None
        self.__pass_hash = None
        headers = ['Користувач', 'Хеш паролю', 'Назва фільму', 'Відгук', 'Оцінка']
        self.__all_notes = pd.read_csv(self.__lib, sep='|', names=headers, header=0)
        for i in range(len(self.__all_notes)):
            self.__users[self.__all_notes.iloc[i]['Користувач']] = self.__all_notes.iloc[i]['Хеш паролю']
        print(self.__users)
        self.terminal()

    def terminal(self):
        command = input()
        if command == 'exit':
            return
        eval(f'self.{command}')
        self.terminal()

    def update_df(self):
        self.__all_notes = pd.read_csv(self.__lib, sep='|', header=0, index_col=False)

    def register(self):
        nickname = input('Nickname: ')
        password = input('Password: ')
        if nickname in self.__users:
            print('Користувач з таким іменем вже існує!')
            return
        else:
            self.__users[nickname] = hashlib.md5(password.encode()).hexdigest()
            print('Ви успішно зареєстровані!')

    def login(self):
        nickname = input('Nickname: ')
        password = input('Password: ')
        if nickname not in self.__users:
            print('Користувача з таким іменем не існує!')
            choice = input('Бажаєте зареєструватися? - ')
            if choice == 'так':
                self.register()
            else:
                return
        elif self.__users[nickname] == hashlib.md5(password.encode()).hexdigest():
            print('Ви успішно авторизовані!')
            self.__signed_in = nickname
            self.__pass_hash = hashlib.md5(password.encode()).hexdigest()
            return

    def add_note(self):
        if not self.__signed_in:
            print('Спершу ви повинні авторизуватися:')
            choice = input('Увійти чи зареєструватися? -')
            if choice.lower() == 'увійти':
                self.login()
            elif choice.lower() == 'зареєструватися':
                self.register()
                print("Авторизуйтеся: ")
                self.login()
        if self.__signed_in:
            film_name = input('Введіть назву фільму: ')
            note = input('Напишіть відгук для фільму: ')
            while True:
                try:
                    mark = int(input('Дайте вашу оцінку для фільму(1-5)'))
                except TypeError:
                    print('Оцінка повинна бути цілим числом від 1 до 5!')
                    continue
                if (mark > 0) and (mark < 6):
                    break
                else:
                    print('Оцінка повинна бути цілим числом від 1 до 5!')
            notes = {
                'Користувач': [self.__signed_in],
                'Хеш паролю': [self.__pass_hash],
                'Назва фільму': [film_name],
                'Відгук': [note],
                'Оцінка': [mark]
            }
            df = pd.DataFrame(notes)
            df.to_csv(self.__lib, mode='a', sep='|')
            self.update_df()

    def delete_note(self):
        if not self.__signed_in:
            print('Спершу ви повинні авторизуватися:')
            choice = input('Увійти чи зареєструватися? -')
            if choice.lower() == 'увійти':
                self.login()
            elif choice.lower() == 'зареєструватися':
                self.register()
                print("Авторизуйтеся: ")
                self.login()
        elif self.__signed_in:
            film_name = input('Відгук до якого фільму ви бажаєте видалити? ')
            if any(self.__all_notes.loc[(self.__all_notes['Користувач'] == self.__signed_in) &
                                        (self.__all_notes['Назва фільму'] == film_name)]):
                print(self.__all_notes.loc[(self.__all_notes['Користувач'] == self.__signed_in) &
                                           (self.__all_notes['Назва фільму'] == film_name)])
                num = int(input('Номер якого відгуку ви бажаєте видалити?'))
                if any(self.__all_notes.loc[(self.__all_notes['Користувач'] == self.__signed_in) &
                                            (self.__all_notes.index.isin([num]))]):
                    print(233)
                    self.__all_notes = self.__all_notes.drop(num, axis=0)
                    self.__all_notes.to_csv(self.__lib, sep='|')

    def read_notes(self, film_name):
        if any(self.__all_notes.loc[(self.__all_notes['Назва фільму'] == film_name)]):
            print(f'Відгуки до фільму "{film_name}"')
            print(self.__all_notes.loc[(self.__all_notes['Назва фільму'] == film_name), ['Користувач', 'Відгук',
                                                                                         'Оцінка']])
        else:
            print('На жаль, відгуків до цього фільму ще немає')

    def read_all(self):
        print(self.__all_notes[['Користувач', 'Назва фільму', 'Відгук', 'Оцінка']])

    def get_highest(self):
        film_mark = {}
        unique = self.__all_notes['Назва фільму'].unique()
        for name in unique:
            df = self.__all_notes.loc[self.__all_notes['Назва фільму'] == name]
            film_mark[name] = df['Оцінка'].mean()
        rating_list = sorted(film_mark, key=film_mark.get, reverse=True)
        if len(rating_list) >= 5:
            print('Топ фільмів з найвищим рейтингом:')
            for i in range(5):
                print(f'{rating_list[i]}: {film_mark[rating_list[i]]}')
        else:
            print('Топ фільмів з найвищим рейтингом:')
            for i in range(len(rating_list)):
                print(f'{rating_list[i]}: {film_mark[rating_list[i]]}')

    def get_lowest(self):
        film_mark = {}
        unique = self.__all_notes['Назва фільму'].unique()
        for name in unique:
            df = self.__all_notes.loc[self.__all_notes['Назва фільму'] == name]
            film_mark[name] = df['Оцінка'].mean()
        rating_list = sorted(film_mark, key=film_mark.get)
        if len(rating_list) >= 5:
            print('Топ фільмів з найнижчим рейтингом:')
            for i in range(5):
                print(f'{rating_list[i]}: {film_mark[rating_list[i]]}')
        else:
            print('Топ фільмів з найнижчим рейтингом:')
            for i in range(len(rating_list)):
                print(f'{rating_list[i]}: {film_mark[rating_list[i]]}')

    def average_rating(self):
        print(f'Середня оцінка серед усіх фільмів в бібліотеці: {self.__all_notes["Оцінка"].mean()}')


lib = MicroLib('Library.csv')
