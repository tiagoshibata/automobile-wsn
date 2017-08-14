import random
import requests

speed = random.uniform(0, 80)
requests.post('http://127.0.0.1:5000/', data={'speed': speed})
