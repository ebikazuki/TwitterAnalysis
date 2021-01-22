import os 
import sys
import time
import csv
import twitter
import datetime as dt
import pandas as pd

args = sys.argv

# API情報をセット
t = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
          consumer_secret=os.environ['CONSUMER_SECRET'],
          access_token_key=os.environ['ACCESS_TOKEN_KEY'],
          access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
          )

def GetUserList(word, days=1, mpr=10):
    """
    python-twitterで特定のワードを呟いたユーザーを取得してcsv出力する関数
    第一引数：ワード
    第二引数：遡る日数(max:7)
    第三引数：１リクエスト当たりの取得時間(min)
    """
    
    days = int(days)
    mpr = int(mpr)

    # Pandas.dfの準備
    columns = ['since','until','user']
    df = pd.DataFrame(columns=columns)

    # GetSearchで期間指定するための準備
    until = dt.datetime.now()
    since = until - dt.timedelta(minutes = mpr)

    # いつまでさかぼるかを設定
    end_point = dt.datetime.now() - dt.timedelta(days = days)

    # GetSearchでデータを取得
    while since >= end_point :
    
        all_info = t.GetSearch(term = word + ' lang:ja'
                        + ' since:' + str(since).replace(" ","_").split(".")[0] 
                        + '_JST' + ' until:' 
                        + str(until).replace(" ","_").split(".")[0] 
                        + '_JST',count=100)
    
        # 1リクエスト取得データが100に到達してしまった場合は警告文を表示する
        if len(all_info) == 100:
            print("since:" + str(since).replace(" ","_").split(".")[0]  
                  +" API制限オーバー:mprをもっと小さくしてください ")
    
        # dfにデータを書き込む
        for user_info in all_info:
            df = df.append({'since': str(since).replace(" ","_").split(".")[0] 
                       , 'until': str(until).replace(" ","_").split(".")[0] 
                       , 'user': user_info.user.screen_name},ignore_index=True)
    
        # 制限回避のために5秒まつ
        time.sleep(5)   
        # リクエストが1回終わったら進捗状況を表示する
        print(' since:' + str(since).replace(" ","_").split(".")[0]+"---OK!")
    
        # 取得期間の更新
        until -= dt.timedelta(minutes = mpr)
        since = until - dt.timedelta(minutes = mpr)

    #csvを保存する
    filename = "ユーザーリスト_" + word  + ".csv"
    df.drop_duplicates(subset=['user']).to_csv(filename, encoding="utf-8-sig")

if __name__ == "__main__":
    args.pop(0)
    GetUserList(*args)
