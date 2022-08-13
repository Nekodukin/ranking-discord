# coding: utf-8
import discord
import random
import time
import bisect
from datetime import datetime
from discord.ext import tasks

# client
client = discord.Client()

# 書き込み数ランキング用
resflag = "✨今日の書き込み数ランキング✨"
medflag = "✨中間発表✨"
author_dic = {}

# 書き込み数ランキング用の辞書追加関数
def add_dic(author):
    if not author in author_dic:
        author_dic[author] = 1
    else:
        author_dic[author] += 1

# 起動時に発動
CHANNEL_ID = 694389838404780123
@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("ランキングはリセットされました😭")        
        
# 発言時に発動
@client.event
async def on_message(message):
    if message.author.bot and message.content != resflag and message.content != medflag:
        return
    # 書き込みカウント（先頭に置かないとpermissionError発生時にカウントされない）
    add_dic(message.author)
    # 「!ハイボール」と発言したらランダムで比率が返る処理
    if message.content == '!ハイボール':
        rand = random.randint(1, 1000)
        prb1 = [300,500,650,750,830,890,945,980]
        rate = bisect.bisect_left(prb1, rand) + 1
        await message.channel.send(str(10-rate)+":"+str(rate))
    # 特定の人物の発言にリアクションを付ける
    users1 = []
    if str(message.author) in users1:
        #print(message.content)
        await message.add_reaction("<:gai:640187532214272020>")
    users2 = [] # "ken#6347"
    if str(message.author) in users2:
        await message.add_reaction("<:kenkusa:711930005243822211>")
    user3 = ["和ちゃん#9589"]
    if str(message.author) in user3:
        await message.add_reaction("🦊")
    tester = ["L_#9273"]
    if str(message.author) in tester and message.content == "Test":
        await message.add_reaction("\N{THUMBS UP SIGN}")
    # 特定の発言でスリープする
    if message.content == "!sleep":
        await message.channel.send("1時間後にまた来るで")
        time.sleep(3600)
    # !omikuji機能
    if message.content == "!omikuji":
        rand = random.randint(1, 50000)
        prb2 = [10000, 14000, 17000, 20000, 23000, 27000, 27200, 31000, 31200, 34000, 36500, 40000, 40350, 40440, 40540, 40800,
                40900, 41000, 41100, 41200, 41300, 41550, 41800, 41900, 42200, 42400, 42500, 42600, 43600, 43700, 43800, 44000,
                44150, 44250, 44350, 44650, 44800, 44900, 45100, 45200, 45600, 47000, 47100, 47300, 47700, 47900, 48100, 48200,
                48400, 48600, 48800, 49000, 49200, 49400, 49600, 49800, 49939, 49989, 49999]
        result = ["【大吉】", "【吉】", "【中吉】", "【小吉】", "【末吉】", "【凶】", "【中凶】", "【大凶】", "【末凶】", "【豚】", "【ぴょん吉】", "【だん吉】",
                  "【かん吉】", "【松】", "【鶴】", "【梅】", "【目白】", "【桜】", "【ほととぎす】", "【菖蒲】", "【牡丹】", "【蝶】", "【猪】", "【坊主】", "【月】",
                  "【菊】", "【盃】", "【紅葉】", "【鹿】", "【柳】", "【おっさん】", "【犬】", "【にゃあ】", "【桐】", "【鳳凰】", "【小野道風】", "【不如帰】",
                  "【ﾆﾀﾞｰ】", "【髪】", "【ゾヌ】", "【腐女子】", "【男の娘】", "【姫君】", "【底辺】", "【上級国民】", "【下級国民】", "【ボブ】", "【チーバくん】",
                  "【ken】", "【天江衣】", "【ウオウオフィッシュライフ】", "【ねず】", "【!KTU】", "【TAKE】", "【ペンタキル】", "【のび太】", "【千葉商科大学】",
                  "【神】", "【女神】", "【尊師】"]
        await message.channel.send(result[bisect.bisect_left(prb2, rand)])
        if rand == 50000:
            await message.add_reaction("🎉")

    # 書き込み数ランキング用
    # !ranking n
    if "!ranking" in message.content and len(message.content.split()) == 2:
        dic_list = list(map(list, list(author_dic.items())))
        dic_list.sort(key=lambda x: x[1], reverse=True)
        for author, times in dic_list:
            if author.bot:
                dic_list.remove([author, times])
        wantrank = int(message.content.split()[1])
        Topwantrank = []
        for i in range(len(dic_list)):
            author = dic_list[i][0]
            if author.nick == None:
                author_name_ = author.name
            else:
                author_name_ = author.nick
            Topwantrank.append([author_name_, dic_list[i][1], i + 1])
        for m in range(1, len(dic_list)):
            if Topwantrank[m][1] == Topwantrank[m - 1][1]:
                Topwantrank[m][2] = Topwantrank[m - 1][2]
        wantrank = Topwantrank[wantrank-1][2]
        Topwantrank_ver2 = []
        for m in range(len(Topwantrank)):
            if Topwantrank[m][2] == wantrank:
                Topwantrank_ver2.append(str(Topwantrank[m][2])+"位："+Topwantrank[m][0]+"（書き込み数："+str(Topwantrank[m][1])+"）")
        res_ = ""
        for j in Topwantrank_ver2:
            res_ += j
            res_ += "\n"
        await message.channel.send(res_)

    # !myrank
    if message.content == "!myrank":
        dic_list = list(map(list, list(author_dic.items())))
        dic_list.sort(key=lambda x: x[1], reverse=True)
        for author, times in dic_list:
            if author.bot:
                dic_list.remove([author, times])
        hisrank = 0
        for i in range(len(dic_list)):
            if dic_list[i][0] == message.author:
                hisrank = i
                break
        Tophisrank = []
        for i in range(hisrank+1):
            author = dic_list[i][0]
            if author.nick == None:
                author_name_ = author.name
            else:
                author_name_ = author.nick
            Tophisrank.append([author_name_, dic_list[i][1], i+1])
        for m in range(1, hisrank+1):
            if Tophisrank[m][1] == Tophisrank[m-1][1]:
                Tophisrank[m][2] = Tophisrank[m-1][2]
        await message.channel.send(str(Tophisrank[hisrank][2]) + "位：" + Tophisrank[hisrank][0] + "（書き込み数：" + str(Tophisrank[hisrank][1]) + "）")

    # !ranking
    if message.content == "!ranking":
        await message.channel.send(medflag)
    if (message.content == resflag or message.content == medflag) and message.author.bot:
        dic_list = list(map(list, list(author_dic.items())))
        dic_list.sort(key=lambda x:x[1], reverse=True)
        for author, times in dic_list:
            if author.bot:
                dic_list.remove([author, times])
        Top5 = dic_list[:5]
        Top5_ver1 = []
        Top5_ver2 = []
        l = len(Top5)
        i = 1
        for author, times in Top5:
            if author.nick == None:
                author_name = author.name
            else:
                author_name = author.nick
            Top5_ver1.append([author_name, times, i])
            i += 1
        for m in range(1, l):
            if Top5_ver1[m][1] == Top5_ver1[m-1][1]:
                Top5_ver1[m][2] = Top5_ver1[m-1][2]
        for m in range(l):
            Top5_ver2.append(str(Top5_ver1[m][2])+"位："+Top5_ver1[m][0]+"（書き込み数："+str(Top5_ver1[m][1])+"）")
        res = ""
        for j in Top5_ver2:
            res += j
            res += "\n"
        await message.channel.send(res)

# 書き込み数ランキングの発表時間
CHANNEL_ID = 694389838404780123
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '23:59':
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(resflag)
    if now == '00:00':
        author_dic.clear()


# 実行
loop.start()
client.run('TOKEN')