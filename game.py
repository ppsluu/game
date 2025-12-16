import os
import random
from player import P
from artifacts import ABox


def mini_battle(p, enemy_name="монстр", enemy_hp=30):
    print("\nМИНИ-БОЙ")
    print(f"На твоем пути {enemy_name}!")
    print(f"Ты: Ну привет, {enemy_name}...")
    print(f"{enemy_name}: Я тебя не боюсь!")
    print(f"Твой уровень: {p.lvl}, HP: {p.hp}/{p.max_hp}")
    print(f"HP врага: {enemy_hp}")

    while enemy_hp > 0 and p.hp > 0:
        print("\nТвои действия:")
        print("1. Атаковать")
        print("2. Защищаться")
        print("3. Подлечиться")
        choice = input("Выбор: ")

        if choice == '1':
            dmg = random.randint(5, 10) + p.lvl
            enemy_hp -= dmg
            print(f"Ты ударил {enemy_name} и нанес {dmg} урона!")
        elif choice == '2':
            print("Ты попытался защититься и приготовился к удару.")
        elif choice == '3':
            heal = random.randint(12, 20)
            old_hp = p.hp
            p.hp = min(p.max_hp, p.hp + heal)
            print(f"Ты лечишься сильнее: было {old_hp} HP, стало {p.hp} HP.")
        else:
            print("Ты думаешь и теряешь инициативу...")

        if enemy_hp <= 0:
            break


        enemy_dmg = random.randint(6, 14)
        if choice == '2':
            enemy_dmg //= 2
        p.hp -= enemy_dmg
        print(f"{enemy_name} атакует и наносит тебе {enemy_dmg} урона!")
        print(f"Твой HP: {p.hp}/{p.max_hp}, HP врага: {enemy_hp}")

    if p.hp <= 0:
        print("\nТы пал в бою...")
        print("Тебя оттаскивают в безопасное место, но силы на исходе.")
        # редкий штраф: шанс потерять один случайный артефакт
        if p.art and random.random() < 0.3:
            lost = random.choice(p.art)
            p.art.remove(lost)
            print(f"В суматохе ты потерял артефакт «{lost}».")
        p.hp = max(10, p.max_hp // 4)
        p.branch = 0
        p.prog = 0
        return False

    print(f"\nТы победил {enemy_name}!")
    p.lvl += 1
    p.max_hp += 3
    p.hp = min(p.max_hp, p.hp + 10)
    print(f"Ты повысил уровень до {p.lvl}! Максимальное HP: {p.max_hp}, текущее HP: {p.hp}")
    return True

def reg():
    login = input("Логин: ")
    if os.path.exists('users.txt'):
        with open('users.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2 and parts[0] == login:
                    print("Логин занят!")
                    return None
    pwd = input("Пароль: ")
    with open('users.txt', 'a', encoding='utf-8') as f:
        f.write(f"{login}:{pwd}\n")
    print("Регистрация успешна!")
    return login

def auth():
    login = input("Логин: ")
    pwd = input("Пароль: ")
    if os.path.exists('users.txt'):
        with open('users.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2 and parts[0] == login and parts[1] == pwd:
                    print("Вход успешен!")
                    return login
    print("Неверный логин/пароль!")
    return None

def main_menu():
    print("\nГЛАВНОЕ МЕНЮ")
    print("1. Регистрация")
    print("2. Вход")
    print("3. Выход")
    ch = input("Выбор: ")
    return ch

def branch_1(p, ab):
    print("\nЛЕС")
    if p.prog == 0:
        print("Ты в темном-темном лесу. Видишь дорогу налево и направо.")
        print("Ты: Куда пойти? ВЫБЕРИ: лево или право...")
        print("1. Идти налево")
        print("2. Идти направо")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 1
            print("Нашел старый меч! Но на пути к нему враг...")
            print("Детпул: Отдай меч, я честно его украл!")
            print("Ты: Нет, он пригодится мне на экзамене по информатике!")
            if not mini_battle(p, "Детпул", 35):
                return
            art = ab.take('меч')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 2
            print("Нашел ключ! Но сначала нужно отбиться от стражника...")
            print("Док Стрендж: Ключ только для избранных.")
            print("Ты: Сейчас проверим, кто тут избранный!")
            if not mini_battle(p, "Док Стрендж", 30):
                return
            art = ab.take('ключ')
            if art:
                p.add_art(art)
    elif p.prog == 1:
        print("Ты уже на левой тропе. Впереди пещера.")
        print("Ты: Там темно... но, может, там сокровища.")
        print("1. Зайти в пещеру")
        print("2. Обойти пещеру")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 3
            print("В пещере прячется чудовище, охраняющее щит!")
            print("Таннос: Никто не берет мой щит!")
            print("Ты: Я только посмотрю... и заберу.")
            if not mini_battle(p, "Таннос", 45):
                return
            art = ab.take('щит')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 4
            print("Обойдя пещеру, ты избежал боя и нашел книгу!")
            print("Ты: Круто, и драться не пришлось.")
            art = ab.take('книга')
            if art:
                p.add_art(art)
    elif p.prog == 2:
        print("Ты на правой тропе. Видишь мост через реку.")
        print("Ты: Мост выглядит не очень надежно...")
        print("1. Перейти мост")
        print("2. Идти вдоль реки")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 5
            print("На мосту тебя поджидает Аллая Ведьма!")
            print("Аллая ведьма: Плата за проход — твоя жизнь.")
            print("Ты: Моя жизнь мне дороже, сама плати своей.")
            if not mini_battle(p, "Аллая Ведьма", 40):
                return
            print("Перешел мост, нашел лук!")
            art = ab.take('лук')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 6
            print("Шел вдоль реки, нашел кольцо!")
            print("Ты: Маленькое кольцо, а выглядит важным.")
            art = ab.take('кольцо')
            if art:
                p.add_art(art)
    else:
        print("Ветка завершена! Возврат в меню.")
        p.branch = 0
        p.prog = 0

def branch_2(p, ab):
    print("\nГОРОД")
    if p.prog == 0:
        print("Ты в большом городе. Куда пойдешь?")
        print("Ты: Столько людей... даже немного страшно.")
        print("1. В таверну")
        print("2. На рынок")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 1
            print("В таверне на тебя нападает пьяный студент!")
            print("Маёвец: Эй, ты чё такой умный?")
            print("Ты: Я просто хочу посидеть.")
            if not mini_battle(p, "пьяный студент", 30):
                return
            print("После драки ты забрал его стипендию и получил посох!")
            art = ab.take('посох')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 2
            print("На рынке тебя пытаются ограбить!")
            print("Коллекторы: Ой, как у тебя много карманов.")
            print("Ты: А у вас сейчас будет много проблем!")
            if not mini_battle(p, "Коллекторы", 25):
                return
            print("Отбившись, ты выгодно купил копье на неворованные деньги!")
            art = ab.take('копье')
            if art:
                p.add_art(art)
    elif p.prog == 1:
        print("Ты в таверне. Что дальше?")
        print("Ты: Может, Лексус что-то знает.")
        print("1. Поговорить с Лексусом")
        print("2. Пойти в подвал")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 3
            print("Лексус соглашается помочь, но сначала просит выгнать дебошира.")
            print("Лексус: Выгони его, и я помогу.")
            print("Ты: Ладно, попробую.")
            if not mini_battle(p, "Прогульщик", 35):
                return
            print("Лексус благодарен и дает тебе лупу!")
            print("Лексус: Ты нормально дерешься, вот держи, пригодится.")
            art = ab.take('лупа')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 4
            print("В подвале ты сталкиваешься с Железным Человеком!")
            print("Железный Человек: Не мешай, я работаю!")
            print("Ты: А мне всё равно, скоро Новый год")
            if not mini_battle(p, "Железный человек", 40):
                return
            print("Победив его, ты находишь маску!")
            art = ab.take('маска')
            if art:
                p.add_art(art)
    elif p.prog == 2:
        print("Ты на рынке. Что делать?")
        print("Ты: Может, тут что-то ценное найдется.")
        print("1. Торговать")
        print("2. Искать редкие товары")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 5
            print("Контрагент оказывается жуликом, начинается потасовка!")
            print("Плохой парень: Я тебя обманул, и что?")
            print("Ты: Теперь будем честно — кулаками.")
            if not mini_battle(p, "Плохой парень", 35):
                return
            print("Удачно продал и получил кольцо!")
            art = ab.take('кольцо')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 6
            print("Охранник общаги не пускает тебя к редким товарам!")
            print("Охранник общаги: Сюда нельзя.")
            print("Ты: Тогда мне очень туда нужно.")
            if not mini_battle(p, "Охранник общаги", 40):
                return
            print("После победы ты находишь редкую книгу!")
            art = ab.take('книга')
            if art:
                p.add_art(art)
    else:
        print("Ветка завершена! Возврат в меню.")
        p.branch = 0
        p.prog = 0

def branch_3(p, ab):
    print("\nПОДЗЕМЕЛЬЕ")
    if p.prog == 0:
        print("Ты спустился в подземелье. Две двери.")
        print("Ты: Не нравится мне это место.")
        print("1. Левая дверь")
        print("2. Правая дверь")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 1
            print("За левой дверью угорает Джокер!")
            print("Джокер: Никто не пройдет.")
            print("Ты: Я как раз собирался пройти.")
            if not mini_battle(p, "Джокер", 45):
                return
            print("В левой комнате нашел щит!")
            art = ab.take('щит')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 2
            print("За правой дверью поджидает Локи!")
            print("Локи: Новый гость, который разрушит тайм-лайн?.")
            print("Ты: Я без злых умыслов и по тебе сохну, но в игре надо драться, поэтому сорри.")
            if not mini_battle(p, "Локи", 50):
                return
            print("В правой комнате нашел ключ!")
            art = ab.take('ключ')
            if art:
                p.add_art(art)
    elif p.prog == 1:
        print("Ты в левой комнате. Дальше?")
        print("Ты: Впереди ещё темнее, но надо идти.")
        print("1. Идти глубже")
        print("2. Вернуться назад")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 3
            print("На пути глубже в подземелье тебя атакует Дарт Вейдер!")
            print("Дарт Вейдер: Ты здесь лишний, преклонись.")
            print("Ты: Это мы сейчас обсудим.")
            if not mini_battle(p, "Дарт Вейдер", 55):
                return
            print("Глубже нашел посох!")
            art = ab.take('посох')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 4
            print("По дороге назад на тебя нападает Воландеморт!")
            print("Воландеморт: Никто не уйдет.")
            print("Ты: Я очень постараюсь, авадакедавра!")
            if not mini_battle(p, "Воландеморт", 45):
                return
            print("Вернувшись, нашел копье!")
            art = ab.take('копье')
            if art:
                p.add_art(art)
    elif p.prog == 2:
        print("Ты в правой комнате. Что дальше?")
        print("Ты: Тут тихо, но это подозрительно.")
        print("1. Открыть сундук")
        print("2. Искать секрет")
        ch = input("Выбор: ")
        if ch == '1':
            p.prog = 5
            print("Сундук охраняет гоблин!")
            if not mini_battle(p, "гоблин", 50):
                return
            print("В сундуке нашел лупу!")
            art = ab.take('лупа')
            if art:
                p.add_art(art)
        elif ch == '2':
            p.prog = 6
            print("Пока ты ищешь секрет, на тебя нападает сессия!")
            if not mini_battle(p, "сессия", 55):
                return
            print("Нашел секретную дверь и маску!")
            art = ab.take('маска')
            if art:
                p.add_art(art)
    else:
        print("Ветка завершена! Возврат в меню.")
        p.branch = 0
        p.prog = 0

def game_loop(p, ab):
    while True:
        if p.branch == 0:
            print(f"\n=== ИГРА ===")
            print(f"Игрок: {p.n}")
            print(f"HP: {p.hp}/{p.max_hp}")
            print(f"Артефакты: {', '.join(p.art) if p.art else 'нет'}")
            print("\nВыбери ветку:")
            print("1. Лес")
            print("2. Город")
            print("3. Подземелье")
            print("4. Сохранить")
            print("5. Выход")
            ch = input("Выбор: ")
            if ch == '1':
                p.branch = 1
                p.prog = 0
                p.saved = False
            elif ch == '2':
                p.branch = 2
                p.prog = 0
                p.saved = False
            elif ch == '3':
                p.branch = 3
                p.prog = 0
                p.saved = False
            elif ch == '4':
                p.save(f"save_{p.n}.json")
                ab.save("artifacts.json")
            elif ch == '5':
                if not p.saved:
                    print("\nВНИМАНИЕ! Прогресс не сохранен!")
                    print("Все артефакты вернутся в копилку!")
                    ans = input("Выйти без сохранения? (да/нет): ")
                    if ans.lower().startswith('д'):
                        ab.return_art(p.art)
                        p.art = []
                        p.prog = 0
                        p.branch = 0
                        print("Прогресс сброшен, артефакты возвращены.")
                return
        elif p.branch == 1:
            branch_1(p, ab)
        elif p.branch == 2:
            branch_2(p, ab)
        elif p.branch == 3:
            branch_3(p, ab)
        
        if ab.is_empty():
            ab.gen_new()

def main():
    print("=== ИГРА ===")
    login = None
    while not login:
        ch = main_menu()
        if ch == '1':
            login = reg()
        elif ch == '2':
            login = auth()
        elif ch == '3':
            return
    
    p = P(login)
    ab = ABox()
    
    if os.path.exists(f"save_{login}.json"):
        ans = input("Найдено сохранение. Загрузить? (да/нет): ")
        if ans.lower().startswith('д'):
            p.load(f"save_{login}.json")
            ab.load("artifacts.json")
            p.saved = True
    
    game_loop(p, ab)
    
    if not p.saved:
        print("\nВНИМАНИЕ! Прогресс не сохранен!")
        ans = input("Сохранить перед выходом? (да/нет): ")
        if ans.lower().startswith('д'):
            p.save(f"save_{login}.json")
            ab.save("artifacts.json")
        else:
            ab.return_art(p.art)
            print("Артефакты возвращены в копилку.")

if __name__ == "__main__":
    main()

