import os
from flask import request, Flask, jsonify, send_file
from saver import Saver
from card import Card
import click

app = Flask(__name__)
app.config['saver'] = None

@app.get('/creators')
def creators_get():
	saver = app.config['saver']
	creator_set = saver.get_creators()
	return jsonify({'creators': creator_set})

@app.get('/creators/<string:creator>/cards')
def creator_cards_get(creator):
	saver = app.config['saver']
	creator_cards = saver.find_cards({'creator': creator})
	return jsonify({'creator':creator, 'cards': creator_cards})


@app.get('/creators/<string:card_creator>/cards/<string:card_name>')
def card_metadata_get(card_creator, card_name):
	saver = app.config['saver']
	return jsonify({'card_metadata': saver.get_metadata(card_name, card_creator)})

@app.get('/creators/<string:card_creator>/cards/<string:card_name>/image.jpeg')
def card_image_get(card_creator, card_name):
	saver = app.config['saver']
	image_path = saver.get_metadata(card_name, card_creator)['image_path']
	return send_file(image_path, mimetype='image')
'''
@click.command()
@click.argument('host', type=click.STRING)
@click.argument('port', type=click.INT)
@click.option('--database_url',defult='mongodb://127.0.0.1:27017', type=click.STRING,
	help= 'url that define saver')
'''
#maybe add debug option
def run_api_server(host, port, database_url):
	print(database_url)
	app.config['saver'] = Saver(database_url)
	app.run(host=host, port=port, debug=True)
	click.echo('server initialized')

if __name__ == '__main__':
	run_api_server('127.0.0.1', 7012, 'filesystem:solved_cards')