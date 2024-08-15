import json
import os
import requests

dirname, _ = os.path.split(os.path.abspath(__file__))
THIS_DIRECTORY = f'{dirname}{os.sep}'

class ConfigError(Exception):
	pass

def init():
	config_file = f'{THIS_DIRECTORY}config.json'
	if os.path.exists(config_file):
		config = load_json(config_file)
		if 'ntfy_url' in config:
			if not config['ntfy_url'] == 'YOUR-TOPIC-URL':
				return config
			else:
				raise ConfigError('No ntfy.sh topic URL specified in config.json, see https://docs.ntfy.sh/')
		else:
			raise ConfigError('No ntfy.sh topic URL specified in config.json, see https://docs.ntfy.sh/')
	else:
		default_config()
		raise ConfigError(f'No config.json file found so generated default. Please add your ntfy.sh topic URL & try again')

def default_config():
	config = {
		'ntfy_url':'YOUR-TOPIC-URL'
	}
	save_json(config, f'{THIS_DIRECTORY}config.json')

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4))

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def notify(url, message, attachment_url=None, tags=None, high_priority=False):
    headers = {}
    if tags is not None:
        headers['Tags'] = ','.join(tags)
    if high_priority:
        headers['Priority'] = '5'
    if attachment_url is not None:
        headers['Actions'] = f'view, View, {attachment_url}'
    requests.post(
        url,
        data=message.encode(encoding='utf-8'),
        headers=headers
   )

def main():
	config = init()
	notify(config['ntfy_url'], 'MarsMonitor has started', tags=['MarsMonitor', 'startup', 'white_circle'])


if __name__ == '__main__':
	main()
