# -*-coding:utf-8-*-
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import urllib
import os
import test

class LuooSpider:
    def __init__(self, root):
        self.websit = 'http://luoomp3.kssws.ks-cdn.com/low/luoo/radio'
        self.localPath = './music'
        self.LatestPeriodicalNum='0'
        self.periodicalNum='0'
        self.periodicalName = ''
        self.songAmount = '0'
        ########################1.main window#########################
        root.title("落网专辑下载工具")
        #root.iconbitmap('luoo1.ico')
        root.resizable(width=FALSE, height=FALSE)
        menu=Menu(root)
        root.config(menu=menu)
        ########################2.menu#########################
        ########################2.1 mainMenu#########################
        settingMenu = Menu(menu)
        helpMenu = Menu(menu)
        infoMenu = Menu(menu)
        menu.add_cascade(label="设置", menu=settingMenu)
        menu.add_cascade(label="帮助", menu=helpMenu)
        menu.add_cascade(label="说明", menu=infoMenu)
        ########################2.2 settingMenu#########################
        ########################2.2.1 languageMenu#########################
        def chooseChinese():
            messagebox.showinfo("语言/Language","已选择中文，重启后生效")
        def chooseEnglish():
             messagebox.showinfo("Language Choose","have chosed English,restart to be available")
        def setNewPath():
             printInTextWidge("当前下载路径为："+self.localPath+'\n',Tview)
             wd = Toplevel(root)
             wd.title("下载路径")
             #root.iconbitmap('luoo1.ico')
             wd.resizable(width=FALSE, height=FALSE)
             L = Label(wd,text="请输入下载路径\n例如：/home/username/Music")
             E = Entry(wd)
             E.insert(10,self.localPath)
             B = Button(wd,text='确认',command=lambda:writeToPath(E.get()))
             L.grid(row=0,column=0,rowspan=2,columnspan=10,sticky=NSEW)
             E.grid(padx=5,row=2,column=0,rowspan=1,columnspan=5,sticky=NSEW)
             B.grid(row=2,column=5,rowspan=1,columnspan=5,sticky=NSEW)
        def writeToPath(text):
            self.localPath=text
            printInTextWidge("已成功设置路径为："+self.localPath+'\n',Tview)
        def setDefaultPath():
             printInTextWidge("当前下载路径为："+self.localPath+'\n',Tview)
             wd = Toplevel(root)
             wd.title("恢复默认下载路径")
             #root.iconbitmap('luoo1.ico')
             wd.resizable(width=FALSE, height=FALSE)
             writeToPath('./music')
             L = Label(wd,text="已经恢复为默认下载路径:\n./music",height=8,width=20)
             L.grid(padx=10,row=0,column=0,rowspan=2,columnspan=10)

        languageMenu=Menu(settingMenu)
        settingMenu.add_cascade(label="语言/Language", menu=languageMenu)
        languageMenu.add_command(label="中文", command=chooseChinese)
        languageMenu.add_command(label="English", command=chooseEnglish)
        ########################2.2.2 downloadAddressMenu#########################
        downloadAddressMenu=Menu(settingMenu)
        settingMenu.add_cascade(label="下载路径", menu=downloadAddressMenu)
        downloadAddressMenu.add_command(label="设置新路径", command=setNewPath)
        downloadAddressMenu.add_command(label="恢复默认路径", command=setDefaultPath)
        ########################2.3 helpMenu#########################
        def helpInfo():
            messagebox.showinfo("帮助说明","智商25以上均可根据提示操作")

        helpMenu.add_command(label="帮助说明", command=helpInfo)
        ########################2.4 infoMenu#########################
        def aboutAuthor():
             ("关于作者","邮箱：charlieshao518@gmial.com\n博客：www.charlieshao.com")
        def versionInfo():
            messagebox.showinfo("版本说明","V1.0，2015年10月25日")
        def copyRight():
            messagebox.showinfo("版权信息","本软件仅用于测试，请勿用于商业用途，歌曲版权归落网或唱片公司所有。")

        infoMenu.add_command(label="关于作者", command=aboutAuthor)
        infoMenu.add_command(label="版本说明", command=versionInfo)
        infoMenu.add_command(label="版权信息", command=copyRight)
        ########################3.interface#########################
        def reFreshPeridicalList(textWidget):
            filPath='albumList.txt'
            if not os.path.exists(filPath):
                 open(filPath, 'w').close()
            f = open(filPath,'r',encoding='utf-8')
            textWidget.delete('1.0','end')
            textWidget.insert('1.0',f.read())
            f.close()
            textWidget.update_idletasks()

        def WriteToPeridicalList(periodicalNum,textWidget):
           periodiaclName=getPeriodiaclName(periodicalNum)
           filPath='albumList.txt'
           if not os.path.exists(filPath):
                 f=open(filPath, 'w')
                 f.write(periodicalNum+'.'+periodiaclName+'\n')
                 f.close()
           else:
               f = open(filPath,'r+',encoding='utf-8')
               albumLists=f.readlines()
               print(albumLists)
               f.close()
               lineNum=0
               for line in albumLists:
                   numInList=line.split('.')[0]
                   print('numInList:'+numInList)
                   if int(periodicalNum)>int(numInList):
                       albumLists.insert(int(lineNum), periodicalNum+'.'+periodiaclName+'\n')
                       print(periodicalNum+'.'+periodiaclName)
                       print(albumLists)
                       f = open(filPath, "w")
                       #albumLists = "".join(albumLists)
                       for item in albumLists:
                         f.write("%s" % item)
                       f.close()
                       reFreshPeridicalList(textWidget)
                       return True
                   elif int(periodicalNum)==int(numInList):
                       print('专辑号码已经存在，无需再次写入')
                       return False
                   lineNum+=1
               albumLists.append(periodicalNum+'.'+periodiaclName+'\n')
               print(periodicalNum+'.'+periodiaclName)
               print(albumLists)
               f = open(filPath, "w")
               #albumLists = "".join(albumLists)
               for item in albumLists:
                   f.write("%s" % item)
               f.close()
               reFreshPeridicalList(textWidget)
               return True

        def getLatestPeriodicalNum():
             # get the html
            numberUrl = 'http://www.luoo.net'
            numberResponse = requests.get(numberUrl)
            numberResponse.encoding = 'utf-8'
            numberSoup = BeautifulSoup(numberResponse.text, "html.parser")
            # parse the html and get the number
            numberText = (numberSoup.find_all('div', 'vol-item-lg')[0]).text
            LatestPeriodicalNum = re.findall(r'\d+', numberText)[0]
            return LatestPeriodicalNum
        #2015.10.25 read periodicalName Amount
        def getPeriodiaclName(periodicalNum):
            periodicalUrl= 'http://www.luoo.net/music/'+ periodicalNum
            periodicalResponse = requests.get(periodicalUrl)
            periodicalResponse.encoding = 'utf-8'
            periodicalSoup = BeautifulSoup(periodicalResponse.text, "html.parser")
            # parse the html and get the number
            periodicalName = (periodicalSoup.find_all("span",class_="vol-title")[0]).string
            return periodicalName

        def getPeriodiaclSongNames(periodicalNum):
            periodicalUrl= 'http://www.luoo.net/music/'+ periodicalNum
            periodicalResponse = requests.get(periodicalUrl)
            periodicalResponse.encoding = 'utf-8'
            periodicalSoup = BeautifulSoup(periodicalResponse.text, "html.parser")
            # parse the html and get the number
            periodicalNames = periodicalSoup.find_all("a",class_="trackname btn-play").text.split('. ')[1]
            for periodicalName in periodicalNames:
                print(periodicalNames[-1].string.split('. ')[0])

        def downloadFile(url, urlLocal):
            html = urllib.request.urlopen(url)
            code = html.getcode()
            if code == 200:
                print("The request is successful! start download:"+urlLocal)
                urllib.request.urlretrieve(url, urlLocal)
                return True
            else:
                print("The request is failed! Error code: %d"%code)
                return False
        def downloadPeriodiacl(websit,localPath,periodicalNum, Warning_Enable=1):
                if WriteToPeridicalList(periodicalNum,T)==False:
                    if Warning_Enable==1:
                        messagebox.showinfo('Warning','Periodiacl Has been download before, please check the file!')
                    return False
                else:
                    #read periodicalName Amount
                    periodicalUrl= 'http://www.luoo.net/music/'+ periodicalNum
                    periodicalResponse = requests.get(periodicalUrl)
                    periodicalResponse.encoding = 'utf-8'
                    periodicalSoup = BeautifulSoup(periodicalResponse.text, "html.parser")# parse the html and get the number
                    if periodicalSoup==None:
                        return False
                    periodicalName = (periodicalSoup.find_all("span",class_="vol-title")[0]).string
                    if periodicalName==None:
                        return False
                    #periodicalSongAmount = periodicalSoup.find_all("a",class_="trackname btn-play")[-1].string.split('. ')[0]
                    periodicalSongNames =  periodicalSoup.find_all("a",class_="trackname btn-play")
                    for periodicalSongName in periodicalSongNames:
                        songName= periodicalSongName.string.replace(' ','')
                        numNameList= songName.split('.')
                        sourceFilePath = websit+periodicalNum+'/'+numNameList[0]+'.mp3'
                        print(sourceFilePath)
                        fileName=periodicalNum+'.'+periodicalName +'/'+ songName + '.mp3'
                        localFilePath = localPath+'/'+fileName
                        printInTextWidge(fileName+'\n',Tview)
                        directory = os.path.dirname(localFilePath)
                        if not os.path.exists(directory):
                             os.makedirs(directory)
                        print(localFilePath)
                        downloadFile(sourceFilePath, localFilePath)
                    return True


        def donwloadLatesPeriodiacl(websit,localPath):
            latestPeriodicalNum= getLatestPeriodicalNum()
            latestPeriodicalName= getPeriodiaclName(latestPeriodicalNum)
            if WriteToPeridicalList(latestPeriodicalNum,T)==False:
                 messagebox.showinfo('Warning','the latest Periodiacl Has been download before, please check the file!')
            else:
                messagebox.showinfo("信息", "检测到新专辑"+latestPeriodicalNum+'.'+ '<'+latestPeriodicalName+'>'+"点击OK开始下载！")
                downloadPeriodiacl(self.websit,self.localPath,latestPeriodicalNum)
                return True

        def donwloadAllAlbums(buttonWidgt,wd):
            #buttonWidgt.config(text='完成本期后停止')
            latestPeriodicalNum=getLatestPeriodicalNum()
            print(latestPeriodicalNum)
            if messagebox.askyesno('确认', '下载全部专辑将花费很长时间，点击Yes开始下载？'):
                #wd.destroy
                print(latestPeriodicalNum)
                for num in range(1,int(latestPeriodicalNum)):#from the latest to the earliest
                    downloadPeriodiacl(self.websit,self.localPath,str(int(latestPeriodicalNum)-num+1),0)

            else:
                messagebox.showinfo('No', '放弃下载全部专辑')

        def readFromTextWidget(textWidget,wd):
            input = textWidget.get("1.0",END)
            messagebox.showinfo("信息", "即将开始下载专辑："+input)
            wd.destroy()
            print(input.find('-'))
            if input.find('-')==-1:
                nums=list(map(int, re.findall(r'\d+', input)))
                if len(nums)>=1:
                    printInTextWidge("开始下载专辑："+str(nums)+"\n",Tview)
                    for num in nums:
                        downloadPeriodiacl(self.websit,self.localPath,str(num),0)
                else:
                    printInTextWidge("输入格式错误，请重新输入",Tview)
            else:
                nums=list(map(int, re.findall(r'\d+', input)))
                if len(nums)==2:
                    for n in range(int(nums[0]),int(nums[1])):
                        downloadPeriodiacl(self.websit,self.localPath,str(n),0)
                else:
                    printInTextWidge("输入格式错误，请重新输入",Tview)

        def downloadSomeAlbum():
             wd = Toplevel(root)
             wd.title("下载某期专辑")
             #root.iconbitmap('luoo1.ico')
             wd.resizable(width=FALSE, height=FALSE)
             L = Label(wd,text="请在文本框输入要下载的专辑号码\n例如：6或7,8,9或10-50")
             T = Text(wd,height=2,width=20)
             B = Button(wd,text='开始下载',command=lambda:readFromTextWidget(T,wd))
             L.grid(row=0,column=0,rowspan=1,columnspan=5)
             T.grid(padx=5,row=1,column=0,rowspan=2,columnspan=5,sticky=NSEW)
             B.grid(row=3,column=0,rowspan=1,columnspan=5)



             #messagebox.showinfo("信息", "请在文本框输入专辑号码，例如：6或7,8,9或10-50")
        def printInTextWidge(text,textWidget):
            textWidget.insert('1.0',text)
            root.update_idletasks()
        L = Label(root,text="已下载专辑")
        T = Text(root,height=15,width=40)
        S = Scrollbar(root)
        L.grid(row=0,column=0,rowspan=2,columnspan=12,sticky=NSEW)
        T.grid(row=2,column=0,rowspan=10,columnspan=10,sticky=NSEW)
        S.grid(row=2,column=11,rowspan=10,columnspan=1,sticky=NSEW)
        T.config(yscrollcommand=S.set)
        S.config(command=T.yview)

        B1 = Button(root, text='下载最新专辑',command=lambda:donwloadLatesPeriodiacl(self.websit,self.localPath))
        B2 = Button(root, text='下载某期专辑',command=downloadSomeAlbum)
        B3 = Button(root, text='下载全部专辑',command=lambda:donwloadAllAlbums(B3,root))
        Tview = Text(root,height=3,width=4)
        Sview= Scrollbar(root)
        Tview.config(yscrollcommand=Sview.set)
        Sview.config(command=Tview.yview)
        B1.grid(row=12,column=0,rowspan=4,columnspan=4,sticky=NSEW)
        B2.grid(row=12,column=4,rowspan=4,columnspan=4,sticky=NSEW)
        B3.grid(row=12,column=8,rowspan=4,columnspan=4,sticky=NSEW)
        Tview.grid(row=16,column=0,rowspan=5,columnspan=10,sticky=NSEW)
        Sview.grid(row=16,column=11,rowspan=5,columnspan=1,sticky=NSEW)

        #WriteToPeridicalList('9',T)
        reFreshPeridicalList(T)
        #downLoadAlbum(self.websit,self.localPath,'764')
        #downloadFile('http://luoomp3.kssws.ks-cdn.com/low/luoo/radio5/01.mp3', r'c:\music\mi.mp3')
        L_Bottem = Label(root,text="该工具仅供测试，请勿商用。").grid(row=21,column=0,rowspan=1,columnspan=13,sticky=NSEW)
        ############################4.running##############################

def main():
    root = Tk()
    LuooSpider(root)
    root.mainloop()

if __name__ == '__main__':
    main()