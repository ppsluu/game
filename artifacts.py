import json
import random

class ABox:
    def __init__(self):
        self.all = ['меч', 'щит', 'лук', 'книга', 'кольцо', 'посох', 'копье', 'лупа', 'ключ', 'маска']
        self.in_box = self.all.copy()
        
    def take(self, name):
        if name in self.in_box:
            self.in_box.remove(name)
            return name
        return None
        
    def return_art(self, arts):
        for a in arts:
            if a not in self.in_box:
                self.in_box.append(a)
        if len(self.in_box) >= len(self.all):
            self.gen_new()
            
    def gen_new(self):
        print("\n=== ГЕНЕРАЦИЯ НОВЫХ АРТЕФАКТОВ ===")
        new = ['клинок', 'броня', 'стрела', 'свиток', 'перстень', 'жезл', 'пика', 'очки', 'карта', 'плащ']
        self.all.extend(new)
        self.in_box = new.copy()
        print(f"Создано {len(new)} новых артефактов!")
        
    def get_random(self):
        if not self.in_box:
            self.gen_new()
        return random.choice(self.in_box) if self.in_box else None
        
    def save(self, fname):
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump({'all': self.all, 'in_box': self.in_box}, f, ensure_ascii=False)
            
    def load(self, fname):
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                d = json.load(f)
            self.all = d['all']
            self.in_box = d['in_box']
        except:
            pass
            
    def is_empty(self):
        # Проверяем, все ли артефакты у игроков
        collected = len([a for a in self.all if a not in self.in_box])
        return collected >= len(self.all)

