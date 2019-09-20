#!/usr/bin/env python3

import sys
import time
import random
import argparse

from vocabulary import ui
from vocabulary.dictionary import Dictionary


def learn(dictionary):
    unlearnt = dictionary.get_unlearnt()
    if not unlearnt:
        ui.writeln('Congratulations! All words are learnt!')
        return False

    word = unlearnt[random.choice(list(unlearnt.keys()))]

    ui.writeln()
    for lang in word.translations:
        attempt = 1
        options = word.translations[lang]

        while attempt <= word.attempts:
            translation = ui.read(f'{word.source} -> ({lang}) ')
            if translation in options:
                ui.writeln('CORRECT!')
                word.score += 1
                break

            ui.error(f'Incorrect. {word.attempts - attempt} attempts left')
            attempt += 1

        time.sleep(0.15)
        ui.writeln('{} - {}'.format(word.source, ', '.join(options)))

    dictionary[str(word)] = word

    ui.writeln()
    return True


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='set debug log level')
    args = parser.parse_args()

    dictionary = Dictionary.load_storage()

    try:
        while learn(dictionary):
            pass
    except KeyboardInterrupt:
        pass

    dictionary.save()

    return 0


if __name__ == '__main__':
    sys.exit(main())
