#! python3
# -*-coding:utf-8-*-
# author: muyangren907
import json,os,codecs,pprint,re,time,queue,urllib,socket,threading
from urllib.request import urlretrieve

itemnum = 0
havedownload = 0
vq = queue.Queue()
def download(vq):
    while True:
        # vq.put([caption, photo_id, mv_urls, atlas, cover_urls],path)
        videomes = vq.get()
        caption = videomes[0]
        photo_id = videomes[1]
        mv_urls = videomes[2]
        atlas = videomes[3]
        cover_urls = videomes[4]
        path = videomes[5]
        # itemnum = videomes[6]

        global havedownload

        if mv_urls!="None" :
            downfile = os.path.join(path, str(photo_id)+"_"+caption + ".mp4")   #filename = photo_id+caption
            try:
              urlretrieve(mv_urls,downfile)
            except IOError:
                downfile = os.path.join(path, "错误" + '%s.mp4') % photo_id
                try:
                    urlretrieve(mv_urls, downfile)
                except (socket.error, urllib.ContentTooShortError):
                    print("请求被断开，休眠2秒")
                    time.sleep(2)
                    urlretrieve(mv_urls,downfile)
            havedownload+=1
            print("(%d/%d)视频下载完成: %s_%s"% (havedownload,itemnum,photo_id,caption))
            vq.task_done()
        else:
            if atlas[0]!="None" :
                caption = caption.replace(".","。")
                if os.path.exists(path+"/"+str(photo_id) + "_" + caption) == False:
                    os.mkdir(path+"/"+str(photo_id) + "_" + caption)
                for atlasindex in range(len(atlas)):
                    atlas_url = atlas[atlasindex]
                    downfile = os.path.join(path+"/"+str(photo_id) + "_" + caption, str(atlasindex) + ".webp")  # filename = atlasindex
                    try:
                        urlretrieve(atlas_url, downfile)
                    except IOError:
                        downfile = os.path.join(path+"/"+str(photo_id) + "_" + caption, "错误" + '%s%s.webp') %(photo_id,atlasindex)
                        try:
                            urlretrieve(atlas_url, downfile)
                        except (socket.error, urllib.ContentTooShortError):
                            print("请求被断开，休眠2秒")
                            time.sleep(2)
                            urlretrieve(atlas_url, downfile)
                havedownload += 1
                print("(%d/%d)图集下载完成: %s_%s" % (havedownload,itemnum,photo_id,caption))
                vq.task_done()
            else:
                downfile = os.path.join(path, str(photo_id) + "_" + caption + ".jpg")  # filename = photo_id+caption
                try:
                    urlretrieve(cover_urls, downfile)
                except IOError:
                    downfile = os.path.join(path, "错误" + '%s.mp4') % photo_id
                    try:
                        urlretrieve(cover_urls, downfile)
                    except (socket.error, urllib.ContentTooShortError):
                        print("请求被断开，休眠2秒")
                        time.sleep(2)
                        urlretrieve(cover_urls, downfile)
                havedownload += 1
                print("(%d/%d)图片下载完成: %s_%s" % (havedownload,itemnum,photo_id,caption))
                vq.task_done()



def main():
    user_name = ""
    user_id = 0

    localtime = time.asctime(time.localtime(time.time())) #get time
    # count number
    global itemnum
    videonum = 0
    atlasnum = 0
    picturenum = 0


    filelist = os.listdir("./")  # get the file list

    jsonfilename = []
    for file_index in range(len(filelist)):
        filestr = str(filelist[file_index])
        if filestr.find(".json", 0, len(filestr)) != -1:
            jsonfilename.append(filestr)  # add json file name to jsonfilename list
    print("json文件总数为: " + str(len(jsonfilename)))

    for file_index in range(len(jsonfilename)):
        jsonfile = open("./"+jsonfilename[file_index],"r",encoding="utf8") #open json file
        jsonstr = jsonfile.read() #read file to jsonstr
        jsonobj = json.loads(jsonstr)

        user_name = jsonobj['feeds'][0]['user_name'].replace("/","")    #get user_name
        user_id = jsonobj['feeds'][0]['user_id']    #get user_id
        # print(user_name+" "+str(user_id))

        if os.path.exists("./"+user_name) == False:
            os.mkdir("./"+user_name)    #mkdir using user_name

        mv_urls = "None"
        atlas = ["None"]
        cover_urls = "None"

        for item in jsonobj['feeds']:
            itemnum+=1
            # pprint.pprint(itme)
            caption = item['caption']

            notchar = ["?", "*", "/", "\\", "<", ">", ":", "\"", "|", "\n","\r"," "]  # These characters cannot appear in the file name
            for chari in range(len(notchar)):
                caption = caption.replace(notchar[chari], "")
            caption = caption[0:29] #file name can't be too long

            photo_id = item['photo_id']
            if 'main_mv_urls' in item :
                videonum+=1
                mv_urls = item['main_mv_urls'][0]['url']
            else :
                mv_urls = "None"
                # print(photo_id)
                if 'atlas' in item["ext_params"] :
                    atlasnum+=1
                    atlas = item["ext_params"]['atlas']['list']
                    for atlas_index in range(len(atlas)):
                        atlas[atlas_index]="http://"+item["ext_params"]['atlas']['cdnList'][0]['cdn']+atlas[atlas_index]  #url=cdn+relative_url
                        # print(atlas[atlas_index])
                else :
                    picturenum+=1
                    atlas=["None"]
                    cover_urls = item['cover_urls'][0]['url']
                    # print(cover_urls)
            # print(caption)
            vq.put([caption,photo_id,mv_urls,atlas,cover_urls,"./"+user_name])

            # fp =open("./"+user_name+"/"+caption+".txt","w")
            # fp.close()
        # print(user_name + str(user_id))

        jsonfile.close() #close file
    print("itemnum\t"+str(itemnum)+"\nvideonum\t"+str(videonum)+"\natlasnum\t"+str(atlasnum)+"\npicturenum\t"+str(picturenum))
    if os.path.exists("./" + user_name + "/" + user_name + ".txt") == False:
        user_mes_file = codecs.open("./" + user_name + "/" + user_name + ".txt", "w","utf-8")
        user_mes_file.write("download_time\t"+localtime+"\n")
        user_mes_file.write("user_name\t" + user_name + "\nuser_id\t" + str(user_id) + "\n")
        user_mes_file.write("itemnum\t"+str(itemnum)+"\nvideonum\t"+str(videonum)+"\natlasnum\t"+str(atlasnum)+"\npicturenum\t"+str(picturenum))
        user_mes_file.close()
    threadnum = 32  # thread number
    for thread_num in range(threadnum):
        t = threading.Thread(target=download,args=(vq,))
        t.setDaemon(True)
        t.start()
    vq.join()
    # print(str(itemnum)+" "+str(videonum)+" "+str(atlasnum)+" "+str(picturenum))
main()
