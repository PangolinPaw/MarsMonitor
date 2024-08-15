import json
import os
import time
import requests
import vision

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

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4))

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
	# notify(
	# 	config['ntfy_url'],
	# 	'MarsMonitor has started',
	# 	tags=['MarsMonitor', 'startup', 'white_circle']
	# )
	while True:
		image = vision.capture()
		error, progress = vision.get_progress(image)
		if error is None:
			status = 'progress'
			high_priority = False
			if progress == 100:
				message = 'Print complete'
				icon = 'green_circle'
				high_priority = True
			elif progress > 75:
				message = f'Print progress: {progress}%'
				icon = 'yellow_circle'
			elif progress < 50:
				message = f'Print progress: {progress}%'
				icon = 'orange_circle'
		else:
			message = f'Print error: {error}'
			status = 'error'
			icon = 'red_circle'
			high_priority = True

		# notify(
		# 	config['ntfy_url'],
		# 	message,
		# 	tags=['MarsMonitor', status, icon],
		# 	high_priority=high_priority
		# )
		
		time.sleep(config.get('update_frequency', 300))


if __name__ == '__main__':
	main()
