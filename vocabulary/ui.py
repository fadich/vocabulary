import sys
import typing

from traceback import format_exc


def write(line: str):
    sys.stdout.write(line)
    sys.stdout.flush()


def writeln(line=''):
    write(f'{line}\n')


def error(line=''):
    sys.stderr.write(f'{line}\n')
    sys.stderr.flush()


def read(prompt=None, reduce: bool = True) -> str:
    if prompt:
        writeln(prompt)

    sys.stdout.write(f' > ')
    sys.stdout.flush()

    line = None
    while line is None:
        try:
            line = sys.stdin.readline()
            sys.stdin.flush()
        except ValueError:
            error(format_exc())

    if reduce:
        line = line.strip().lower()

    return line


def read_valid(prompt: str = None, reduce: bool = True,
               err_msg: str = 'Not a number', attempts: int = -1,
               exit_msg: str = 'No attempt left', validate: typing.Callable = None):

    assert callable(validate)

    while True:
        if attempts == 0:
            raise KeyboardInterrupt(exit_msg)

        line = read(prompt=prompt, reduce=reduce)
        if validate(line):
            return line

        error(err_msg)
        attempts -= 1


def read_in(prompt: str = None, reduce: bool = True,
            err_msg: str = 'Invalid value', attempts: int = -1,
            exit_msg: str = 'No attempt left', choices: typing.Iterable = None):

    choices = set(choices) or {}
    if reduce:
        choices = list(map(lambda x: x.strip().lower(), choices))

    return read_valid(
        prompt=prompt,
        reduce=reduce,
        err_msg=err_msg,
        attempts=attempts,
        exit_msg=exit_msg,
        validate=lambda x: x in choices)


def read_number(prompt: str = None, reduce: bool = True,
                err_msg: str = 'Not a positive number', attempts: int = -1,
                exit_msg: str = 'No attempt left'):

    return int(
        read_valid(
            prompt=prompt,
            reduce=reduce,
            err_msg=err_msg,
            attempts=attempts,
            exit_msg=exit_msg,
            validate=lambda x: x.isdigit() and int(x) > 0))
