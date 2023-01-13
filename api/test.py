import requests

response = requests.post("https://api-getaround.herokuapp.com/predict", json={
    'plat': "poulet",   
})

print(response.json())