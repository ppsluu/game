import json  # стандартная библиотека питона для работы с JSON (сохранение/загрузка как просили)


class P:
    # Класс игрока: хранит все характеристики и умеет сохраняться в файл

    def __init__(self, n):
        # Создаём нового игрока с базовыми параметрами
        self.n = n              # имя игрока (логин из меню)
        self.lvl = 1            # уровень
        self.hp = 70            # текущее здоровье
        self.max_hp = 60        # максимум здоровья
        self.mana = 50
        self.max_mana = 50
        self.art = []           # список названий артефактов
        self.prog = 0           # прогресс внутри выбранной ветки сюжета
        self.branch = 0         # текущая ветка (0 — в меню, 1/2/3 — лес/город/подземелье)
        self.saved = False      # флаг: сохранён ли прогресс игрока
        
    def add_art(self, a):
        # Добавить игроку артефакт и немного усилить его хп и ману)
        self.art.append(a)
        self.max_hp += 5
        self.hp = min(self.max_hp, self.hp + 5)
        self.max_mana += 5
        self.mana = min(self.max_mana, self.mana + 5)
        print(f"Получен артефакт: {a}")
        print(f"=== ДОСТИЖЕНИЕ! Найден артефакт «{a}» ===")
        
        
    def to_dict(self):
        # Преобразовать объект игрока в словарь для сохранения в JSON
        return {
            'n': self.n,
            'lvl': self.lvl,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'art': self.art,
            'prog': self.prog,
            'branch': self.branch
        }
    
    def from_dict(self, d):
        # Заполнить поля игрока из словаря (после загрузки из JSON)
        self.n = d['n']
        self.lvl = d['lvl']
        self.hp = d['hp']
        self.max_hp = d['max_hp']
        # Чтобы не ломать старые сохранения, берём значения через get с дефолтом
        self.mana = d.get('mana', 50)
        self.max_mana = d.get('max_mana', 50)
        self.art = d['art']
        self.prog = d['prog']
        self.branch = d['branch']
        
    def save(self, fname):
        # Сохранить текущее состояние игрока в JSON-файл
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)
        self.saved = True
        print(f"Сохранено: {fname}")
        
    def load(self, fname):
        # Загрузить состояние игрока из JSON-файла
        with open(fname, 'r', encoding='utf-8') as f:
            d = json.load(f)
        self.from_dict(d)
        self.saved = True
        print(f"Загружено: {fname}")

