import json
from enum import Enum
from typing import List


class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Widget:
    def __init__(self, parent: 'Widget' = None):
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.add_children(self)

    def add_children(self, children: 'Widget'):
        self.children.append(children)

    def to_binary(self) -> dict:
        return {
            'class': self.__class__.__name__,
            'children': [child.to_binary() for child in self.children]
        }

    @classmethod
    def from_binary(cls, data: dict, parent: 'Widget' = None) -> 'Widget':
        widget_class = globals()[data['class']]
        widget = widget_class.from_binary(data=data, parent=parent)
        for child_data in data['children']:
            child = Widget.from_binary(data=child_data, parent=widget)
            child.parent = parent
        return widget

    def __str__(self):
        return f"{self.__class__.__name__}{self.children}"

    def __repr__(self):
        return str(self)


class MainWindow(Widget):
    def __init__(self, title: str):
        super().__init__(None)
        self.title = title

    def to_binary(self) -> dict:
        data = super().to_binary()
        data.update({'title': self.title})
        return data

    @classmethod
    def from_binary(cls, data: dict, parent: 'Widget' = None) -> 'MainWindow':
        title = data.pop('title')
        return cls(title=title)


class Layout(Widget):
    def __init__(self, parent: Widget, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment

    def to_binary(self) -> dict:
        data = super().to_binary()
        data.update({'alignment': self.alignment.name})
        return data

    @classmethod
    def from_binary(cls, data: dict, parent: 'Widget' = None) -> 'Layout':
        alignment = Alignment[data.pop('alignment')]
        return cls(parent=parent, alignment=alignment)


class LineEdit(Widget):
    def __init__(self, parent: Widget, max_length: int = 10):
        super().__init__(parent)
        self.max_length = max_length

    def to_binary(self) -> dict:
        data = super().to_binary()
        data.update({'max_length': self.max_length})
        return data

    @classmethod
    def from_binary(cls, data: dict, parent: 'Widget' = None) -> 'LineEdit':
        max_length = data.pop('max_length', 10)
        return cls(parent=parent, max_length=max_length)


class ComboBox(Widget):
    def __init__(self, parent: Widget, items: List):
        super().__init__(parent)
        self.items = items

    def to_binary(self) -> dict:
        data = super().to_binary()
        data.update({'items': self.items})
        return data

    @classmethod
    def from_binary(cls, data: dict, parent: 'Widget' = None) -> 'ComboBox':
        items = data.pop('items', [])
        return cls(parent=parent, items=items)


app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

box1 = ComboBox(layout2, [1, 2, 3, 4])
box2 = ComboBox(layout2, ["a", "b", "c"])

print(app)

bts = json.dumps(app.to_binary())
print(f"Binary data length {len(bts)}")
print(f"Binary data \n {bts}")

new_app = Widget.from_binary(json.loads(bts))
print(new_app)
