kv = '''
#:import NoTransition kivy.uix.screenmanager.NoTransition
ScreenManager:
    transition: NoTransition()
    Screen:
        name: 'list'
        BoxLayout:
            orientation: 'vertical'

            BoxLayout:
                padding: dp(10)
                size_hint_y: None
                height: dp(55)
                canvas.before:
                    Color:
                        rgb: .3, .3, .3
                    Rectangle:
                        size: self.size
                        pos: self.pos
                Label:
                    id: log
                    text: 'KivyLog'
                    bold: True
                    halign: 'left'

            RecycleList:
                id: logs
                viewclass: 'LogBar'
                cols: 1
                default_height: dp(60)
                size_hint_y: .8
        
        Label:
            text: 'No logs' if not root.ids.logs.data else ''
            font_size: dp(15)
            color: 1, 1, 1, 1   


    Screen:
        name: 'log'
        BoxLayout:
            orientation: 'vertical'

            BoxLayout:
                padding: dp(10)
                size_hint_y: None
                height: dp(55)
                canvas.before:
                    Color:
                        rgb: .3, .3, .3
                    Rectangle:
                        size: self.size
                        pos: self.pos
                Button:
                    text: 'Back'
                    font_size: dp(12)
                    size_hint_x: None
                    width: dp(40)
                    color: .8, .8, .8, 1
                    background_color: 0, 0, 0, 0
                    on_release: app.root.current = 'list'

                Label:
                    id: log
                    text: 'log'
                    bold: True
                    halign: 'left'

            ScrollView:
                BoxLayout:
                    size_hint: .9, None
                    pos_hint: {'center_x': .5}
                    orientation: 'vertical'
                    padding: dp(5)
                    height: self.minimum_height

                    Label:
                        id: log_text
                        text: ''
                        color: 1, 1, 1, 1
                        font_size: dp(13)
                        text_size: self.width, None
                        size_hint: 1, None
                        markup: True
                        halign: 'left'
                        height: self.texture_size[1]


<Bar@BoxLayout>:
    file: ""
    padding: dp(10)
    Label:
        text: root.file
        halign: 'right'
        color: 1, 1, 1, 1

<LogBar@ButtonBehavior+Bar>:
    on_release: app.show_log(root.file)


<RecycleList@RecycleView>:
    viewclass: "LogBar"
    default_height: dp(110)
    RecycleBoxLayout:
        spacing: 30
        padding: 20
        orientation: 'vertical'
        default_size: 0, root.default_height
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height


'''