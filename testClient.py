import urllib2
import requests

# f = urllib2.urlopen("https://s3.amazonaws.com/outcome-blog/wp-content/uploads/2017/02/25192225/cat.jpg")
f1 = open("static/uploads/cat.jpg", 'rb')
f2 = open("static/uploads/cat.jpg", 'rb')
f3 = open("static/uploads/cat.jpg", 'rb')
f4 = open("static/uploads/cat.jpg", 'rb')
f5 = open("static/uploads/dog.jpg", 'rb')
data = {("file", f1), ("file", f2), ("file", f3), ("file", f4), ("file", f5)}
config = {"model": "alexnet", "agg": "none"}
r = requests.post("http://localhost:5000/serving", files=data, data=config)

print(r.text)
