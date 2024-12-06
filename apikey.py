import http.client

conn = http.client.HTTPSConnection("joke3.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "API-Key",
    'x-rapidapi-host': "joke3.p.rapidapi.com"
}

conn.request("GET", "/v1/joke", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))