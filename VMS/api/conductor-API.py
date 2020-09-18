import requests

url = "http://staging-cm.dadcdigital.com:8112/api/email_links"

querystring = {"multitenancyemail":"jasmine.ma@sonydadc.com"}

payload = "{\"components\":[\"000003fflu\"],\"recipients\":[{\"firstName\":\"Jasmine\",\"lastName\":\"Ma\",\"emailAddress\":\"Jasmine.ma@sonydadc.com\"}],\"message\":\" Yeeehaaa \",\"expirationDays\":\"7\",\"oneLinkOnly\":true} "
headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "601c21fc-317d-4417-ad5c-c133613ddd64,7360d51b-7ee2-4a97-9dc1-1ddbb3606859",
    'Host': "staging-cm.dadcdigital.com:8112",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "189",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("PUT", url, data=payload, headers=headers, params=querystring)

print(response.text)