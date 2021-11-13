import pypresence
import psutil
import time
import json
import sys

import logging
import coloredlogs

log = logging.getLogger('RPC')
coloredlogs.install()

def get_process_by_name(name: str):

    log.debug(f'Looking for process "{name}"')

    for process in psutil.process_iter(['name', 'exe', 'pid', 'create_time']):
        if process.info['name'] == name:
            log.debug(f'Found process! PID: {process.pid}...')
            return process
    
    log.debug('No process was found.')


games_data = json.load(open('games.json', 'r', encoding='utf-8'))

log.info('Running.')

while True:

    exit_on_game_close = True if '--exit_on_game_close' in sys.argv else False

    for game in games_data.keys():

        process = get_process_by_name(name = game)

        if process == None:
            continue

        else:

            log.debug(f'Starting RPC for "{game}"...')

            RPC = pypresence.Presence(client_id = games_data[game]['client_id'])
            RPC.connect()

            log.info('Connected to Discord')

            RPC.update(
                pid = process.info['pid'],
                start = process.info['create_time'],
                large_image = games_data[game]['icon_name']
            )

            while True:

                time.sleep(15)
                process = get_process_by_name(name = game)

                if process == None:
                    break

            log.debug('Game process finished. Stopping RPC')
            RPC.close()

            if exit_on_game_close:
                exit()

    time.sleep(2)