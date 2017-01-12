import requests

print requests.__version__

response = requests.get("https://raw.githubusercontent.com/zhangtuxin/CMPUT404Wesdnesday/master/checkversion.py")
print response.text
print response.status_code
