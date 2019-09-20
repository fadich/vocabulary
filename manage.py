#!/usr/bin/env python3

import sys
import argparse

from collections import defaultdict

from vocabulary import ui
from vocabulary import languages
from vocabulary.word import Word
from vocabulary.dictionary import Dictionary


def insert():
    def _insert():
        choices = {languages.LANG_DE, languages.LANG_RU}
        while True:
            source = ui.read('Word: ')
            language = ui.read_in(
                'language ({}): '.format(', '.join(choices)),
                choices=choices)

            translation = defaultdict(set)
            ui.writeln('Translations (press <Ctrl + C> to stop)')
            try:
                for lang in choices ^ {language}:
                    try:
                        while True:
                            ui.write(f'({lang})')
                            line = ui.read()
                            if line:
                                translation[lang].add(line)
                    except KeyboardInterrupt:
                        ui.writeln('\r')
            except KeyboardInterrupt:
                ui.writeln('\r')

            value = ui.read_number('Value: ')
            ui.writeln()

            yield Word(
                source=source,
                language=language,
                translations=translation,
                value=value)

    try:
        dictionary = Dictionary.load_storage()
    except ValueError as e:
        ui.error(e)
        return -1

    try:
        for word in _insert():
            dictionary[str(word)] = word
    except KeyboardInterrupt:
        pass

    ui.writeln('Saving. Please wait...')
    dictionary.save()

    return 0


def delete():
    try:
        dictionary = Dictionary.load_storage()
    except ValueError as e:
        ui.error(e)
        return -1

    choices = {languages.LANG_DE, languages.LANG_RU}
    try:
        while True:
            source = ui.read('Word: ')
            language = ui.read_in(
                'language ({}): '.format(', '.join(choices)),
                choices=choices)
            word = Word(source, language, {})
            key = str(word)
            if key not in dictionary:
                ui.error(f'`{key}` does not exist')
                continue

            del dictionary[key]
    except KeyboardInterrupt:
        pass

    ui.writeln('Saving. Please wait...')
    dictionary.save()

    return 0


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('action', type=str, help='action in {insert,delete}')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='set debug log level')
    args = parser.parse_args()

    if args.action == 'insert':
        return insert()
    if args.action == 'delete':
        return delete()

    ui.error(f'No such action "{args.action}"')
    return -1


if __name__ == '__main__':
    sys.exit(main())
