#!./venv/bin/python


from engine import Engine


def main():
    engine = Engine((320, 640))
    engine.start()


if __name__ == '__main__':
    main()
