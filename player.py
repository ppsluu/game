import json

class P:
    def __init__(self, n):
        self.n = n  #имя
        self.lvl = 1  #уровень
        self.hp = 70        #немного меньше начального HP
        self.max_hp = 70
        self.art = []  #артефакты
        self.prog = 0  #прогресс ветки
        self.branch = 0  #текущая ветка (0-нет, 1-2-3 линии)
        self.saved = False  #сохранен ли
        
    def add_art(self, a):
        self.art.append(a)
        self.max_hp += 5
        self.hp = min(self.max_hp, self.hp + 5)
        print(f"Получен артефакт: {a}")
        print(f"=== ДОСТИЖЕНИЕ! Найден артефакт «{a}» ===")
        
    def to_dict(self):
        return {
            'n': self.n,
            'lvl': self.lvl,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'art': self.art,
            'prog': self.prog,
            'branch': self.branch
        }
    
    def from_dict(self, d):
        self.n = d['n']
        self.lvl = d['lvl']
        self.hp = d['hp']
        self.max_hp = d['max_hp']
        self.art = d['art']
        self.prog = d['prog']
        self.branch = d['branch']
        
    def save(self, fname):
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)
        self.saved = True
        print(f"Сохранено: {fname}")
        
    def load(self, fname):
        with open(fname, 'r', encoding='utf-8') as f:
            d = json.load(f)
        self.from_dict(d)
        self.saved = True
        print(f"Загружено: {fname}")

