import urllib2
import requests

# f = urllib2.urlopen("https://s3.amazonaws.com/outcome-blog/wp-content/uploads/2017/02/25192225/cat.jpg")
f = open("static/uploads/cat.jpg", 'rb')
data = {"file": f}
r = requests.post("http://localhost:5000/serving", files=data)

print(r.text)
