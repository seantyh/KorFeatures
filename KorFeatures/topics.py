import requests
import pdb

TOPIC_ENDPOINT = "http://ctm.metafield.net:5000/"

def test_topics_endpoint():
    if not TOPIC_ENDPOINT:
        return False

    try:
        resp = requests.get(TOPIC_ENDPOINT)
        return resp.status_code == 200
    except:
        return False


def get_topics(words):
    text_data = "\n".join(words).encode("UTF-8")
    resp = requests.post(TOPIC_ENDPOINT, data = text_data)
    if resp.status_code != 200:
        print(resp.content)
        return None
    else:
        return resp.json()

def list_topics():
    resp = requests.get(TOPIC_ENDPOINT + "topic")
    if resp.status_code != 200:
        print(resp.content)
        return None
    else:
        return resp.json()
