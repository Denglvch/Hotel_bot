prices = {
    '/lowprice': {'max': 100,
                  'min': 1},
    '/highprice': {'max': 9999,
                   'min': 100},
}

ru_steps = {
    'year': 'год',
    'month': 'месяц',
    'day': 'день'
}

text_command = {
    'lowprice': 'Самые низкие цены',
    'highprice': 'Самые высокие цены',
    'bestdeal': 'Лучшие цены по расположению'
}

messages: dict[int: list[int]] = dict()
