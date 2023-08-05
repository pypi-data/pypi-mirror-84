import hashlib
import json
import logging
import traceback

import requests
from getenv import Env

from flask import Flask, Response, jsonify, request
from flask_caching import Cache
from flask_cors import CORS

from src import redis
from src.dfslo.lineup.generate_lineup import generate_lineup
from src.dfslo.projections import get_projections

logger = logging.getLogger('lineup-optimizer')
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)
cache = Cache(app)

projections_cache_duration: int = 86400


@app.errorhandler(500)
def __five_hundred_error(e):
    logger.error('an error happened', exc_info=e)
    return Response(traceback.format_exc(), status=500, mimetype='application/text')


@app.route('/')
def __health_check():
    return 'hi'


@app.route('/leagues')
@cache.cached(timeout=300)
def __get_leagues():
    contests = requests.get('https://www.draftkings.com/lobby/getcontests?sport=SOC').json()
    game_sets = [x['ContestStartTimeSuffix'].strip().replace('(', '').replace(')', '') for x in contests['GameSets']]
    return jsonify([x for x in game_sets if len(x.split(' ')) == 1]), 200


@app.route('/key/<string:league>')
@cache.cached(timeout=60)
def __get_projections(league: str):
    projections = get_projections(league)
    m = hashlib.sha256()
    m.update(json.dumps(projections).encode('utf-8'))
    key = m.hexdigest()
    redis.put(key, json.dumps(projections), projections_cache_duration)
    return jsonify(key=key), 200


@app.route('/players/<string:key>')
@cache.cached(timeout=300)
def __get_players(key: str):
    return jsonify(__load_projections(key)['players']), 200


@app.route('/games/<string:key>')
@cache.cached(timeout=300)
def __get_games(key: str):
    return jsonify(__load_projections(key)['games']), 200


@app.route('/lineup', methods=['POST'])
def __generate_lineup():
    request_data = json.loads(request.data)
    key = request_data['key']
    projections = __load_projections(key)
    return jsonify(generate_lineup(
        request_data['roster_format'],
        request_data['flex_position_mapping'],
        request_data['salary_limit'],
        projections['players']
    )), 200


def __load_projections(key: str) -> dict:
    projections = json.loads(redis.get(key))
    redis.expire(key, projections_cache_duration)
    return projections


if __name__ == '__main__':
    Env.set_prefix('')
    app.run(
        host='0.0.0.0',
        threaded=True,
        port=Env('PORT', type=int, default=5000).get(),
        debug=Env('DEBUG', type=bool, default=True).get()
    )
