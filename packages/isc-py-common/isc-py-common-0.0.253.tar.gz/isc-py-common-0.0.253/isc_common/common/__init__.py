import os
from typing import Text
from uuid import UUID


def getOrElse(default, value):
    if value:
        return value
    else:
        return default


black = "black"
blue = "blue"
closed = "closed"
create = "create"
deleted = "deleted"
doing = "doing"
formirovanie="formirovanie"
green = "green"
made = "made"
new = "new"
new_man = "new_man"
orange = "orange"
red = "red"
restarted = "restarted"
started = "started"
stoped = "stoped"
transferred = "transferred"
update = "update"
value_odd = "value_odd"

name_new="Новый"
name_new_s="Новый (с)"
name_new_h="Новый (р)"
name_started="Запущен"
name_restarted="Запущен (повторно)"
name_transferred="Назначенный"
name_stoped="Остановлен"
name_doing="Выполнен"
name_closed="Закрыт"
name_formirovanie="Формирование"
name_handmade="Системный (ручное формирование)"


def blinkString(text, blink=True, color="black", bold=False) -> Text:
    if blink:
        res = f'<div class="blink"><strong><font color="{color}"</font>{text}</strong></div>'
    else:
        res = f'<div><strong><font color="{color}"</font>{text}</strong></div>'

    if bold == True:
        return f'<b>{res}</b>'
    else:
        return res


def uuid5():
    return UUID(bytes=os.urandom(16), version=4)

def uuid4():
    return str(UUID(bytes=os.urandom(16), version=4)).upper().replace('-', '_')
