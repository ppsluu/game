import json   # для сохранения/загрузки артефактов в файл
import random # для случайного выбора артефактов

class ABox:
    """Коробка с артефактами.

    Хранит список всех возможных артов и те, которые ещё лежат в коробке.
    Игроки забирают артефакты отсюда и могут возвращать их обратно.
    """
    def __init__(self):
        # Базовый список артефактов в игре
        self.all = ['меч', 'щит', 'лук', 'книга', 'кольцо', 'посох', 'копье', 'лупа', 'ключ', 'маска']
        # Какие артефакты сейчас лежат в "коробке" и ещё не взяты игроками
        self.in_box = self.all.copy()
        
    def take(self, name):
        """Взять артефакт по имени из коробки (если он там есть)."""
        if name in self.in_box:
            self.in_box.remove(name)
            return name
        return None
        
    def return_art(self, arts):
        """Вернуть один или несколько артефактов обратно в коробку.

        Если все артефакты вернулись (коробка полная), генерируем новый набор.
        """
        for a in arts:
            if a not in self.in_box:
                self.in_box.append(a)
        if len(self.in_box) >= len(self.all):
            self.gen_new()
            
    def gen_new(self):
        """Сгенерировать новый набор артефактов, когда старые уже собрали."""
        print("\n=== ГЕНЕРАЦИЯ НОВЫХ АРТЕФАКТОВ ===")
        new = ['клинок', 'броня', 'стрела', 'свиток', 'перстень', 'жезл', 'пика', 'очки', 'карта', 'плащ']
        self.all.extend(new)
        self.in_box = new.copy()
        print(f"Создано {len(new)} новых артефактов!")
        
    def get_random(self):
        """Вернуть случайный артефакт из коробки.

        Если коробка пустая, сначала генерируем новые артефакты.
        """
        if not self.in_box:
            self.gen_new()
        return random.choice(self.in_box) if self.in_box else None
        
    def save(self, fname):
        """Сохранить состояние коробки артефактов в JSON-файл."""
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump({'all': self.all, 'in_box': self.in_box}, f, ensure_ascii=False)
            
    def load(self, fname):
        """Загрузить состояние коробки из JSON-файла.

        Если что-то пошло не так (файл битый/нет файла), просто игнорируем ошибку.
        """
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                d = json.load(f)
            self.all = d['all']
            self.in_box = d['in_box']
        except:
            pass
            
    def is_empty(self):
        """Проверить, разобрали ли игроки все доступные артефакты.

        Возвращает True, если каждый артефакт из списка all уже кем-то взят
        (то есть его нет в in_box).
        """
        # Считаем, сколько артов сейчас НЕ лежит в коробке
        collected = len([a for a in self.all if a not in self.in_box])
        return collected >= len(self.all)

