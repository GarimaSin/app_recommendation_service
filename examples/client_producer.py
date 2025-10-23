import requests, random, time, json
URL = 'http://localhost:8000/v1/recommend'
users = [f'user_{i}' for i in range(100)]
def call():
    uid = random.choice(users)
    r = requests.post(URL, json={'user_id': uid, 'k': 10})
    print(r.status_code, r.text)
if __name__=='__main__':
    for _ in range(5):
        call()
        time.sleep(1)
