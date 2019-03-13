#users = flickr.people.getInfo(user_id='7130511@N02')
#users = flickr.groups.discuss.topics.getList(group_id='35034344821@N01')
#users =flickr.groups.pools.getPhotos(group_id='35034344821@N01')
#sets = flickr.photosets.getList(user_id='7130511@N02')

def output10(x):
    for count in range(0,10) :
        print x[count]
        
    
import time
import os
import json
import flickrapi
api_key = u'531de57675ff6e07d3c683b7083467f2'
api_secret = u'f1e92d7e0e8cb21c'


f=open('combine_data_lee.txt','r')
userID=[]
photoID=[]
for lines in f:
    items=lines.strip().split('\t')
    userID.append(items[12])
    photoID.append(items[13])
f.close()


textFeature={}
contentDict={'Tags':0,'Title':0,'Desc':0}
for item in photoID:
    textFeature[item]=contentDict


flickr = flickrapi.FlickrAPI(api_key, api_secret,format='parsed-json')


ErrorList=[]
x=0
while x < len(photoID) :
    try:
    
        photoRawInfo = flickr.photos.getInfo(photo_id=photoID[x])
        if photoRawInfo['photo']['id'] == photoID[x]:
            textFeature[photoID[x]]['Title'] = photoRawInfo['photo']['title']['_content']
            textFeature[photoID[x]]['Desc'] = photoRawInfo['photo']['description']['_content']
            tmp=[]
            for item in photoRawInfo['photo']['tags']['tag']:
                tmp.append(item['_content'])
            textFeature[photoID[x]]['Tags']=tmp
            print(x," . ",photoID[x],"is OK")
            x=x+1
            
    except Exception, e:
    
        error_meaasge=str(e)
        if ("invalid ID"  in  error_meaasge) or  ("not found" in error_meaasge):
            print(x," . ",photoID[x]," === ",error_meaasge)
            ErrorList.append(photoID[x])
            x=x+1
        else:
            print(error_meaasge)


with open('dataaa.txt', 'w') as outfile:
    json.dump(textFeature, outfile)

f=open('ErrorList.txt','w')
for x in ErrorList:
    f.write(x)
    f.write("\r\n")
f.close()
