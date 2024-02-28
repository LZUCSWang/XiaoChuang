import sqlite3
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from home.forms import LoginForm
from django.contrib import auth

idx = [
    0,
    "成瘾问题",
    "焦虑心理",
    "恋爱相关",
    "强迫症",
    "适应障碍",
    "睡眠障碍",
    "抑郁心理",
    "自我认知障碍",
]
file = ""
from PY import (
    ftoken2account,
    upload_data,
    get_dataset,
    get_datasets,
    creat_dataset,
    delete_dataset,
    rename_dataset,
    delete_data,
)
from PY import login as py_login

stations = [
    {"id": 1, "name": "成瘾问题", "image": "/static/elena.jpg"},
    {"id": 2, "name": "焦虑心理", "image": "/static/elena.jpg"},
    {"id": 3, "name": "恋爱相关", "image": "/static/elena.jpg"},
    {"id": 4, "name": "强迫症", "image": "/static/elena.jpg"},
    {"id": 5, "name": "适应障碍", "image": "/static/elena.jpg"},
    {"id": 6, "name": "睡眠障碍", "image": "/static/elena.jpg"},
    {"id": 7, "name": "抑郁心理", "image": "/static/elena.jpg"},
    {"id": 8, "name": "自我认知障碍", "image": "/static/elena.jpg"},
]
diaries = []
musics = []
explores = []
content_id = 0

# Create your views here.
global_token = ""
global_dataset_id = ""

import sqlite3


def get_replies(c, parent_id):
    """
    根据帖子ID获取所有直接回复，并递归获取楼中楼回复。
    """
    c.execute(
        "SELECT id, post_time, content, author FROM home_explore WHERE parent_id = ?",
        (parent_id,),
    )
    replies = c.fetchall()

    replies_dict = []
    for reply in replies:
        reply_id = reply[0]
        # 递归获取当前回复的楼中楼回复
        nested_replies = get_replies(c, reply_id)
        replies_dict.append(
            {
                "id": reply_id,
                "post_time": reply[1],
                "content": reply[2],
                "author": reply[3],
                "replies": nested_replies,
            }
        )

    return replies_dict


def show_diary(request):
    if request.method == "POST":
        try:
            # 直接从POST数据中解析，无需json.loads
            title = request.POST.get("title")
            content = request.POST.get("content")
            weather = request.POST.get("weather")
            background = request.POST.get("category")
            print("POST", title, content, weather, background)
            # 连接到数据库
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()

            # 检查是否存在具有给定标题的条目
            cursor.execute("SELECT * FROM home_diary WHERE title = ?", (title,))
            entry = cursor.fetchone()
            print(entry)
            if entry:
                # 更新存在的条目
                cursor.execute(
                    "UPDATE home_diary SET content = ?, weather = ?, background = ? WHERE title = ?",
                    (content, weather, background, title),
                )
                print("UPDATE home_diary SET content = ?, weather = ?, background = ? WHERE title = ?", (content, weather, background, title))
            else:
                # 创建新的条目
                cursor.execute(
                    "INSERT INTO home_diary (title, content, weather, background) VALUES (?, ?, ?, ?)",
                    (title, content, weather, background),
                )

            # 提交更改并关闭连接
            conn.commit()
            cursor.close()
            conn.close()

            return JsonResponse(
                {"status": "success", "message": "Diary entry updated successfully."}
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    for record in diaries:
        if record["id"] == int(content_id):
            print(record)
            return render(request, "diary.html", {"diary": record})
    return render(request, "diary.html")
    # return render(request, "diary-test.html")


from django.http import JsonResponse


def show_explore(request):
    global content_id
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    print(123)
    original_content = c.execute(
        "SELECT * FROM home_explore WHERE id = ?", (content_id,)
    ).fetchone()
    print(original_content)
    original_dict = dict(
        (k, original_content[i])
        for i, k in enumerate(["id", "post_time", "content", "author"])
    )
    replies_dict = get_replies(c, content_id)
    return render(
        request,
        "explore.html",
        {"original_post": original_dict, "replies": replies_dict},
    )


def show_station(request):
    if request.method == "POST":
        print("POST")
        global content_id
        content_type = request.POST.get("type")
        content_name = request.POST.get("name")
        print("content_id", content_id)
        print("content_type", content_type)
        print("content_name", content_name)

        global file
        if content_type == "科普":
            file = (
                "/static/"
                + content_type
                + "/"
                + idx[int(content_id)]
                + "/"
                + content_name
                + ".pdf"
            )
            return JsonResponse({"status": "success", "redirect_url": "/show_article/"})
        if content_type == "问卷":
            file = idx[int(content_id)] + "-" + content_name + ".html"
            return JsonResponse({"status": "success", "redirect_url": "/show_survey/"})
        if content_type == "方案":
            file = (
                "/static/"
                + content_type
                + "/"
                + idx[int(content_id)]
                + "/"
                + content_name
                + ".pdf"
            )
            return JsonResponse({"status": "success", "redirect_url": "/show_article/"})

        return JsonResponse({"status": "success", "redirect_url": "/show_explore/"})

    station_id = request.POST.get("station_id")
    # return HttpResponse("station" + str(station_id))
    # global content_id
    subcategory_name = idx[int(content_id)]
    # 链接数据库
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    # 查询数据库
    cursor.execute(
        "SELECT * FROM home_item WHERE subcategory = ?",
        (subcategory_name,),
    )
    items = cursor.fetchall()
    print(items)
    # 关闭数据库连接
    cursor.close()
    conn.close()
    ke_pus, wen_juans, fang_ans = [], [], []
    for item in items:
        if item[3] == "科普":
            ke_pus.append(
                {
                    "id": item[0],
                    "name": item[1],
                    "script": item[2],
                    "category": item[3],
                    "subcategory": item[4],
                    "image": "/static/elena.jpg",
                }
            )
        if item[3] == "问卷":
            wen_juans.append(
                {
                    "id": item[0],
                    "name": item[1],
                    "script": item[2],
                    "category": item[3],
                    "subcategory": item[4],
                    "image": "/static/elena.jpg",
                }
            )
        if item[3] == "方案":
            fang_ans.append(
                {
                    "id": item[0],
                    "name": item[1],
                    "script": item[2],
                    "category": item[3],
                    "subcategory": item[4],
                    "image": "/static/elena.jpg",
                }
            )
    return render(
        request,
        "station.html",
        {
            "station_id": station_id,
            "ke_pus": ke_pus,
            "wen_juans": wen_juans,
            "fang_ans": fang_ans,
        },
    )


from django.http import HttpResponse
from pdf2image import convert_from_path
import io


def show_Hitokoto(request):
    print("------------------------------")
    return render(request, "Hitokoto.html")


def show_article(request):
    # return HttpResponse('article')
    print(file)
    return render(request, "article.html", {"file": file})
    # return render(request, "成瘾问题科普文章(完成).mhtml")
    # views.py


def show_survey(request):
    # return HttpResponse('survey')
    return render(request, file)


def show_music(request):
    # musics[int(content_id) - 1]
    # 假设 musics 是您的数组，content_id 是要移动到开头的元素的索引（从 1 开始）
    content_id_int = int(content_id)  # 将字符串类型的索引转换为整数类型
    if 1 <= content_id_int <= len(musics):
        musics.insert(0, musics.pop(content_id_int - 1))

    return render(request, "music.html", {"music": musics})


def usr(request, token):
    global global_token
    global_token = token
    return render(
        request,
        "usr.html",
        {
            "token": token,
            "username": ftoken2account(token),
            "datasets": get_datasets(token),
        },
    )


def submit_survey(request):
    return HttpResponse("submit_survey")


def home(request):
    global global_dataset_id
    global global_token
    if request.method == "POST":
        dataset_id = request.POST.get("dataset_id")
        global_dataset_id = dataset_id
        dataset_name = get_datasets(global_token)[dataset_id]["name"]
        # print(dataset_name)
        return redirect(reverse("home"))
    else:
        dataset = json.dumps(get_dataset(global_token, global_dataset_id))
        return render(request, "home.html", {"dataset": dataset})


def django_login(request):
    # global global_token
    if request.method == "POST":
        global content_id
        content_id = request.POST.get("id")
        content_type = request.POST.get("type")
        if content_type == "station":
            return JsonResponse({"status": "success", "redirect_url": "/show_station/"})
        if content_type == "diary":
            return JsonResponse({"status": "success", "redirect_url": "/show_diary/"})
        if content_type == "music":
            # print("music[id]", musics[int(content_id) - 1])
            return JsonResponse({"status": "success", "redirect_url": "/show_music/"})
        if content_type == "explore":
            return JsonResponse(
                {
                    "status": "success",
                    "content_id": content_id,
                    "redirect_url": "/show_explore/",
                }
            )

        return JsonResponse({"status": "success", "redirect_url": "/show_explore/"})

        return HttpResponse("POST")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    diaries.clear()
    musics.clear()
    explores.clear()
    c.execute("SELECT * FROM home_diary")
    records = c.fetchall()
    print(records)
    for i, record in enumerate(records):
        diaries.append(
            {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "weather": record[3],
                "mood": record[4],
                "background": record[5],
                "image": "/static/elena.jpg",
            }
        )

    c.execute("SELECT * FROM home_music")
    records = c.fetchall()
    for i, record in enumerate(records):
        musics.append(
            {
                "id": record[0],
                "src": "/static/" + record[1],
                "poster": "/" + record[6],
                "name": record[2],
                "artist": record[3],
                "lyric": record[4],
                "sublyric": record[5],
            }
        )

    c.execute("SELECT * FROM home_explore")
    # print(c.fetchall()[0][0])
    records = c.fetchall()
    print(records)
    for record in records:
        if record[4] == None:
            print(record)
            explores.append(
                {
                    "id": record[0],
                    "time": record[1],
                    "name": record[2][:8],
                    "image": "/static/elena.jpg",
                }
            )

    return render(
        request,
        "login.html",
        {
            "stations": stations,
            "diaries": diaries,
            "musics": musics,
            "explores": explores,
        },
    )


# 参考（django）01 django实现前端上传图片到后端保存_django保存图片-CSDN博客.pdf
def django_upload_data(request):
    # 由前端指定的name获取到图片数据
    global global_token
    global global_dataset_id
    img = request.FILES.get("img")
    # 获取图片的全文件名
    img_name = img.name
    # 截取文件后缀和文件名
    mobile = os.path.splitext(img_name)[0]
    ext = os.path.splitext(img_name)[1]
    # 重定义文件名
    img_name = f"{mobile}{ext}"
    # print(img_name)
    upload_dir = os.path.join(os.getcwd(), "usr_upload")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    img_path = os.path.join(upload_dir, img_name)
    if not os.path.exists(img_path):
        # return HttpResponse('File already exists')
        # 写入文件
        with open(img_path, "ab") as fp:
            # 如果上传的图片非常大，就通过chunks()方法分割成多个片段来上传
            for chunk in img.chunks():
                fp.write(chunk)
        # fp.write(img.read())
    # 上传到AI库里
    with open(img_path, "rb") as f:
        data = f.read()
    upload_data(global_token, global_dataset_id, [(img_name, data)])
    # json2sqlite()+
    return HttpResponseRedirect(reverse("home"))


def django_delete_data(request):
    global global_token
    if request.method == "POST":
        # 批量删除版本
        data_id_seq = request.POST.get("delete_data_id")
        data_id_list = data_id_seq.split(",")
        for data_id in data_id_list:
            if data_id == "" or delete_data(global_token, global_dataset_id, data_id):
                continue
            else:
                HttpResponse("failue")
        return redirect(reverse("home"))
        # 单个删除版本
        data_id = request.POST.get("delete_data_id")
        if delete_data(global_token, global_dataset_id, data_id):
            return redirect(reverse("home"))
        else:
            HttpResponse("failue")
    pass


def django_create_dataset(request):
    if request.method == "POST":
        # 获取提交的数据
        global global_token
        dataset_name = request.POST.get("create_dataset_name")
        # print(token, dataset_name)
        datasets = get_datasets(global_token)
        dup = 0
        for dataset_id, dataset_info in datasets.items():
            if dataset_info["name"] == dataset_name:
                dup = 1
                break
        # 在这里处理你的逻辑，比如保存数据到数据库等
        if dup == 0:
            dataset_id = creat_dataset(global_token, dataset_name)
        # 返回一个简单的响应，你可以根据实际需求进行修改
        return render(
            request,
            "usr.html",
            {
                "dup": dup,
                "token": global_token,
                "username": ftoken2account(global_token),
                "datasets": get_datasets(global_token),
            },
        )
    # 如果是 GET 请求，可以根据实际需求返回一个页面或其他响应
    return HttpResponse("Invalid request method")


def django_delete_dataset(request):
    if request.method == "POST":
        global global_token
        account = ftoken2account(global_token)
        dataset_name = request.POST.get("delete_dataset_name")
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(
            "SELECT dataset_id FROM datasets WHERE dataset_name = ? AND account_id = (SELECT id FROM account WHERE username = ?)",
            (
                dataset_name,
                account,
            ),
        )
        try:
            dataset_id = c.fetchone()[0]
        except:
            # 删除不存在的数据集
            return render(
                request,
                "usr.html",
                {
                    "dup": 0,
                    "del": 1,
                    "token": global_token,
                    "username": ftoken2account(global_token),
                    "datasets": get_datasets(global_token),
                },
            )
        conn.close()
        print(dataset_id)
        if delete_dataset(global_token, dataset_id):
            return render(
                request,
                "usr.html",
                {
                    "dup": 0,
                    "token": global_token,
                    "username": ftoken2account(global_token),
                    "datasets": get_datasets(global_token),
                },
            )
        else:
            # HttpResponse('failue')
            # 删除失败
            return render(
                request,
                "usr.html",
                {
                    "dup": 0,
                    "del": 1,
                    "token": global_token,
                    "username": ftoken2account(global_token),
                    "datasets": get_datasets(global_token),
                },
            )
    return HttpResponse("Invalid request method")


def django_rename_dataset(request):
    global global_token
    if request.method == "POST":
        account = ftoken2account(global_token)
        previous_dataset_name = request.POST.get("previous_dataset_name")
        new_dataset_name = request.POST.get("new_dataset_name")
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(
            "SELECT dataset_id FROM datasets WHERE dataset_name = ? AND account_id = (SELECT id FROM account WHERE username = ?)",
            (
                new_dataset_name,
                account,
            ),
        )
        if c.fetchone() != None:
            # 新重命名的数据集已存在
            return render(
                request,
                "usr.html",
                {
                    "dup": 0,
                    "ren": 2,
                    "token": global_token,
                    "username": ftoken2account(global_token),
                    "datasets": get_datasets(global_token),
                },
            )
        c.execute(
            "SELECT dataset_id FROM datasets WHERE dataset_name = ? AND account_id = (SELECT id FROM account WHERE username = ?)",
            (
                previous_dataset_name,
                account,
            ),
        )
        try:
            dataset_id = c.fetchone()[0]
        except:
            # 原重命名的数据集不存在
            return render(
                request,
                "usr.html",
                {
                    "dup": 0,
                    "ren": 1,
                    "token": global_token,
                    "username": ftoken2account(global_token),
                    "datasets": get_datasets(global_token),
                },
            )
        conn.close()
        if rename_dataset(global_token, dataset_id, new_dataset_name):
            return render(
                request,
                "usr.html",
                {
                    "dup": 0,
                    "ren": 0,
                    "token": global_token,
                    "username": ftoken2account(global_token),
                    "datasets": get_datasets(global_token),
                },
            )
        else:
            # 重命名失败
            return render(
                request,
                "usr.html",
                {
                    "dup": 0,
                    "ren": 1,
                    "token": global_token,
                    "username": ftoken2account(global_token),
                    "datasets": get_datasets(global_token),
                },
            )
    return HttpResponse("Invalid request method")


def django_research_dataset(request):
    if request.method == "POST":
        global global_token
        global global_dataset_id
        dataset_name = request.POST.get("research_dataset_name")
        dataset = {}
        print(get_datasets(global_token))
        for key, value in get_datasets(global_token).items():
            print(value["name"], dataset_name)
            if value["name"] == dataset_name:
                dataset[key] = value
                return render(
                    request,
                    "usr.html",
                    {
                        "rea": 0,
                        "token": global_token,
                        "username": ftoken2account(global_token),
                        "datasets": dataset,
                    },
                )
        # print(dataset_name)

        dataset = get_datasets(global_token)
        return render(
            request,
            "usr.html",
            {
                "rea": 1,
                "token": global_token,
                "username": ftoken2account(global_token),
                "datasets": dataset,
            },
        )
    return HttpResponse("Invalid request method")
