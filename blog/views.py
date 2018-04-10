from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import Post
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm
import rethinkdb as r

gcpconn = r.connect(host = '35.196.140.167', port = 28015)
conn = r.connect()
conn.use('babyhome')

import datetime
import pymongo
import re
from pymongo import MongoClient
client = MongoClient()
client = MongoClient("mongodb://localhost:27017")
db = client.pttdb
posts = db.beautysalon_adj
oil_regex=re.compile("出油|控油|油性",re.IGNORECASE)
dry_regex=re.compile("保濕|滋潤",re.IGNORECASE)
middle_good_regex=re.compile("T字|t字|混和",re.IGNORECASE)
middle_bad_regex=re.compile("敏感",re.IGNORECASE)
d1 = datetime.datetime.strptime("2016-01-20T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
d2 = datetime.datetime.strptime("2018-03-21T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

import base64



me = get_user_model().objects.get(username="emilien")

def post_list(request):
    post_form = PostForm()
    posts = Post.objects.all().order_by('-created_date')
    
    x=r.db('faceai').table('project').get('916bcc4a-85a4-4cac-93b7-a00f9505f073').run(gcpconn)['model']
    y=r.db('faceai').table('project').get('916bcc4a-85a4-4cac-93b7-a00f9505f073').run(gcpconn)['z_img']
    if x=='oil_bad' or x=='oil_good':
        result=r.db('babyhome').table("test333").filter(r.row['title'].match("出油|控油|油性")).order_by(r.desc("id")).limit(4).run(conn)
        mgresult=db.beautysalon_adj.find({"$and": [{'article_title':oil_regex},{'pub_date':{'$gte':d1,'$lt':d2}}]}).sort([("pub_date", pymongo.DESCENDING)]).limit(4)
    elif x=='dry_good' or x=='dry_bad':
        result=r.db('babyhome').table("test333").filter(r.row['title'].match("保濕|滋潤")).order_by(r.desc("id")).limit(4).run(conn)
        mgresult=db.beautysalon_adj.find({"$and": [{'article_title':dry_regex},{'pub_date':{'$gte':d1,'$lt':d2}}]}).sort([("pub_date", pymongo.DESCENDING)]).limit(4)
    elif x=='middle_good':
        result=r.db('babyhome').table("test333").filter(r.row['title'].match("T字|t字|混和")).order_by(r.desc("id")).limit(4).run(conn)
        mgresult=db.beautysalon_adj.find({"$and": [{'article_title':middle_good_regex},{'pub_date':{'$gte':d1,'$lt':d2}}]}).sort([("pub_date", pymongo.DESCENDING)]).limit(4)
    else:
        result=r.db('babyhome').table("test333").filter(r.row['title'].match("敏感")).order_by(r.desc("id")).limit(4).run(conn)
        mgresult=db.beautysalon_adj.find({"$and": [{'article_title':middle_bad_regex},{'pub_date':{'$gte':d1,'$lt':d2}}]}).sort([("pub_date", pymongo.DESCENDING)]).limit(4) 
    ### Server
    image_64_decode = base64.b64decode(y)
    image_result = open('test.jpg', 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    image_result.close()
    
    
    author0=result[0]['author']
    author1=result[1]['author']
    author2=result[2]['author']
    author3=result[3]['author']
    title0=result[0]['title']
    title1=result[1]['title']
    title2=result[2]['title']
    title3=result[3]['title']
    url0=result[0]['url']
    url1=result[1]['url']
    url2=result[2]['url']
    url3=result[3]['url']
    mgauthor0=mgresult[0]['author']
    mgauthor1=mgresult[1]['author']
    mgauthor2=mgresult[2]['author']
    mgauthor3=mgresult[3]['author']
    mgtitle0=mgresult[0]['article_title']
    mgtitle1=mgresult[1]['article_title']
    mgtitle2=mgresult[2]['article_title']
    mgtitle3=mgresult[3]['article_title']
    mgurl0=mgresult[0]['url']
    mgurl1=mgresult[1]['url']
    mgurl2=mgresult[2]['url']
    mgurl3=mgresult[3]['url']
    
    return render(request,'blog/post_list.html',locals())

def add_record(request):
    if request.POST:
        title = request.POST['title']
        text = request.POST['text']
        newpost = Post.objects.create(author = me, title=title, text=text)
    return redirect('/blog')

def post_record(request,id):
    posts = Post.objects.filter(id__lte=id)[::-1][:2]
    post = posts[0]
    next_post = posts[1] if len(posts) > 1 else None
    return render(request, 'blog/post_record.html', locals())



def getResult(request):
    
    return render(request,'blog/post_list.html',locals())
