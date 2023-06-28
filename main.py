# -*- coding: utf8 -*-
'''Программа для рандомной выдочи карточек к собеседованию'''

import requests
from datetime import datetime
import telebot
from random import shuffle, choice
import datetime
import sqlite3

token = '6034011497:AAHN0vZgct7hqIFaqK-pp8B4UCybxpD3bzg'

db = sqlite3.connect('server.db')
sql = db.cursor()



class Card:
    '''класс карточки с вопросом и ответом'''

    def __init__(self, number):
        sql.execute(f"SELECT * FROM cards WHERE card_number = {number}")
        res = sql.fetchall()
        self.number = number
        self.question = res[0][1]
        self.answer = res[0][2]

    def show_number(self):
        print(f"Номер карточки: {self.number}")

    def quest(self):
        result = str(self.number) + " " + str(self.question)
        return result

    def answ(self):
        result = str(self.answer)
        return result

def create_tables():
    """Создает таблицы в БД"""
    sql.execute("CREATE TABLE IF NOT EXISTS cards ("
                "card_number INTEGER primary key,"
                "card_question TEXT,"
                "card_answer TEXT)")
    db.commit()
    print("таблица cards создана")

def drop_tables():
    sql.execute("DROP TABLE cards")
    db.commit()
    print("таблицы дропнуты")
    create_tables()

def new_card(question: str, answer: str):
    sql.execute(f"INSERT INTO cards (card_question, card_answer) VALUES ('{question}', '{answer}')")
    db.commit()
    print("карточка добавлена")


def rand_card():
    # cards_list = [card5, card7, card10, card17, card23, card24, card25, card30, card34, card36]
    # all cards
    # cards_list = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card11, card12, card13, card14,
    #              card15, card16, card17, card18, card19, card20, card21, card22, card23, card24, card25, card26, card27,
    #              card28, card29, card30, card31, card32, card33, card34, card35, card36, card37, card38, card39, card40,
    #              card41, card42, card43, card44, card45, card46, card47, card48, card49, card50]
    # group 1
    # cards_list = [card5, card6, card8, card12, card13, card16, card17, card20, card30, card33, card38, card45]
    # group 2
    # cards_list = [card31, card9, card35, card44, card7, card23, card32, card26, card49, card4, card24]
    # group3 = [card36, card34, card27, card28, card50, card10, card2, card43, card25, card22, card29]
    # group4 = [card1, card3, card11, card14, card15, card18, card19, card21]
    # group5 = [card37, card39, card40, card41, card42, card46, card47, card48]
    # cards_list = [card5, card6, card8, card12, card13, card16, card17, card20, card30, card33, card38, card45]
    # print("len cards_list = ", len(cards_list))
    cards_list = []
    today = datetime.datetime.today().weekday()
    if today == 0:
        cards_list = [card5, card6, card8, card12, card13, card16, card17, card20, card30, card33, card38, card45]
    elif today == 1:
        cards_list = [card31, card9, card35, card44, card7, card23, card32, card26, card49, card4, card24]
    elif today == 2:
        cards_list = [card36, card34, card27, card28, card50, card10, card2, card43, card25, card22, card29]
    elif today == 3:
        cards_list = [card1, card3, card11, card14, card15, card18, card19, card21]
    elif today == 4:
        cards_list = [card37, card39, card40, card41, card42, card46, card47, card48]
    else:
        cards_list = [card1]

    shuffle(cards_list)
    s = choice(cards_list)
    return s.quest()


def card_answer(number):
    sql.execute(f"SELECT card_answer FROM cards WHERE card_number = {number}")
    answer = sql.fetchall()
    return answer[0][0]



def norm_number(number):
    if number.isdigit():
        return int(number)
    else:
        return 0

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello!")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text == "test":
            bot.send_message(message.chat.id, "test ok")
        elif message.text == "l":
            try:
                bot.send_message(message.chat.id, rand_card())
            except Exception as ex:
                bot.send_message(
                    message.chat.id,
                    f"something wrong: {ex}"
                )
                print(ex)
        elif norm_number(message.text) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                           22, 23, 24,
                                           25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,
                                           44, 45, 46, 47, 48, 49, 50]:
            try:
                bot.send_message(message.chat.id, card_answer(int(message.text)))
            except Exception as ex:
                bot.send_message(message.chat.id, f"самсынг вронг {ex}")
                print(ex)
        else:
            bot.send_message(
                message.chat.id,
                "chek the command"
            )

    bot.polling()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # telegram_bot(token)
    # new_card('вопрос 1', 'ответ 1')
    # new_card('вопрос 2', 'ответ 2')
    # new_card('вопрос 3', 'ответ 3')
    # print(card_answer(1))
    # sql.execute("INSERT INTO cards (card_question, card_answer) VALUES ('вопрс 2', 'ответ 2')")
    # sql.execute(f"INSERT INTO clients (client_name) VALUES ('{name}')")
    # db.commit()
    card1 = Card(3)
    card1.show_number()
    print(card1.quest())
    print(card1.answer)

    # drop_tables()


# сделать динамическое добавление экземпляров класса из БД