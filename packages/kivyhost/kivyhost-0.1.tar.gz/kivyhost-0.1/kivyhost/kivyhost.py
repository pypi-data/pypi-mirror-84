import os
from pickle import dumps, loads


def check_host_log(force: bool = False) -> bool:
    if not os.path.exists('host.log') or force:
        with open(f'{os.getcwd()}/host.log', 'wb') as file:
            file.write(dumps({'show_log': True}))
        return False
    else:
        try:
            # reading file
            with open(f'{os.getcwd()}/host.log', 'rb') as file:
                data = loads(file.read())

            # forcing to show logs if kivy app doesnt end properly
            check_host_log(force=True)

            # returning launch status
            return data['show_log']

        except KeyError:
            check_host_log(force=True)


def end():
    with open(f'{os.getcwd()}/host.log', 'rb') as file:
        data = loads(file.read())

    data['show_log'] = False

    with open(f'{os.getcwd()}/host.log', 'wb') as file:
        file.write(dumps(data))

    exit()


def printout(log: any):
    from kivy.logger import Logger

    Logger.info(str(log))


if check_host_log():
    # kivy imports
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.core.window import Window

    # layout import
    from kivyhost.layout import kv

    class KivyHost(App):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Window.bind(on_close=self.closing)
            Window.bind(on_keyboard=self.keyboard)

        def build(self):
            self.root = Builder.load_string(kv)

            try:
                logs = os.listdir(f'{os.getcwd()}/.kivy/logs')
            except:
                logs = []

            logs = [{'file': item} for item in logs][:-1]

            self.root.ids.logs.data = logs

        def list_view(self):
            self.root.current = 'list'

        def show_log(self, file: str):
            self.root.current = 'log'

            with open(f'{os.getcwd()}/.kivy/logs/{file}', 'r') as file_object:
                log = file_object.read()

            self.root.ids.log.text = file
            self.root.ids.log_text.text = log

        @staticmethod
        def closing(*_):
            end()

        def keyboard(self, *args):
            if args[1] == 27:
                if self.root.current == 'log':
                    self.root.current = 'list'
                else:
                    end()
            return True

    KivyHost().run()
