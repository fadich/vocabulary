
class Word(object):

    def __init__(self, source: str, language: str, translations: dict,
                 attempts: int = 3, value: int = 3, score: int = 0):
        self.source = source
        self.language = language
        self.translations = {lang: set(items) for lang, items in translations.items()}
        self.attempts = attempts
        self.value = value
        self.score = score

    def to_dict(self):
        return {
            'source': self.source,
            'language': self.language,
            'translations': {lang: list(items) for lang, items in self.translations.items()},
            'value': self.value,
            'score': self.score,
        }

    def __str__(self):
        return f'{self.language}__{self.source}'

    @property
    def is_learnt(self):
        return self.score >= self.value
