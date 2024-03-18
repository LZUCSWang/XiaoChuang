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
# from PY import (
#     ftoken2account,
#     upload_data,
#     get_dataset,
#     get_datasets,
#     creat_dataset,
#     delete_dataset,
#     rename_dataset,
#     delete_data,
# )
# from PY import login as py_login

stations = [
    {
        "id": 1,
        "name": "成瘾问题",
        "image": "/static/科普/成瘾问题/成瘾问题科普文章.png",
    },
    {
        "id": 2,
        "name": "焦虑心理",
        "image": "/static/方案/焦虑心理/面对焦虑，我该怎么办？.png",
    },
    {
        "id": 3,
        "name": "恋爱相关",
        "image": "/static/方案/恋爱相关/大学生的恋爱心理矛盾及解决.png",
    },
    {"id": 4, "name": "强迫症", "image": "/static/科普/强迫症/什么是强迫症？.png"},
    {
        "id": 5,
        "name": "适应障碍",
        "image": "/static/科普/适应障碍/【专家说】人生就是一场适应的过程，带你了解“适应障碍”.png",
    },
    {
        "id": 6,
        "name": "睡眠障碍",
        "image": "/static/科普/睡眠障碍/睡眠障碍科普文章.png",
    },
    {
        "id": 7,
        "name": "抑郁心理",
        "image": "/static/科普/抑郁心理/关于抑郁症，这些知识你一定要知道！.png",
    },
    {
        "id": 8,
        "name": "自我认知障碍",
        "image": "/static/方案/自我认知障碍/自卑心理解决方案.png",
    },
]
diaries = []
musics = []
explores = []
content_id = 0

# Create your views here.
global_token = ""
global_dataset_id = ""
global_username = ""
import sqlite3


def login1(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        global global_username
        global_username = username
        # user = auth.authenticate(username=username, password=password)
        # if user is not None and user.is_active:
        #     auth.login(request, user)
        return redirect(reverse("login"))
        # else:
        #     messages.add_message(request, messages.ERROR, "用户名或密码错误")
        #     return render(request, "login1.html")
    return render(request, "login1.html")


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
                "parent_id": parent_id,
            }
        )

    return replies_dict


def show_diary(request):
    if request.method == "POST":
        try:
            if request.POST.get("delete") == "yes":
                conn = sqlite3.connect("db.sqlite3")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM home_diary WHERE id = ?", (content_id,))
                conn.commit()
                cursor.close()
                conn.close()
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Diary entry deleted successfully.",
                    }
                )
            # 直接从POST数据中解析，无需json.loads
            title = request.POST.get("title")
            content = request.POST.get("content")
            weather = request.POST.get("weather")
            background = request.POST.get("category")
            # 连接到数据库
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE home_diary SET content = ?, weather = ?, background = ? ,title = ? WHERE id = ?",
                (content, weather, background, title, content_id),
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
            print(diaries)
            return render(request, "diary.html", {"diary": record})
    return render(request, "diary.html")


from django.http import JsonResponse


def show_explore(request):
    global content_id
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    original_content = c.execute(
        "SELECT * FROM home_explore WHERE id = ?", (content_id,)
    ).fetchone()
    original_dict = dict(
        (k, original_content[i])
        for i, k in enumerate(["id", "post_time", "content", "author", "parent_id"])
    )
    replies_dict = get_replies(c, content_id)
    return render(
        request,
        "explore.html",
        {"original_post": original_dict, "replies": replies_dict},
    )

content_name = ""
def show_station(request):
    if request.method == "POST":
        global content_id
        content_type = request.POST.get("type")
        global content_name
        content_name= request.POST.get("name")

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
                    "image": "/static/科普/" + item[4] + "/" + item[1] + ".png",
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
                    "image": "/static/问卷/" + item[4] + "/" + item[1] + ".png",
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
                    "image": "/static/方案/" + item[4] + "/" + item[1] + ".png",
                }
            )
    return render(
        request,
        "station.html",
        {
            "typename": idx[int(content_id)],
            "station_id": station_id,
            "ke_pus": ke_pus,
            "wen_juans": wen_juans,
            "fang_ans": fang_ans,
        },
    )


from django.http import HttpResponse

# from pdf2image import convert_from_path
import io


def show_Hitokoto(request):
    return render(request, "Hitokoto.html")


def show_article(request):
    # return HttpResponse('article')
    return render(request, "article.html", {"file": file})
    # return render(request, "成瘾问题科普文章(完成).mhtml")
    # views.py


def show_survey(request):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM home_questionnaire WHERE title = ?", (content_name,))
    _ = cursor.fetchone()    
    questionnaire={}
    questionnaire["title"]=content_name
    questionnaire["description"]=_[3]
    questionnaire["result"]=_[2]
    questions=[]
    cursor.execute("SELECT * FROM home_question WHERE questionnaire_id = ?", (_[0],))
    _ = cursor.fetchall()
    for i in _:
        question={}
        question["id"]=i[0]
        question["text"]=i[1]
        question["options"]=[]
        # print(_)
        for j in range(3, 7):
            if i[j]:
                # question["options"].append({"value": i, "label": idx[i]})
                cursor.execute("SELECT * FROM home_option WHERE id = ?", (i[j],))
                opt = cursor.fetchone()
                print(opt)
                question["options"].append({"value": opt[2], "text": opt[1]})
        questions.append(question)
    return render(request, "survey.html", {"questionnaire": questionnaire,"questions":questions})
    # return render(request, file, {"questions": questions})
    questions = []
    if file == "适应障碍-大学生适应性量表.html":
        question = """ 
1.我时大学的学习感到无所适从。
2.我感到周围的人难以相处，
3.我和异性同学相处得不好。
4.我觉得自己还没有作好进入社会的准备。
5.我能独立地处理日常事务。
6.周末我常常堂得没事可做。
7.我经常感到身体乏力，不舒服。
8.我时常无理由地郁郁寡欢。
9.我时自己上了这所大学感到高兴。
10.父每不在身边，我也能够田顾好自己。
11.我从没有考虑过以后的就业问题。
12.我参与了很多大学里的社会活动。
13.我能很快化解与他人的矛盾冲突。
14 我无法适应大学教师的投课方式。
15.我不知道以何种方式与大学老师相处。
16.我根难加入到别人的讨论中去。
17.我从不关心学习以外的东西。
18.我有明确的就业意向。
19.我常打电话向家人诉苦或求助。
20.我很喜欢校园里的自然环境。
21.我很容易生气。22.我总是没精打采。
23.我对大学里的谋外活动感到满意。
24.我不敢单独上街买东西。
25.我不知道自己适合从事哪方面的工作。
26.我只在乎自己的学业成绩。
27.大伙儿讲话时，我时需躲在后面。
28.在考试前，我不如道该如何着手复习。
29.我现在还没找到自己较为满意的学习方法。
30.我在大学里如那地结交了一些朋友。
31.除了学习，我很少参加别的活动。
32.我难以决定自己该到哪星工作。
33.我很少自己动手洗衣服。
3L 学校的娱乐设施不能满足我的需要。
35.我容易觉得累。
36.我的胃口还好。
37.我认为学校的风气很糟。
38.在大学什么都差靠自己，我感到很不适应。
39.我有意识地训练自己的职业技能。
40.若有机会，我能胜任某种学生干部的工作。
41.我觉得我已融入了大学的环境。
42 我一直都没有明确的学习计划。
43.我感到无法缓解自己的学习压力。4L 我感到自己在学校里成了一个被道忘的人。
45.我很重视发展自己的业余爱好。
46.我参加过与专业有关的社会实践活动。
47.我觉得学校的硬件设施很差。
48.我的体重增加(或减少》了很多。
49.我很容易失眠。
50.我有意识他通过各种渠道收集就业信息。
51.我认为在大学集应多参加一些学习以外的活动。
52.我害怕与异性同学交往。
53.我对自己在班上的学业地位感到失望。
5L 我不知道哪些专业知识是以后工作所需要的。
55.我能与人愉快的进行合作。
56.我常感到头痛。
57.我有时想找心理医生寻求帮助。
58.在学校票和同学在一起时，我感到不自在。
59.与我的努力相比。我的学习成绩不算好。
60.对于我在大学里的社空。我感到相当满意。
61.我的确不胜任大学的学习任务。
62.在大学菜，我有一些亲害的朋友。
63.我有意识地培养自己的业会兴趣。
64.我有业识的为以后的就业加强各种训练，
65.我认为学校的风气很差。
66.完全拿自己，自己对自己负责，这对于我而言并不容易。
""".split()
        options = [{"value":1,"label":"很不符合"},{"value":2,"label":"不太符合"},{"value":3,"label":"不能确定"},{"value":4,"label":"有点符合"},{"value":5,"label":"非常符合"}]
        for q in question:
            questions.append({"id":len(questions)+1,"text":q,"options":options})
    if file == "适应障碍-工作适应障碍量表.html":
        options = [{"value":1,"label":"对"},{"value":2,"label":"错"}]
        Tfor1 = [3,4,5,6,7,8,9,10,12,13,15,17,18,20,21,22,23,25,26,27,28,29,30,31,33,34,35,36,37]
        question = """1. 我早上起来的时候，多半觉得睡眠充足，头脑清醒。
2. 我现在工作（学习）的能力，和从前差不多。
3. 我总是在很紧张的情况下工作。
4. 我深信生活对我是不公平的。
5. 我发现我很难把注意力集中到一件工作上。
6. 假如不是有人和我作对，我一定会有更大的成就。
7. 有很多时候我宁愿坐着空想，而不愿做任何事情。
8. 我曾一连几天、几个星期、几个月什么也不想干，因为我总是提不起精神。
9. 我时常得听从某些人的指挥，其实他们还不如我高明。
10. 现在，我发现自己很容易自暴自弃。
11. 我总觉得人生是有价值的。
12. 有些人太霸道，即使我明知他们是对的，也要和他们对着干。
13. 我时常认为必须坚持那些我认为正确的事。
14. 我喜欢研究和阅读与我目前工作有关东西。
15. 我不在乎别人对我有什么看法。
16. 我喜欢许多不同种类的游戏和娱乐。
17. 我的做事方法容易被人误解。
18. 有人想把世界上所能得到的东西都夺到手，我决不责怪他。
19. 凡是我所做的事，我都指望能够成功。
20. 做什么事情，我都感到难以开头。
21. 我有时精力充沛。
22. 许多时候，生活对我来说是一件吃力的事。
23. 我不喜欢有人在我的身旁。
24. 在我的日常生活中，充满着使我感兴趣的事情。
25. 假如不是有人和我作对，我一定会有更大的成就。
26. 我不能专心于一件事情上。
27. 哪怕是琐碎的小事，我也再三考虑后才去做。
28. 我时常遇见一些所谓的专家，他们并不比我高明。
29. 当事情不顺利的时候，我就想立即放弃。
30. 面对困难或危险的时候，我总退缩不前。
31. 当我想纠正别人的错误和帮助他们的时候，我的好意常被误解。
32. 我通常很镇静，不容易激动。
33. 我通常喜欢和妇女一起工作。
34. 我的计划看来总是困难重重，使我不得不一一放弃。
35. 我经常遇到一些顶头上司，他们把功劳归于自己，把错误推给下级。
36. 我的前途似乎没有希望。
37. 未来是变化无常的，一个人很难做出认真的安排。""".split("\n")
        for i in range(1,38):
            if i in Tfor1:
                questions.append({"id":i,"text":question[i-1],"options":options})
            else:
                questions.append({"id":i,"text":question[i-1],"options":[{"value":2,"label":"对"},{"value":1,"label":"错"}]})



    def show_survey(request):
        questionnaires = Questionnaires.objects.all()
        return render(request, "survey.html", {"questionnaires": questionnaires})
    c = conn.cursor()
    c.execute("SELECT * FROM Questionnaires")
    questionnaires = c.fetchall()
    conn.close()
    return render(request, "survey.html", {"questionnaires": questionnaires})
def show_music(request):
    # musics[int(content_id) - 1]
    # 假设 musics 是您的数组，content_id 是要移动到开头的元素的索引（从 1 开始）
    content_id_int = int(content_id)  # 将字符串类型的索引转换为整数类型
    # if 1 <= content_id_int <= len(musics):
    # musics.insert(0, musics.pop(content_id_int - 1))
    for music in musics:
        if music["id"] == content_id_int:
            musics.insert(0, musics.pop(musics.index(music)))
            return render(request, "music.html", {"music": musics})
    return render(request, "music.html", {"music": musics})


def reply(request):
    parent_id = request.POST.get("m_id")
    content = request.POST.get("input_content")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(content, global_username, parent_id, formatted_time)
    c.execute(
        "INSERT INTO home_explore (content, author, parent_id,post_time) VALUES (?, ?, ?,?)",
        (content, global_username, parent_id, formatted_time),
    )
    conn.commit()
    conn.close()
    return JsonResponse({"status": "success", "redirect_url": "/show_explore/"})


# def usr(request, token):
#     global global_token
#     global_token = token
#     return render(
#         request,
#         "usr.html",
#         {
#             "token": token,
#             "username": ftoken2account(token),
#             "datasets": get_datasets(token),
#         },
#     )


# def submit_survey(request):
#     return HttpResponse("submit_survey")


# def home(request):
#     global global_dataset_id
#     global global_token
#     if request.method == "POST":
#         dataset_id = request.POST.get("dataset_id")
#         global_dataset_id = dataset_id
#         dataset_name = get_datasets(global_token)[dataset_id]["name"]
#         # print(dataset_name)
#         return redirect(reverse("home"))
#     else:
#         dataset = json.dumps(get_dataset(global_token, global_dataset_id))
#         return render(request, "home.html", {"dataset": dataset})

import datetime


def add_button(request):
    input_content = request.POST.get("input_content")
    input_type = request.POST.get("input_type")
    # print(input_content, input_type)
    if input_type == "diary":
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(
            "INSERT INTO home_diary (title,background) VALUES (?,?)",
            (input_content, "默认"),
        )
        conn.commit()
        conn.close()
    elif input_type == "explore":
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO home_explore (content,author,post_time) VALUES (?,?,?)",
            (input_content, global_username, formatted_time),
        )
        conn.commit()
        conn.close()
    return JsonResponse({"status": "success", "redirect_url": "/login/"})
    # return render(request, "add_button.html")


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
    c.execute("SELECT id,title,weather,mood,background,content FROM home_diary")
    records = c.fetchall()
    for i, record in enumerate(records):
        diaries.append(
            {
                "id": record[0],
                "title": record[1],
                "weather": record[2],
                "mood": record[3],
                "background": record[4],
                "content": record[5],
                "image": "/static/" + record[4] + ".jpg",
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
    records = c.fetchall()
    for record in records:
        if record[4] == None:
            explores.append(
                {
                    "id": record[0],
                    "time": record[1],
                    "name": record[2][:8],
                    "image": "/static/question.jpg",
                }
            )
    return render(
        request,
        "login.html",
        {
            "username": global_username,
            "stations": stations,
            "diaries": diaries,
            "musics": musics,
            "explores": explores,
        },
    )


# # 参考（django）01 django实现前端上传图片到后端保存_django保存图片-CSDN博客.pdf
# def django_upload_data(request):
#     # 由前端指定的name获取到图片数据
#     global global_token
#     global global_dataset_id
#     img = request.FILES.get("img")
#     # 获取图片的全文件名
#     img_name = img.name
#     # 截取文件后缀和文件名
#     mobile = os.path.splitext(img_name)[0]
#     ext = os.path.splitext(img_name)[1]
#     # 重定义文件名
#     img_name = f"{mobile}{ext}"
#     # print(img_name)
#     upload_dir = os.path.join(os.getcwd(), "usr_upload")
#     if not os.path.exists(upload_dir):
#         os.makedirs(upload_dir)
#     img_path = os.path.join(upload_dir, img_name)
#     if not os.path.exists(img_path):
#         # return HttpResponse('File already exists')
#         # 写入文件
#         with open(img_path, "ab") as fp:
#             # 如果上传的图片非常大，就通过chunks()方法分割成多个片段来上传
#             for chunk in img.chunks():
#                 fp.write(chunk)
#         # fp.write(img.read())
#     # 上传到AI库里
#     with open(img_path, "rb") as f:
#         data = f.read()
#     upload_data(global_token, global_dataset_id, [(img_name, data)])
#     # json2sqlite()+
#     return HttpResponseRedirect(reverse("home"))


# def django_delete_data(request):
#     global global_token
#     if request.method == "POST":
#         # 批量删除版本
#         data_id_seq = request.POST.get("delete_data_id")
#         data_id_list = data_id_seq.split(",")
#         for data_id in data_id_list:
#             if data_id == "" or delete_data(global_token, global_dataset_id, data_id):
#                 continue
#             else:
#                 HttpResponse("failue")
#         return redirect(reverse("home"))
#         # 单个删除版本
#         data_id = request.POST.get("delete_data_id")
#         if delete_data(global_token, global_dataset_id, data_id):
#             return redirect(reverse("home"))
#         else:
#             HttpResponse("failue")
#     pass


# def django_create_dataset(request):
#     if request.method == "POST":
#         # 获取提交的数据
#         global global_token
#         dataset_name = request.POST.get("create_dataset_name")
#         # print(token, dataset_name)
#         datasets = get_datasets(global_token)
#         dup = 0
#         for dataset_id, dataset_info in datasets.items():
#             if dataset_info["name"] == dataset_name:
#                 dup = 1
#                 break
#         # 在这里处理你的逻辑，比如保存数据到数据库等
#         if dup == 0:
#             dataset_id = creat_dataset(global_token, dataset_name)
#         # 返回一个简单的响应，你可以根据实际需求进行修改
#         return render(
#             request,
#             "usr.html",
#             {
#                 "dup": dup,
#                 "token": global_token,
#                 "username": ftoken2account(global_token),
#                 "datasets": get_datasets(global_token),
#             },
#         )
#     # 如果是 GET 请求，可以根据实际需求返回一个页面或其他响应
#     return HttpResponse("Invalid request method")


# def django_delete_dataset(request):
#     if request.method == "POST":
#         global global_token
#         account = ftoken2account(global_token)
#         dataset_name = request.POST.get("delete_dataset_name")
#         conn = sqlite3.connect("db.sqlite3")
#         c = conn.cursor()
#         c.execute(
#             "SELECT dataset_id FROM datasets WHERE dataset_name = ? AND account_id = (SELECT id FROM account WHERE username = ?)",
#             (
#                 dataset_name,
#                 account,
#             ),
#         )
#         try:
#             dataset_id = c.fetchone()[0]
#         except:
#             # 删除不存在的数据集
#             return render(
#                 request,
#                 "usr.html",
#                 {
#                     "dup": 0,
#                     "del": 1,
#                     "token": global_token,
#                     "username": ftoken2account(global_token),
#                     "datasets": get_datasets(global_token),
#                 },
#             )
#         conn.close()
#         print(dataset_id)
#         if delete_dataset(global_token, dataset_id):
#             return render(
#                 request,
#                 "usr.html",
#                 {
#                     "dup": 0,
#                     "token": global_token,
#                     "username": ftoken2account(global_token),
#                     "datasets": get_datasets(global_token),
#                 },
#             )
#         else:
#             # HttpResponse('failue')
#             # 删除失败
#             return render(
#                 request,
#                 "usr.html",
#                 {
#                     "dup": 0,
#                     "del": 1,
#                     "token": global_token,
#                     "username": ftoken2account(global_token),
#                     "datasets": get_datasets(global_token),
#                 },
#             )
#     return HttpResponse("Invalid request method")


# def django_rename_dataset(request):
#     global global_token
#     if request.method == "POST":
#         account = ftoken2account(global_token)
#         previous_dataset_name = request.POST.get("previous_dataset_name")
#         new_dataset_name = request.POST.get("new_dataset_name")
#         conn = sqlite3.connect("db.sqlite3")
#         c = conn.cursor()
#         c.execute(
#             "SELECT dataset_id FROM datasets WHERE dataset_name = ? AND account_id = (SELECT id FROM account WHERE username = ?)",
#             (
#                 new_dataset_name,
#                 account,
#             ),
#         )
#         if c.fetchone() != None:
#             # 新重命名的数据集已存在
#             return render(
#                 request,
#                 "usr.html",
#                 {
#                     "dup": 0,
#                     "ren": 2,
#                     "token": global_token,
#                     "username": ftoken2account(global_token),
#                     "datasets": get_datasets(global_token),
#                 },
#             )
#         c.execute(
#             "SELECT dataset_id FROM datasets WHERE dataset_name = ? AND account_id = (SELECT id FROM account WHERE username = ?)",
#             (
#                 previous_dataset_name,
#                 account,
#             ),
#         )
#         try:
#             dataset_id = c.fetchone()[0]
#         except:
#             # 原重命名的数据集不存在
#             return render(
#                 request,
#                 "usr.html",
#                 {
#                     "dup": 0,
#                     "ren": 1,
#                     "token": global_token,
#                     "username": ftoken2account(global_token),
#                     "datasets": get_datasets(global_token),
#                 },
#             )
#         conn.close()
#         if rename_dataset(global_token, dataset_id, new_dataset_name):
#             return render(
#                 request,
#                 "usr.html",
#                 {
#                     "dup": 0,
#                     "ren": 0,
#                     "token": global_token,
#                     "username": ftoken2account(global_token),
#                     "datasets": get_datasets(global_token),
#                 },
#             )
#         else:
#             # 重命名失败
#             return render(
#                 request,
#                 "usr.html",
#                 {
#                     "dup": 0,
#                     "ren": 1,
#                     "token": global_token,
#                     "username": ftoken2account(global_token),
#                     "datasets": get_datasets(global_token),
#                 },
#             )
#     return HttpResponse("Invalid request method")


# def django_research_dataset(request):
#     if request.method == "POST":
#         global global_token
#         global global_dataset_id
#         dataset_name = request.POST.get("research_dataset_name")
#         dataset = {}
#         print(get_datasets(global_token))
#         for key, value in get_datasets(global_token).items():
#             print(value["name"], dataset_name)
#             if value["name"] == dataset_name:
#                 dataset[key] = value
#                 return render(
#                     request,
#                     "usr.html",
#                     {
#                         "rea": 0,
#                         "token": global_token,
#                         "username": ftoken2account(global_token),
#                         "datasets": dataset,
#                     },
#                 )
#         # print(dataset_name)

#         dataset = get_datasets(global_token)
#         return render(
#             request,
#             "usr.html",
#             {
#                 "rea": 1,
#                 "token": global_token,
#                 "username": ftoken2account(global_token),
#                 "datasets": dataset,
#             },
#         )
#     return HttpResponse("Invalid request method")
