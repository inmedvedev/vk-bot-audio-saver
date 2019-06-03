from flask import Flask, request, json
import vk_api
import logging
import os
import requests


access_token = 'YOUR_ACCESS_TOKEN'
confirmation_token = 'YOUR_CONFIRMATION_TOKEN'


logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.DEBUG,
    filename=u'mylog.log'
)


app = Flask(__name__)


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if data['type'] == 'confirmation':
        return confirmation_token
    if data['type'] == 'message_new':
        if not data['object']['attachments']:
            return 'ok'
        attachment_info = data['object']['attachments'][0]
        uid = str(data['object']['from_id'])
        if not os.path.exists(uid):
            os.makedirs(uid)
        link_mp3 = attachment_info['audio_message']['link_mp3']
        number_of_files = len([filename for filename in os.listdir(uid) if os.path.isfile(os.path.join(uid, filename))])
        filename = 'auido_message_{}'.format(number_of_files)
        with open(os.path.join(uid, filename), 'wb') as out_stream:
            req = requests.get(link_mp3, stream=True)
            for chunk in req.iter_content(1024):
                out_stream.write(chunk)
        logging.info(filename)
    return 'ok'
