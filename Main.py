"""
Программа протестированна в mail.ru, yandex.ru, gmail.com. Позже добавим остальные почтовые сервисы
Для того чтобы работала программа, заходим на вашу почту через веб интерфейс
->>безопасность ->>двухфакторная авторизация ->>создаем пароль для стороннего приложения
Этот пароль вам нужно будет использоватся в этой программе, иначе вы не авторизуетесь
->> Заходим в папку setup, открываем setup.cfg. Там есть пример настройки

Программа создает в папке temp .html файлы на каждую учетную запись с вашими письмами
открывает их в отдельных вкладках в вашем браузере по умолчанию
Сторонних библиотек не используется, все есть в коробке Python

Сорян, пока не сделал перенос прочитанных сообщений в корзину.
Но Скоро добавлю
"""

import imaplib
import email

del_message = 0
auth_data = {}
server = {'@mail.ru': 'imap.mail.ru', '@yandex.ru': 'imap.yandex.ru', '@gmail.com': 'imap.gmail.com'}


def init():
    """Main Def"""
    global del_message
    global auth_data

    try:
        with open("setup/setup.cfg", "r", encoding="utf-8") as file:
            for line in file:
                if not line.startswith('#'):
                    if line.startswith('Delete'):
                        del_message = line.split('=')[1]
                    if "@" in line:
                        temp = line.split(" ")
                        auth_data[temp[0].strip()] = temp[1].strip()
        for user, password in auth_data.items():
            imap = server.get(user[user.find("@"):])
            if server:
                mail_obj = authorization(user, password, imap)
                id_list, mail = give_message_indox(mail_obj)
                result = give_html_text(id_list, mail, user)
                create_and_open_html(result, user)
            else:
                print("Unsupported server (Неподдерживаемый сервер)")
                input("Нажмите Enter чтобы продолжить")
    except Exception as ex:
        print(f"Сорян, мы кое-что не учли. Напишите нам если есть минутка vv.aa.ss@yandex.ru\n{ex}")
        input()
    return 0


def authorization(user, password, server):
    """АВТОРИЗАЦИЯ"""
    mail = imaplib.IMAP4_SSL(server)
    mail.login(user, password)
    return mail


def give_message_indox(mail):
    """ЛОКАЦИЯ"""
    mail.list()
    mail.select("inbox")
    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    return id_list, mail


def give_html_text(ids_list, mail, user):
    """ПРЕОБРАЗУЕМ СЫРОЕ СООБЩЕНИЕ В HTML"""
    letter_count = 1
    all_text = f'<!DOCTYPE html>' \
                f'<html>' \
                    f'<head>' \
                    f'<meta charset="utf-8">' \
                    f'<meta name="description" content="some text">' \
                    f'<title>{user}</title>' \
                    f'</head>'

    """СОБИРАЕМ СООБЩЕНИЯ"""
    for latest_email_id in ids_list[-1:0:-1]:
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8-sig')
        email_message = email.message_from_string(raw_email_string)
        all_text += f'<hr>\n\n<p><font size="11" color="#008B8B" face="Comic Sans MS"><center>Letter #{letter_count}</center></font></p><hr>'
        """ЕСЛИ НЕ ОДНА ЧАСТЬ (HTML + TEXT)"""
        if email_message.is_multipart():
            mes_count = 1
            """ЕСЛИ ТОЛЬКО HTML БЕРЕМ ЕГО, ИНАЧЕ ТОЖЕ САМОЕ, НО БЕРЕМ ПО ДРУГОМУ ИНДЕКСУ"""
            if len(email_message.get_payload()) == 1:
                mes_count = 0
            body = email_message.get_payload()[mes_count].get_payload(decode=True).decode('utf-8')
            all_text += f'\n{body}\n\n'
        else:
            """ДРУГИЕ СЛУЧАИ"""
            body = email_message.get_payload(decode=True).decode('utf-8')
            all_text += f'{body}\n\n'
        letter_count += 1
    return all_text


def create_and_open_html(text, user):
    import webbrowser
    import os
    with open(f"temp/{user}_result.html", "w", encoding="utf-8-sig") as file:
        file.write(text)
    file = os.path.abspath(f"temp/{user}_result.html")
    webbrowser.open(f'file://{file}', 2)


if __name__ == '__main__':
    init()
