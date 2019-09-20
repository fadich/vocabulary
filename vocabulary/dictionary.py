import os
import json

from vocabulary.word import Word


class Dictionary(dict):
    STORAGE_PATH = 'storage.json'

    def get_learnt(self):
        return self.__class__(**{k: w for k, w in self.items() if w.is_learnt})

    def get_unlearnt(self):
        return self.__class__(**{k: w for k, w in self.items() if not w.is_learnt})

    def save(self):
        data = {}
        for key, word in self.items():
            data[key] = word.to_dict()

        data = json.dumps(data)

        with open(self.STORAGE_PATH, 'w+') as f:
            f.write(data)

    @classmethod
    def load_storage(cls):
        if not os.path.exists(cls.STORAGE_PATH):
            return cls()
        if os.path.isdir(cls.STORAGE_PATH):
            raise ValueError(f'{cls.STORAGE_PATH} is directory')

        try:
            with open(cls.STORAGE_PATH, 'r') as f:
                words = json.loads(f.read())
        except json.JSONDecodeError:
            raise ValueError('Invalid storage content')

        return cls._from_json(words)

    @classmethod
    def _from_json(cls, words: dict):
        word_list = cls()
        for key, params in words.items():
            word_list[key] = Word(**params)

        return word_list
