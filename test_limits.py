import requests

for i in range(1, 100):
    response = requests.get(f"http://localhost/search/google?text=Абрамов&page={i}", timeout=120)
    print(response)
    data = response.json()
    if data["status"] != 200:
        print(i, data)
        break
