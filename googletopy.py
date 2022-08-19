import gspread
import json
import praw
import emoji

reddit = praw.Reddit()


credentials = {
}


gc = gspread.service_account_from_dict(credentials)
usersbanned = []
banres = []
bandict = {}
st = 0
end = 0

def gsheet():
    global bandict,st,end
    sht2 = gc.open('r/SpamHunting')
    worksheet = sht2.get_worksheet(0)
    length = len(worksheet.col_values(1))
    st = int(input("Enter start row : "))
    while True:        
        if st<1 or st>length:
            st = int(input(f"Enter the value between 0 and {length} : "))
        else:
            break
    end = int(input("Enter end row : "))
    while True:        
        if end<1 or end>length or end<st:
            end = int(input(f"Enter the value between {st} and {length} : "))
        else:
            break
    
        
    for i in range(st,end+1):
        print(i)
        if (worksheet.cell(i, 8).value).lower() == 'yes':
            while True:
                a = input(f"The user {i} is possibly human, do you wish to continue? (y to continue, any other character to ignore user...) : ")
                if a == 'y':
                    usersbanned.append(worksheet.cell(i, 1).value)
                    banres.append(worksheet.cell(i, 4).value)
                    break
                else:
                    break
        else:
            usersbanned.append(worksheet.cell(i, 1).value)
            banres.append(worksheet.cell(i, 4).value)
   
    bandict = dict(zip(usersbanned,banres))
    print("The users and reasons : ")
    print()
    print(json.dumps(bandict, sort_keys=False, indent=4))
    print("-"*100)
    print("Time to start the script "+(emoji.emojize(":grinning_face_with_big_eyes:")))
   



def ban_script():
    print("-"*100)
    for i,j in bandict.items():
        if i:
            for subreddit in reddit.redditor("_Xyreo_").moderated():
                try:
                    reddit.subreddit(subreddit.display_name).banned.add(i, ban_reason=j)
                    print(f"{i} banned in {subreddit} for {j} - Xyreo")
                except:
                    continue
            print()
            print(f"Globally banned {i}...")
            print("-"*100)


     
gsheet()
ban_script()
    
