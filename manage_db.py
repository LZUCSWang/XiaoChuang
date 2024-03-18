import sqlite3

# 链接数据库
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
quest="""1、我感到情绪沮丧，郁闷。
*2、我感到早晨心情最好。
3、我要哭或想哭。
4、我夜间睡眠不好。
*5、我吃饭象平时一样多。
*6、我的性功能正常。
7、我感到体重减轻。
8、我为便秘烦恼．。
9、我的心跳比平时快。
10、我无故感到疲劳。
*11、我的头脑象往常一样清楚。
*12、我做事情象平时一样不感到困难。
13、我坐卧不安，难以保持平静。
*14、我对未来感到有希望。
15、我比平时更容易激怒。
*16、我觉得决定什么事很容易。
*17．我感到自已是有用的和不可缺少的人。
*18、我的生活很有意义。
19、假若我死了别人会过得更好。
*20、我仍旧喜爱自己平时喜爱的东西。""".split("\n")

reidx = [2,5,6,11,12,14,16,17,18,20]
reopt = [109,110,111,112]
opt_Id=[4,5,6,7]
# 打开questions表并添加内容
for idx,i in enumerate(quest):
    if idx+1 in reidx:
        cursor.execute("INSERT INTO home_question (text,questionnaire_id,option1_id,option2_id,option3_id,option4_id) VALUES (?,?,?,?,?,?)",(i,13,reopt[0],reopt[1],reopt[2],reopt[3]))
    # cursor.execute("INSERT INTO home_question (text,questionnaire_id,option1_id,option2_id,option3_id,option4_id) VALUES (?,?,?,?,?,?)",(i,11,opt_Id[0],opt_Id[1],opt_Id[2],opt_Id[3]))
    else:
        cursor.execute("INSERT INTO home_question (text,questionnaire_id,option1_id,option2_id,option3_id,option4_id) VALUES (?,?,?,?,?,?)",(i,13,4,5,6,7))
    print(i,idx)
conn.commit()

# 关闭数据库连接
conn.close()