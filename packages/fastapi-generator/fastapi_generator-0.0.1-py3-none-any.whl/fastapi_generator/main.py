from pathlib import Path

import plac


def gen_main_app():
    root_dir = Path('app')
    if not root_dir.exists():
        root_dir.mkdir()
    Path('app', 'main.py').touch()


if __name__ == '__main__':
    plac.call(gen_main_app)
