def file_generation(topic, number):
    return f'questions/{topic}_{number}.png'


def check_result(res):
    math = res['math']
    human = res['humanitarian']
    if math == human and math == 5:
        text = 'Поздравляю! 🎆 Ты ответил_а правильно на ВСЕ вопросы! Это значит что тебе под силу как математические, '\
               'так и гуманитарные науки'
        photo = 'results/best.jpg'
    elif 2 <= math <= 4 and math == human:
        text = f'Поздравляю, ты верно ответил_а на {math} вопроса по математике и на столько же по гуманитарным ' \
               f'наукам 🔥 Это значит, что сейчас нельзя определить, что у тебя получается лучше. Можешь пройти тест ' \
               f'ещё раз. А вот верные ответы: {right_answers}'
        photo = 'results/math-humanitarian.jpg'
    elif math == human and math == 1:
        text = f'Ты ответил_а на 1 вопрос по математике, и на 1 по гуманитарным наукам, поэтому сейчас нельзя ' \
               f'определить, что у тебя получается лучше 🤷‍♀ Пока что постарайся повторить пройденное, и тогда твой ' \
               f'результат улучшится! А вот верные ответы: {right_answers}'
        photo = 'results/math-humanitarian.jpg'
    elif math > human:
        if max(math, human) < 3:
            text = f'Так, твои верные ответы: по математике - {math}, по гуманитарным наукам - {human}, а значит, ' \
                   f'тебе больше подойдёт математический класс 📐 Но постарайся подтянуть знания по школьной ' \
                   f'программе. А вот верные ответы: {right_answers}'
            photo = 'results/math.jpg'
        else:
            text = f'Итак, твои верные ответы: по математике - {math}, по гуманитарным наукам - {human}, а значит ,' \
                   f'тебе больше подойдёт математический класс 📐 А вот верные ответы: {right_answers}'
            photo = 'results/math.jpg'
    elif math < human:
        if max(math, human) < 3:
            text = f'Так, твои верные ответы: по математике - {math}, по гуманитарным наукам - {human}, а значит, ' \
                   f'тебе больше подойдёт гуманитарный класс 🎨 Но постарайся подтянуть знания по школьной программе. ' \
                   f'А вот верные ответы: {right_answers}'
            photo = 'results/humanitarian.jpg'
        else:
            text = f'Итак, твои верные ответы: по математике - {math}, по гуманитарным наукам - {human}, а значит, ' \
                   f'тебе больше подойдёт гуманитарный класс 🎨 А вот верные ответы: {right_answers}'
            photo = 'results/humanitarian.jpg'
    else:
        text = 'Ой... Ты не ответил правильно ни на один вопрос 😢 Похоже, тебе следует подтянуть школьные знания'
        photo = 'results/nothing.jpg'
    return text, photo


questions = {'Математика': {'topic': 'math',
                            'answers': [['130', '110', '90', '120', 1],
                                        ['22', '20', '24', '23', 0],
                                        ['15', '20', '25', '30', 2],
                                        ['5', '4', '6', '3', 0],
                                        ['3', '2', '5', '4', 3]]},
             'Гуманитарные науки': {'topic': 'humanitarian',
                                    'answers': [['23', '13', '14', '24', 2],
                                                ['А3\nБ2', 'А1\nБ3', 'А2\nБ1', 'А3\nБ1', 0],
                                                ['А', 'Б', 'В', 'Никакой', 1],
                                                ['Понедельник', 'Вторник', 'Четверг', 'Воскресенье', 2],
                                                ['А - Австралия\nБ - Евразия', 'А - Южная Америка\nБ - Африка',
                                                 'А - Антарктида\nБ - Северная Америка',
                                                 'А - Австралия\nБ - Северная Америка', 3]]}}
start_message = 'Привет! 😉 Если ты учишься в 4 классе - этот бот точно для тебя! Здесь можно пройти небольшой тест и ' \
                'узнать, в каком классе тебе будет лучше учится в 5 классе - в математическом или в гуманитарном. ' \
                'Жми /help чтобы узнать, как здесь всё работает!'
help_message = 'Вот список команд, с помощью которых ты можешь общаться с ботом:\n/start - выведет приветственное ' \
               'сообщение 🖐\n/help - отправит сообщение, которое ты сейчас читаешь 📖\n/starttest - запустит ' \
               'прохождение теста 📋\n❗ Если во время прохождения теста запустить одну из команд, тест придётся ' \
               'начинать сначала\nПожалуйста, общайся с ботом только с помощью команд 🙏'
right_answers = ''
for key in questions.keys():
    l = questions[key]['answers']
    for i in range(len(l)):
        right_answers = right_answers + '\n' + l[i][l[i][4]]
users = {}
