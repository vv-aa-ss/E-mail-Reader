"""
Сейчас буду разбираться с другими потовыми сервисами
Если разберусь изменю код так, чтобы можно было удобно добавлять несколько аккаунтов + использовать какие либо фильтры.
Еще планирую обязательно добавить удаление прочитанных сообщений, или загрузку только новых
"""

import imapclient
import pyzmail


def connect(): # Подключаемся к аккаунту, заходим в папку Входящие
    login = '***2-3@mail.ru'
    password = 'Sx***PDpFvxb'
    server = 'imap.mail.ru'

    imapObj = imapclient.IMAPClient(server, ssl=True)
    imapObj.login(login, password)
    imapObj.select_folder('INBOX', readonly=True)
    UIDs = imapObj.search(['ALL'])
    iter_mess(UIDs, imapObj)


def iter_mess(UIDs, imapObj):# Итерируем по входящим
    global result
    number = 1
    for id_s in UIDs:
        result += (f'===---===---===---===---===---===---===---\nСообщение №{number}\n')
        rawMessages = imapObj.fetch(id_s, ['BODY[]'])
        result += give_text_message(rawMessages, id_s)
        number+=1
    imapObj.logout()


def give_text_message(r_mess, id_mes): #Приводим сырой E-mail в человеческий вид
    message = pyzmail.PyzMessage.factory(r_mess[id_mes][b'BODY[]'])
    fr_m = message.get_addresses('from')
    to = message.get_addresses('to')
    subject = message.get_subject()
    if message.text_part != None:
        txt_message = message.text_part.get_payload().decode(message.html_part.charset)
    else:
        txt_message = message.get_payload()
        txt_message = txt_message.replace("</div>", "\n") # Это конечно ужасно, но пока я не знаю как иначе
        txt_message = txt_message.replace("<div>", "")

    result = (f''
        f'{"Сообщение от пользователя:".ljust(29)}{fr_m[0][0]} \t e-mail:{fr_m[0][1]}\n'
        f'{"На вашу почту:".ljust(28)} {to[0][1]}\n'
        f'{"Тема:".ljust(28)} {subject}\n\n'
        f'{"Сообщение:".ljust(28)}\n{txt_message}'
        f'===---===---===---===---===---===---===---\n\n')
    return result


def save_to_file(text):
    with open("mail.txt", 'w', encoding="utf-8") as file:
        file.write(result)


if __name__ == '__main__':
    result = ""
    connect()
    save_to_file(result)
