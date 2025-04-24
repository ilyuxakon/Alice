from flask import Flask, request, jsonify
import os
import logging


app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='example.log')

sessionStorage = dict()


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response: {response!r}')

    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                'Не хочу',
                'Не буду',
                'Отстань'
            ],
            'stage': 0
        }

        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    answers = ['ладно', 'куплю', 'покупаю', 'хорошо', 'я покупаю', 'я куплю']

    if req['request']['original_utterance'].lower() in answers:
        if sessionStorage[user_id]['stage'] == 0:
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
            sessionStorage[user_id] = {
                'suggests': [
                    'Не хочу',
                    'Не буду',
                    'Отстань'
                ],
                'stage': 1
            }
        
        else:
            res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
            res['response']['end_session'] = True
            return
    
    if sessionStorage[user_id]['stage'] == 0:
        res['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    
    elif sessionStorage[user_id]['stage'] == 1:
        res['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи кролика!"

    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        if session['stage'] == 0: url = 'https://market.yandex.ru/search?text=слон'
        elif session['stage'] == 1: url ='https://market.yandex.ru/search?text=кролик'
        suggests.append({
            'title': 'Ладно',
            'url': url,
            'hide': True
        })

    return suggests


if __name__ == '__main__':
    app.run()