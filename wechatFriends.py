import itchat
import pickle

# 登录
itchat.login()
# 获取好友，返回好友信息字典
my_friends = itchat.get_friends(update=True)[0:]

# 持久化
with open('my_friends.pickle', 'wb') as e:
    pickle.dump(my_friends, e)