# -*- coding: utf8 -*-

from random import randint
import time
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from sqlalchemy import Column, Integer, String, exists, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

engine = sa.create_engine("sqlite:///MathDB7.db")
Base = declarative_base()
metadata = sa.MetaData()

titles = sa.Table("Users", metadata,
                  sa.Column("id", sa.Integer, primary_key=True),
                  sa.Column("Username", sa.String(50), nullable=True),
                  sa.Column("Minus", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Multiply", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Divide", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Sqrt", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Degree", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Coins", sa.Integer, nullable=False, unique=False),
                  sa.Column("Average_Time", sa.Float, nullable=False, unique=False),
                  sa.Column("Bought_Section", sa.Integer, nullable=False, unique=False),
                  sa.Column("Chat_ID", sa.Integer, nullable=False, unique=True),
                  sa.Column("Stop_Activated", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Answer", sa.Integer, nullable=False, unique=False),
                  sa.Column("Start_Time", sa.String(100), nullable=False, unique=False),
                  sa.Column("Want_To_Buy", sa.String(100), nullable=False, unique=False),
                  sa.Column("Shop_Active", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Coins_Per_Task", sa.Integer, nullable=False, unique=False),
                  sa.Column("Completed_Game", sa.Boolean, nullable=False, unique=False),
                  sa.Column("Now_Symbol", sa.String, nullable=False, unique=False)
                  )
metadata.create_all(engine)
Session = sessionmaker(engine)
ses = Session()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    minus = Column(Boolean)
    multiply = Column(Boolean)
    divide = Column(Boolean)
    sqrt = Column(Boolean)
    degree = Column(Boolean)
    coins = Column(Integer)
    average_time = Column(Float)
    bought_section = Column(Integer)
    chat_id = Column(Integer)
    stop_activated = Column(Boolean)
    answer = Column(Integer)
    start_time = Column(String)
    want_to_buy = Column(String)
    shop_active = Column(Boolean)
    coins_per_task = Column(Integer)
    completed_game = Column(Boolean)
    now_symbol = Column(String)


a = '+'
b = '-'
c = '*'
d = ':'
e = '√'
g = '^'
total_episodes = 6
custom_keyboard = [[a, b], [c, d], [e,g]]
reply_markup = ReplyKeyboardMarkup(custom_keyboard)


def generator_for_examples(x, id):
    global string
    c, d = generate_numbers(id)
    if x == 1:
        string = '🤜' + str(c) + ' + ' + str(d) + '🤛'
        ses.query(User).filter(User.chat_id == id).update({'answer': c + d})
        ses.commit()

    if x == 2:
        string = '🤜' + str(c) + ' - ' + str(d) + '🤛'
        ses.query(User).filter(User.chat_id == id).update({'answer': c - d})
        ses.commit()

    if x == 3:
        string = '🤜' + str(c) + ' * ' + str(d) + '🤛'
        ses.query(User).filter(User.chat_id == id).update({'answer': c * d})
        ses.commit()

    if x == 4:
        y = c * d
        string = '🤜' + str(y) + ' : ' + str(d) + '🤛'
        ses.query(User).filter(User.chat_id == id).update({'answer': y / d})
        ses.commit()

    if x == 5:
        string = e + str(c * c)
        ses.query(User).filter(User.chat_id == id).update({'answer': c})
        ses.commit()

    if x == 6:
        string = '🤜' + str(c) + ' ^ ' + str(2) + '🤛'
        ses.query(User).filter(User.chat_id == id).update({'answer': c ** 2})
        ses.commit()


    ses.query(User).filter(User.chat_id == id).update({'coins_per_task': x})
    ses.commit()
    return string


def write_txt(number, id):
    with open(str(id) + ".txt", "w", encoding='utf-8') as output:
        output.write(str(number) + '\n')


def read_text(id):
    f = open(str(id) + '.txt', 'r', encoding='utf-8')
    text = []
    for i in f:
        text.append(i)

    f.close()
    return text


def check_answer(number, id):
    users = ses.query(User).filter(User.chat_id == id).all()
    for user in users:

        write_txt(time.time() - float(user.start_time), id)

        print('User: ', number)
        print('Answer : ', user.answer)

        if str(user.answer) == number:

            user.coins = user.coins + user.coins_per_task
            ses.query(User).filter(User.chat_id == id).update({'coins': user.coins})
            ses.commit()

            return 'Правильно 😊'
        else:
            if user.coins - user.coins_per_task > 0:
                user.coins = user.coins - user.coins_per_task

                ses.query(User).filter(User.chat_id == id).update({'coins': user.coins})
                ses.commit()
            else:

                ses.query(User).filter(User.chat_id == id).update({'coins': 0})
                ses.commit()

            return 'Неправильно 😡'


def generate_numbers(id):
    c = randint(1, 10)
    d = randint(1, 10)
    users = ses.query(User).filter(User.chat_id == id).all()
    for user in users:
        user.start_time = time.time()

    ses.query(User).filter(User.chat_id == id).update({'start_time': user.start_time})
    ses.commit()

    return c, d


def get_total_coins(id):
    users = ses.query(User).filter(User.chat_id == id).all()
    for user in users:
        return 'Монет : ' + str(user.coins) + '💵'


def start(update,context):
    update.message.reply_text(
        "Привіт! \nЦей бот був створений для людей, які хочуть тренувати свої математичні навички. У цьому боті ви побачите 5 кнопок +, -, *, /, √. Наразі розблоковано лише + епізод, але згодом ви можете збирати гроші з епізод і купити ще один епізод. Всього ви можете придбати 4 епізоди. Якщо ви хочете зупинити один з навчальних розділів, просто напишіть stop")
    update.message.reply_text('Оберіть варіант', reply_markup=reply_markup)

    chat_id = update.message.from_user.id
    username = update.message.from_user.username
    minus = False
    multiply = False
    divide = False
    sqrt = False
    degree = False
    coins = 0
    average_time = 0
    bought_section = 1
    stop_activated = False
    answer = 0
    start_time = time.time()
    want_to_buy = '  '
    shop_activate = False
    coins_per_task = 1
    completed_game = True
    now_symbol = " "

    res = ses.query(exists().where(User.chat_id == chat_id)).scalar()

    if res:
        print('User exists\n')
    else:
        user = User(username=username, minus=minus, multiply=multiply, divide=divide, coins=coins,
                    average_time=average_time, sqrt=sqrt,degree=degree, bought_section=bought_section,
                    chat_id=chat_id, stop_activated=stop_activated, answer=answer, start_time=start_time,
                    want_to_buy=want_to_buy, shop_active=shop_activate, coins_per_task=coins_per_task,
                    completed_game=completed_game, now_symbol=now_symbol)
        ses.add(user)
        print('User doesnt exist\n')

    ses.commit()


def help(update,context):
    update.message.reply_text(
        "Привіт! \nЦей бот був створений для людей, які хочуть тренувати свої математичні навички. У цьому боті ви побачите 5 кнопок +, -, *, /, √,^. Наразі розблоковано лише + епізод, але згодом ви можете збирати гроші з епізод і купити ще один епізод. Всього ви можете придбати 4 епізоди. Якщо ви хочете зупинити один з навчальних розділів, просто напишіть stop")


def is_game_completed(id):
    users = ses.query(User).filter(User.chat_id == id).all()
    for user in users:
        if user.bought_section == total_episodes:
            return True
        else:
            return False


def blocked_text(x):
    return '🚫 Заблоковано. Ви не можете його придбати, вам потрібно заробити {} монет, щоб придбати його'.format(x)


def keyboard_for_shop(x, id):
    if x == 2:
        ses.query(User).filter(User.chat_id == id).update({'want_to_buy': b})
    if x == 5:
        ses.query(User).filter(User.chat_id == id).update({'want_to_buy': c})
    if x == 10:
        ses.query(User).filter(User.chat_id == id).update({'want_to_buy': d})
    if x == 15:
        ses.query(User).filter(User.chat_id == id).update({'want_to_buy': e})
    if x == 20:
        ses.query(User).filter(User.chat_id == id).update({'want_to_buy': g})

    ses.commit()

    ses.query(User).filter(User.chat_id == id).update({'shop_active': True})
    ses.commit()

    text = "Його ви можете придбати,  напишіть yes/no (Ціна :{}💵)".format(x)
    text = text + '\nОберіть варіант:'
    custom_keyboard = [['yes'], ['no']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    return text, reply_markup


def shop(text, id):
    users = ses.query(User).filter(User.chat_id == id).all()
    for user in users:
        if str(text).lower() == 'yes':

            user.bought_section = user.bought_section + 1

            ses.query(User).filter(User.chat_id == id).update({'bought_section': user.bought_section})
            ses.commit()

            ses.query(User).filter(User.chat_id == id).update({'shop_active': False})
            ses.commit()

            if user.want_to_buy == b:
                ses.query(User).filter(User.chat_id == id).update({'minus': True})
                ses.commit()
                return "🤟Ви успішно розблокували етап мінус🤟"

            elif user.want_to_buy == c:
                ses.query(User).filter(User.chat_id == id).update({'multiply': True})
                ses.commit()
                return "🤟Ви успішно розблокували етап множення🤟"

            elif user.want_to_buy == d:
                ses.query(User).filter(User.chat_id == id).update({'divide': True})
                ses.commit()
                return "🤟Ви успішно розблокували етап ділення🤟"

            elif user.want_to_buy == e:
                ses.query(User).filter(User.chat_id == id).update({'sqrt': True})
                ses.commit()
                return "🤟Ви успішно розблокували етап виведення числа з-під кореня 🤟"

            elif user.want_to_buy == g:
                ses.query(User).filter(User.chat_id == id).update({'degree': True})
                ses.commit()
                return "🤟Ви успішно розблокували етап зведення числа в степінь🤟"

        elif str(text).lower() == 'no':
            ses.query(User).filter(User.chat_id == id).update({'shop_active': False})
            ses.commit()
            return 'Це ваш вибір'

        return 'Я не зрозумів. Напишіть ще раз '


def echo(update,context):
    users = ses.query(User).filter(User.chat_id == update.message.from_user.id).all()
    for user in users:

        if not user.stop_activated:

            if user.shop_active:
                update.message.reply_text(shop(update.message.text, update.message.from_user.id))

            if is_game_completed(update.message.from_user.id) and user.completed_game:
                ses.query(User).filter(User.chat_id == update.message.from_user.id).update({'completed_game': False})
                ses.commit()
                update.message.reply_text(
                    "😇Ви успішно закінчили гру, тепер ви можете збирати  і далі гроші і тренувати свій мозок, щоб отримати кращі оцінки в школі😇")

            # plus
            if update.message.text == a:
                user.now_symbol = a

                ses.query(User).filter(User.chat_id == update.message.from_user.id).update({'now_symbol': user.now_symbol})
                ses.commit()

                ses.query(User).filter(User.chat_id == update.message.from_user.id).update({'stop_activated': True})
                ses.commit()

                update.message.reply_text(generator_for_examples(1, update.message.from_user.id))

            # minus
            elif update.message.text == b:
                #Havent bought and you have enough money to buy it
                if user.coins >= 2 and user.minus == False:

                    text, text1 = keyboard_for_shop(2, update.message.from_user.id)

                    update.message.reply_text(text, reply_markup=text1)
                # If you bought it
                elif user.minus:
                    user.now_symbol = b

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'now_symbol': user.now_symbol})
                    ses.commit()

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'stop_activated': True})
                    ses.commit()

                    update.message.reply_text(generator_for_examples(2, update.message.from_user.id))
                else:
                    update.message.reply_text(blocked_text(2))

            # multiply
            elif update.message.text == c:
                if user.coins >= 5 and user.multiply == False:

                    text, text1 = keyboard_for_shop(5, update.message.from_user.id)
                    update.message.reply_text(text, reply_markup=text1)

                elif user.multiply:
                    user.now_symbol = c

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'now_symbol': user.now_symbol})
                    ses.commit()

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'stop_activated': True})
                    ses.commit()

                    update.message.reply_text(generator_for_examples(3, update.message.from_user.id))
                else:
                    update.message.reply_text(blocked_text(5))

            # divide
            elif update.message.text == d:
                if user.coins >= 10 and user.divide == False:

                    text, text1 = keyboard_for_shop(10, update.message.from_user.id)
                    update.message.reply_text(text, reply_markup=text1)

                elif user.divide:
                    user.now_symbol = d

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'now_symbol': user.now_symbol})
                    ses.commit()

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'stop_activated': True})
                    ses.commit()

                    update.message.reply_text(generator_for_examples(4, update.message.from_user.id))

                else:
                    update.message.reply_text(blocked_text(10))

            # sqrt
            elif update.message.text == e:
                if user.coins >= 15 and user.sqrt == False:

                    text, text1 = keyboard_for_shop(15, update.message.from_user.id)
                    update.message.reply_text(text, reply_markup=text1)

                elif user.sqrt:
                    user.now_symbol = e

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'now_symbol': user.now_symbol})
                    ses.commit()

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'stop_activated': True})
                    ses.commit()

                    update.message.reply_text(generator_for_examples(5, update.message.from_user.id))

                else:
                    update.message.reply_text(blocked_text(15))

            elif update.message.text == g:
                if user.coins >= 20 and user.degree == False:

                    text, text1 = keyboard_for_shop(20, update.message.from_user.id)
                    update.message.reply_text(text, reply_markup=text1)

                elif user.degree:
                    user.now_symbol = g

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'now_symbol': user.now_symbol})
                    ses.commit()

                    ses.query(User).filter(User.chat_id == update.message.from_user.id).update(
                        {'stop_activated': True})
                    ses.commit()

                    update.message.reply_text(generator_for_examples(6, update.message.from_user.id))

                else:
                    update.message.reply_text(blocked_text(20))

            else:
                update.message.reply_text('Оберіть варіант:', reply_markup=reply_markup)

        else:
            if (str(update.message.text)).lower() == 'stop':

                sum_of_all_time_solving = 0
                all_time_solve = []

                for i in read_text(user.chat_id):
                    all_time_solve.append(float(i))

                for i in all_time_solve:
                    sum_of_all_time_solving = sum_of_all_time_solving + i

                user.average_time = sum_of_all_time_solving / len(all_time_solve)
                update.message.reply_text('Ваш середній час : {}{}'.format(round(user.average_time, 2), '🕦'))

                ses.query(User).filter(User.chat_id == update.message.from_user.id).update({'stop_activated': False})
                ses.commit()

                all_time_solve.clear()

                update.message.reply_text(get_total_coins(update.message.from_user.id))

            else:

                update.message.reply_text(check_answer(update.message.text, update.message.from_user.id))
                update.message.reply_text(get_total_coins(update.message.from_user.id))

                if user.now_symbol == a:
                    update.message.reply_text(generator_for_examples(1, update.message.from_user.id))
                elif user.now_symbol == b:
                    update.message.reply_text(generator_for_examples(2, update.message.from_user.id))
                elif user.now_symbol == c:
                    update.message.reply_text(generator_for_examples(3, update.message.from_user.id))
                elif user.now_symbol == d:
                    update.message.reply_text(generator_for_examples(4, update.message.from_user.id))
                elif user.now_symbol == e:
                    update.message.reply_text(generator_for_examples(5, update.message.from_user.id))
                elif user.now_symbol == g:
                    update.message.reply_text(generator_for_examples(6, update.message.from_user.id))


def main():
    updater = Updater("TOKEN", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

