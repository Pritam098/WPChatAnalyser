import matplotlib.pyplot as plt 

def fun(day,mon,year):
	if(year%4==0 and year%100!=0) or year%400==0:
		x=29
	else:
		x=28
	dict_fun={1:31,2:x,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
	arr_fun=[31,x,31,30,31,30,31,31,30,31,30,31]
	for i in range(1,len(arr_fun)):
		arr_fun[i]+=arr_fun[i-1]
	if mon!=1:
		return day+arr_fun[mon-2]
	else:
		return day
print('Enter path to your file')
file=input()
print("WhatsApp Chat Analyzer!")
f=open(file,encoding="utf8")

k=list()
admins=set()
timestamp=[]
msglog=[]
date=[]
time=[]
dates={}

dict={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}


##split and store data
for  i in f.readlines():
	k.append(i.split('-'))

for i in k:
	if(len(i)>=2):
		if i[0].count('/')==2 and i[0].count(',')!=0:
			temp=''
			for k in range(1,len(i)):
				temp+=i[k]
			if temp.find(':')!=-1:
				msglog.append(temp)
				timestamp.append(i[0])
			elif temp.find('added')!=-1:
				admins.add(temp[:temp.find('added')])
			elif temp.find('created')!=-1:
				admins.add(temp[:temp.find('created')])
		else:
			temp=''
			temp+=msglog[len(msglog)-1]
			temp+='\n'+i[0]
			msglog[len(msglog)-1]=temp
	else:
		temp=''
		temp+=msglog[len(msglog)-1]
		temp+='\n'+i[0]
		msglog[len(msglog)-1]=temp


for i in timestamp:
	temp=i.split(',')
	date.append(temp[0])
	time.append(temp[1])


for i in date:
	if dates.get(i,-1)==-1:
		dates[i]=1
	dates[i]+=1

o=0
for key in dates:
	if o==0:
		mx_dates=key
		o+=1
		continue
	if dates[key]>dates[mx_dates]:
		mx_dates=key
t=mx_dates.split('/')
most_active_day=t[1]+' '+dict[int(t[0])]+' 20'+t[2]
print('Most active date:-  {}'.format(most_active_day))
print('Number of messages on {}= {}'.format(most_active_day,dates[mx_dates]))


day=[]
month=[]
year=[]
for i in date:
	temp=i.split('/')
	month.append(int(temp[0]))
	day.append(int(temp[1]))
	year.append(int(temp[2]))

mon_cnt=[]
for i in range(1,13):
	mon_cnt.append(0)
for i in month:
	mon_cnt[i-1]+=1
max_month_msg=max(mon_cnt)
max_month=mon_cnt.index(max_month_msg)+1

print('Most active month:- {}'.format(dict[max_month]))
print('Number of messages in {}'.format(dict[max_month],max_month_msg))

#code to split msglog to store users and messages and for most active user

users=set() #to store phone no
users_cnt={} 

for i in msglog:
	contact=''
	ind=i.index(":")
	contact+=i[:ind]
	users.add(contact.strip)
	if users_cnt.get(contact,-1)==-1:
		users_cnt[contact]=[]
	users_cnt[contact].append(i[ind+1:])

#code for most active user

nmsg=-1
mxuser='-1'
for key in users_cnt:
	if len(users_cnt[key])>nmsg:
		mxuser=key
		nmsg=len(users_cnt[key])

print('Overall, most active user:- {},has posted {}messages in this group'.format(mxuser,nmsg))


print('List of active admins in this group:-')
for i in admins:
	print(i)
print('Number of users:- {}'.format(len(users_cnt)))
#print('List of all users:-')


#code for words per user for each user#
nwords_per_user={}
for key in users_cnt:
	nwords=0
	nmsg=len(users_cnt[key])
	for i in users_cnt[key]:
		nwords+=len(i)
	nwords_per_user[key]=nwords//nmsg
for i in nwords_per_user:
	print('{} -{}'.format(i,nwords_per_user[i]))
word_dict={}
chars=['.','/','"',';',':','=','+','-','*','!','@','#','&',',','?','<','>','(',')','[',']','{','}','^','%','$','_','|']
for key in users_cnt:
	for i in users_cnt[key]:#i iterates over messages
		temp=i.split()#temp is list of unfiltered words in msg
		for j in range(len(temp)):#filter ./'";:=+ etc
			temp2=list(temp[j])#temp[j] is  a word

			for ch in chars:
				while True:
					if ch in temp2:
						temp2.remove(ch)
					else:
						break

			st=''
			for h in temp2:
				st+=h
			temp[j]=st
		for word in temp:
			if word_dict.get(word,-1)==-1:
				word_dict[word]=1
			else:
				word_dict[word]+=1

#code for most used word
best_word_cnt=0
for i in word_dict:
	if word_dict[i]>best_word_cnt:
		best_word_cnt=word_dict[i]
		best_word=i
print('Most used word here is {},used {} times'.format(best_word,best_word_cnt))

## code to plot no of messages per Day
plotting_years=[]
j=0
duy=[0]*367
for i in range(len(duy)):
	duy[i]=i+1
start=date[0][2]
arr_plot=[]
i=0
import numpy as np 
while i<len(date):
	start=date[i].split('/')[2]
	temp=[0]*367
	while i<len(date) and date[i].split('/')[2]==start:
		m,d,y=[int(k) for k in date[i].split('/')]
		temp[fun(d,m,y)]+=1
		i+=1
	arr_plot.append(temp)
lll=1
for i in arr_plot:
	plt.plot(duy,i,label=str(lll)+' year')
	lll+=1
plt.xlabel('Day in year (out of 365/366)')
plt.ylabel('No. of messages')
plt.title('No .of messages/Day')
plt.legend()
plt.show()


#code for pie chart of top 5 users

nmsg_per_user={}
for i in users_cnt:
	nmsg_per_user[i]=len(users_cnt[i])
sorted_users_cnt=sorted(nmsg_per_user,key=nmsg_per_user.__getitem__,reverse=True)
top_five_users=[]
cols=['c','r','b','m','g']

for i in range(5):
	top_five_users.append([sorted_users_cnt[i],nmsg_per_user[sorted_users_cnt[i]]])
plt.pie([i[1] for i in top_five_users],labels=[i[0] for i in top_five_users],colors=cols,startangle=90,shadow=True,autopct='%1.1f%%',explode=(.1,0,0,0,0),radius=.8)

plt.title('Top 5 Active users...!!!')
plt.legend(loc=(.65,-12))
plt.show()

f.close()
#code for time


