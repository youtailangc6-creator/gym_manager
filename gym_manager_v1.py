from datetime import date

def pause():
    input("\nEnterキーでメニューに戻ります")

def save_weights(weights):
    text=",".join(map(str,weights))
    with open("weights.txt","w")as file:
        file.write(text)

    print("記録を保存しました")
    print("保存内容:",text)

def load_weights():
    try:
        with open("weights.txt","r")as file:
            text=file.read()
    except FileNotFoundError:
            print("ファイルがないため空の記録で開始します")
            return[]
    
    if text=="":
        return[]
    items=text.split(",")
    weights=[]

    for item in items:
        weights.append(int(item))

    return weights

weights=load_weights() 

def show_menu():    
    print()
    print("="*38)
    print(".    Gym Manager Ver.1.0")
    print("="*38)

    print("1. 重量追加")
    print("2. 集計結果を見る")
    print("3. 記録一覧を見る")
    print("4. 番号を選んで記録削除")
    print("5. 番号を選んで修正")
    print("6, 推定1RMを計算")
    print("7. 1RM 履歴を見る")
    print("8. 1RMの集計を見る")
    print("9. 1RM成長を見る")
    print("10. 1RMの履歴を削除する")
    print("11. トレーニング履歴を見る")
    print("12. 終了")

    print("="*38)

def input_weight():
    while True:
        new_weight=input("重量を入力してください:")

        if new_weight.lstrip("-").isdigit():
          weight=int(new_weight)

          if weight<=0:
             print("1kg以上を入力してください")
          else:
             return weight

        else:
           print("数字を入力してください")    

def add_weight(weights):
    weight=input_weight() 
    weights.append(weight)
    print(weight,"kgを追加しました")

def show_summary(weights):
    if len(weights)==0:
        print("記録はありません")
        return 
    
    print("集計処理を続けます")

    count=0
    total=0
    best=weights[0]    
    worst=weights[0]

    for weight in weights:
        total=total+weight

        if weight>=60:
            count=count+1

        if weight>best:
            best=weight

        if weight<worst:
            worst=weight

    avg=total/len(weights)

    print("===== 集計結果 =====")
    print("記録件数:",len(weights),"件")
    print("合計重量:",total,"kg")
    print("平均重量:",round(avg,1),"kg")
    print("最高重量:",best,"kg")
    print("最低重量:",worst,"kg")
    print("60kg以上:",count,"件")

def show_records(weights):
    if len(weights)==0:
        print("記録はありません")
        return

    avg=sum(weights)/len(weights)

    print("===== 記録一覧 =====")
    for weight in weights:
        if weight>=avg:
          print(weight,"kg→平均以上")   
        else:
          print(weight,"kg→平均未満")    

def show_numbered_records(weights):
    if len(weights)==0:
        print("記録はありません")
        return
    
    print("===== 記録一覧 =====")

    for number,weigtht in enumerate(weights,start=1):
        print(number,":",weigtht,"kg")

def remove_selected_weight(weihts):
    if len(weights)==0:
        print("記録はありません")
        return

    show_numbered_records(weights)

    number=int(input("削除したい番号は？:"))

    if 1<=number<=len(weights):
        deleted_weight=weights.pop(number-1)
        print(deleted_weight,"kgを削除しました")
 
    print("現在の記録:",weights)

def update_selected_weight(weights):
    if len(weights)==0:
        print("記録はありません")
        return
    
    print("===== 記録一覧 =====")

    for number,weight in enumerate(weights,start=1):
        print(number,":",weight,"kg")

    number=int(input("修正したい番号は？:"))    

    if 1<=number<=len(weights):
        old_weight=weights[number-1]
        new_weight=int(input("新しい重量は？:"))
        weights[number-1]=new_weight
        print(old_weight,"kgを",new_weight,"kgに変更しました")
        print("現在の記録:",weights)
    else:
        print("正しい番号を入力してください:")


weights=load_weights()
print("現在の記録:",weights)

def calculate_1rm():
    while True:
            try:
                weight=float(input("重量を入力してください:"))
                if weight<=0:
                    print("1kg以上を入力してください:")
                    continue
                break
            except ValueError:
                print("数字を入力してください")
    
    while True:
            try:
                reps=int(input("回数を入力したください:"))
                if reps<=0:
                    print("1回以上を入力してください:")
                    continue
                break
            except ValueError:
                print("数字を入力してください:")  
    

    max_weight=weight*(1+reps/30)
    max_weight=round(max_weight,1)

    print("推定MAX:", max_weight,"kg")

    return weight,reps,max_weight

def save_workout_record(weight,reps,max_weight):
    today=date.today()
    record=f"{today},{weight},{reps},{max_weight}"
    with open("workout_history.csv","a")as file:
        file.write(str(record)+"\n")
    print("日付付き記録を保存しました")

def save_1rm(max_weigth):
    with open("one_rm_history.txt","a")as file:
        file.write(str(max_weigth)+"\n")
    print("1RM履歴へ保存しました")  

def show_1rm_history():
    with open("one_rm_history.txt","r")as file:
      history=file.readlines()

    if len(history)==0:
        print("履歴はありません")
        return
    
    print("===== 1RM履歴 =====")

    for number,max_weight in enumerate(history,start=1):
        max_weight=max_weight.strip()
        print(number,".",max_weight,"kg")

def show_1rm_summary():
    with open("one_rm_history.txt","r")as file:
        history=file.readlines()

    if len(history)==0:
            print("履歴はありません")
            return 

    one_rm_list=[]

    for max_weight in history:
        max_weight=max_weight.strip()
        one_rm_list.append(float(max_weight))

        
    avg=sum(one_rm_list)/len(one_rm_list) 
    avg=round(avg,1)

    
    print("===== 1RM集計 =====")
    print("記録件数:",len(one_rm_list),"件")    
    print("最高1RM:",max(one_rm_list),"kg")
    print("平均1RM",avg,"kg)")

def show_1rm_progress():    
    with open("one_rm_history.txt","r")as file:
            history=file.readlines()

    if len(history)<2:
        print("比較できません")
        return

    one_rm_list=[]

    for max_weight in history:
         max_weight=max_weight.strip()
         one_rm_list.append(float(max_weight))

    first=one_rm_list[0]
    latest=one_rm_list[-1]

    dif=latest-first 
    dif=round(dif,1)

    print("===== 1RM成長記録 =====")
    print("最初の1RM:",first,"kg")  
    print("最新の1RM:",latest,"kg")
    print(f"変化:{dif:+.1f}kg")
          

    if dif>0:
        print("成長してます")
    elif dif<0:
        print("最初の記録を下回ってます")
    else:
        print("変化はありません")
def remove_selected_1rm():
    with open("one_rm_history.txt","r")as file:
            history=file.readlines()

    if len(history)==0:
        print("履歴はないです")
        return

    print("===== 1RM履歴 =====")

    for number,max_weight in enumerate(history,start=1):
        max_weight=max_weight.strip()
        print(number,".",max_weight,"kg")

    while True:
        try:
            deleted_number=int(input("削除する番号は？"))
            if 1<=deleted_number<=len(history):
                deleted=history.pop(deleted_number-1)
                break

            print("正しい番号を入力してください")

        except ValueError:
            print("数字を入力してください") 

    with open("one_rm_history.txt","w")as file:
        file.writelines(history)

    deleted=deleted.strip()
    print(deleted,"kgを削除しました")

def show_workout_history():
    try:
        with open("workout_history.csv","r")as file:
            history=file.readlines()

    except FileNotFoundError:
        print("トレーニング履歴はありません")
        return


    if len(history)==0:
        print("トレーニング履歴はありません")
        return

    print("===== トレーニング履歴 =====")
    for number,record in enumerate(history,start=1):
        record=record.strip()
        parts=record.split(",")

        if len(parts)!=4:
            print(f"{number}行目は形式が不正なのでスキップします")
            continue

        date,weight,reps,max_weight=parts
        
        print(f"{number}.{date}|{weight}kg x {reps}回"f"|推定1RM{max_weight}kg")
        
while True:
    show_menu()

    choice=input("番号を入力してください:")  

    if choice=="1":
        add_weight(weights) 

    elif choice=="2":
        show_summary(weights)  

    elif choice=="3":
        show_records(weights)  

    elif choice=="4":
        remove_selected_weight(weights)      

    elif choice=="5":
        update_selected_weight(weights)

    elif choice=="6":
        weight,reps,max_weight=calculate_1rm() 

        save_1rm(max_weight) 
        save_workout_record(weight,reps,max_weight)

    elif choice=="7":
        show_1rm_history()

    elif choice=="8":
        show_1rm_summary() 

    elif choice=="9":
        show_1rm_progress()  

    elif choice=="10":
        remove_selected_1rm()

    elif choice=="11":
        show_workout_history()    
         
    elif choice=="12":
        save_weights(weights)
        print("終了")
        break

    else:
        print("1~12の番号を入力してください:")

    pause()    








