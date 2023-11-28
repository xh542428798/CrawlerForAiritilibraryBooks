
#%%
import time
import base64
import os
# pip install selenium
# pip install msedge-selenium-tools
from msedge.selenium_tools import Edge, EdgeOptions
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# urlList = [
#     r'https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200321779&DetailSourceType=0'
# ]
urlDict = {
    "中枢神经系统CT和MRI影像解读（第2版）":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200612270&DetailSourceType=0",
"肿瘤影像诊断图谱第2版":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200813237&DetailSourceType=0",
'颅脑影像诊断学': r'https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20210830427&DetailSourceType=0',
"中华医学影像案例解析宝典_骨肌分册": r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605092&DetailSourceType=0",
"中华医学影像案例解析宝典_神经分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605130&DetailSourceType=0",
"中华医学影像案例解析宝典_乳腺分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20210922289&DetailSourceType=0",
"中华医学影像案例解析宝典．头颈分册": r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605298&DetailSourceType=0",
"中华医学影像案例解析宝典_心胸分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605096&DetailSourceType=0",
"中华医学影像案例解析宝典_腹部分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605143&DetailSourceType=0",
"中华医学影像案例解析宝典_儿科分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605116&DetailSourceType=0",
"中华医学影像案例解析宝典_介入分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200321773&DetailSourceType=0",
"胎儿磁共振影像诊断学": r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605444&DetailSourceType=0",
"医学影像学读片诊断图谱_骨肌分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605176&DetailSourceType=0",
"医学影像学读片诊断图谱_胸部分册":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200528332&DetailSourceType=0",
"中华医学影像技术学_MR成像技术卷":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200605154&DetailSourceType=0",
"头颈部放射治疗解剖图谱":r"https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200521260&DetailSourceType=0"
}

len(urlDict)
#%%
thisID = 0
book_title = list(urlDict.keys())[thisID]
url = urlDict.get(book_title)
options = EdgeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = Edge(options=options, executable_path=r"..\msedgedriver.exe") # 相应的浏览器的驱动位置
# 打开登录页面
browser.get(url)
print(book_title,":",url)
#%%
#在点击m某个的时候会打开新窗口，需要切换窗口
handles = browser.window_handles #查询窗口总数，返回一个包含所有窗口句柄handles的列表
print('老窗口句柄为：{0}'.format(handles))
wait = WebDriverWait(browser, 4)
button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnReadOnline"]')))
button.click()

#确定pdf模式
button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnPDF_Online"]')))
button.click()

#%%
handles = browser.window_handles #再次获取窗口句柄handles
print('新窗口句柄为：{0}'.format(handles))
#新老句柄列表可以看出，新出现的句柄在列表里面排在后面
browser.switch_to.window(handles[-1])#执行切换窗口操作

#%% 设置单页
element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler"]')))
element.click()
element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btn_set"]')))
element.click()
element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btn_sp"]')))
element.click()
# 查询 title, 通过 id 属性获取指定的 span 元素
span_element = browser.find_element_by_id("booktitle")
element.click()
book_title = span_element.get_attribute("textContent")
# 查询totalPage
element = browser.find_element_by_xpath('//*[@id="intPageTotal"]')
totalPage = int(element.get_attribute('textContent').replace(" / ",""))
book_title = book_title.replace(".","").replace("：","").replace(" ","")
print(book_title)
folder = "./"+ book_title
if not os.path.exists(folder):
    print(folder)
    os.mkdir(folder)

time.sleep(2)
# 定位到页面中间的元素
element = browser.find_element_by_xpath('//*[@id="L1_0_0"]')
element.click()
# 等待3秒钟
time.sleep(2)

#%%
print(book_title,":",url)
# for step in range(0,totalPage+1):
for step in range(0,totalPage+1):
    print("step开始",step)
    pageNum = step
    filePath = '{}/{}.jpeg'.format(folder,pageNum)
    if os.path.exists(filePath):
        print("文件存在")
        continue
    # 获取page按钮
    # time.sleep(1)
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler2"]')))
    element.click()
    try:
        element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pageNum"]')))
        element.clear()  # 先清空文本框内容
        element.send_keys(step)  # 输入数字
        element.send_keys(Keys.RETURN)  # 模拟回车键
        # pageNum = element.get_attribute('value')
    except:
        # 如果失效，就点击一下中间的图片激活
        element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'L1_0_0')))
        element.click()
        time.sleep(2)
        element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler2"]')))
        element.click()
        element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pageNum"]')))
        element.clear()  # 先清空文本框内容
        element.send_keys(step)  # 输入数字
        element.send_keys(Keys.RETURN)  # 模拟回车键
        pageNum = element.get_attribute('value')
    time.sleep(1)
    # 获取包含 base64 图片的元素
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'L1_0_0')))
    image_src = element.get_attribute('src')
    # time.sleep(2)
    # 显示获取到的图片 src
    print("图片页码：",pageNum) #,"。Src:", image_src)
    # print(pageNum,"。Src:", image_src)
    # 保存image，将image_src base64转成jpeg
    sss= image_src.replace("data:image/jpeg;base64,","")
    # print(len(sss)) # print(imagedata)
    imagedata = base64.b64decode(sss)
    # 保存
    file = open('{}/{}.jpeg'.format(folder,pageNum),"wb")
    file.write(imagedata)
    file.close()

    # df.loc[len(df)]=[step,pageNum,image_src]
    print("step结束了",step)
  
    if step == totalPage:
        print("Finished")

# %%
browser.close()
# 关闭浏览器
browser.quit()
for thisID in range(0,len(urlDict)):
    print(thisID,":",list(urlDict.keys())[thisID])
# %% 批量
# for thisID in range(0,len(urlDict)):
for thisID in [0,1]:
    # thisID = 6
    book_title = list(urlDict.keys())[thisID]
    url = urlDict.get(book_title)
    options = EdgeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = Edge(options=options, executable_path=r"..\msedgedriver.exe") # 相应的浏览器的驱动位置
    # 打开登录页面
    browser.get(url)
    print("ID:",thisID,"。",book_title,":",url)

    #在点击m某个的时候会打开新窗口，需要切换窗口
    handles = browser.window_handles #查询窗口总数，返回一个包含所有窗口句柄handles的列表
    print('老窗口句柄为：{0}'.format(handles))
    wait = WebDriverWait(browser, 4)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnReadOnline"]')))
    button.click()
    time.sleep(2)
    try:
        #确定pdf模式
        button = browser.find_element_by_xpath('//*[@id="btnPDF_Online"]')
        button.click()
        time.sleep(2)
    except:
        None
    time.sleep(2)
    handles = browser.window_handles #再次获取窗口句柄handles
    print('新窗口句柄为：{0}'.format(handles))
    #新老句柄列表可以看出，新出现的句柄在列表里面排在后面
    browser.switch_to.window(handles[-1])#执行切换窗口操作
    time.sleep(2)

    # 设置单页
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler"]')))
    element.click()
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btn_set"]')))
    element.click()
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btn_sp"]')))
    element.click()
    # 查询 title, 通过 id 属性获取指定的 span 元素
    span_element = browser.find_element_by_id("booktitle")
    element.click()
    book_title = span_element.get_attribute("textContent")
    # 查询totalPage
    element = browser.find_element_by_xpath('//*[@id="intPageTotal"]')
    totalPage = int(element.get_attribute('textContent').replace(" / ",""))
    book_title = book_title.replace(".","").replace("：","").replace(" ","")
    print(book_title)
    folder = "./"+ book_title
    if not os.path.exists(folder):
        print(folder)
        os.mkdir(folder)

    time.sleep(2)
    try:
        # 定位到页面中间的元素
        center_x = browser.execute_script("return window.innerWidth") / 2
        center_y = browser.execute_script("return window.innerHeight") / 2
        actions = ActionChains(browser)
        actions.move_by_offset(center_x, center_y).click().perform()
        # element = browser.find_element_by_xpath('//*[@id="L1_0_0"]')
        # browser.execute_script("arguments[0].scrollIntoView();", element)
        # element.click()
        # 等待3秒钟
        time.sleep(2)
    except:
        None

    print(book_title,":",url)
    for step in range(0,totalPage+1):
        # print("step开始",step)
        pageNum = step
        filePath = '{}/{}.jpeg'.format(folder,pageNum)
        if os.path.exists(filePath):
            # print("文件存在")
            continue
        # 获取page按钮
        # time.sleep(1)
        element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler2"]')))
        element.click()
        try:
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pageNum"]')))
            element.clear()  # 先清空文本框内容
            element.send_keys(step)  # 输入数字
            element.send_keys(Keys.RETURN)  # 模拟回车键
            # pageNum = element.get_attribute('value')
        except:
            # 如果失效，就点击一下中间的图片激活
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'L1_0_0')))
            element.click()
            time.sleep(2)
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler2"]')))
            element.click()
            element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pageNum"]')))
            element.clear()  # 先清空文本框内容
            element.send_keys(step)  # 输入数字
            element.send_keys(Keys.RETURN)  # 模拟回车键
            pageNum = element.get_attribute('value')
        time.sleep(3)
        # 获取包含 base64 图片的元素
        element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'L1_0_0')))
        image_src = element.get_attribute('src')
        # time.sleep(2)
        # 显示获取到的图片 src
        print("图片页码：",pageNum) #,"。Src:", image_src)
        # print(pageNum,"。Src:", image_src)
        # 保存image，将image_src base64转成jpeg
        sss= image_src.replace("data:image/jpeg;base64,","")
        # print(len(sss)) # print(imagedata)
        imagedata = base64.b64decode(sss)
        # 保存
        file = open('{}/{}.jpeg'.format(folder,pageNum),"wb")
        file.write(imagedata)
        file.close()

        # df.loc[len(df)]=[step,pageNum,image_src]
        print("step结束了",step)
    
        if step == totalPage:
            print("Finished")

    # 关闭浏览器
    browser.quit()
# %%
import os

ls_change = []
folders  = r'F:\F_study档案\爱好代码\华艺爬虫\new'
ls = [ name for name in os.listdir(folders) if os.path.isdir(os.path.join(folders, name)) ]
for fname in ls:
    folder_path = "./"+ fname
    files = os.listdir(folder_path)
    files.sort(key=lambda x: int(x.split('.')[0]))
    i = 0
    while i < len(files)-1:
        size1 = os.path.getsize(os.path.join(folder_path, files[i]))
        size2 = os.path.getsize(os.path.join(folder_path, files[i+1]))
        if size1==size2:
            if int(files[i].split('.')[0]) > int(files[i+1].split('.')[0]):
                os.remove(os.path.join(folder_path, files[i]))
                print(os.path.join(folder_path, files[i]))
                files.remove(files[i])  # 手动更新文件列表
                
            else:
                os.remove(os.path.join(folder_path, files[i+1]))
                print(os.path.join(folder_path, files[i+1]))
                files.remove(files[i+1])  # 手动更新文件列表
        else:
            i += 1
# %% 全图片两两比较
import os
from tqdm import tqdm
ls_change = []
folders  = r'F:\F_study档案\爱好代码\华艺爬虫\new'
ls = [ name for name in os.listdir(folders) if os.path.isdir(os.path.join(folders, name)) ]
len(ls)
for fname in tqdm(ls[10:11]):
    print(fname)
    folder_path = "./"+ fname
    files = os.listdir(folder_path)
    files.sort(key=lambda x: int(x.split('.')[0]))
    for i in range(len(files)):
        for j in range(i+1, len(files)):
            size1 = os.path.getsize(os.path.join(folder_path, files[i]))
            size2 = os.path.getsize(os.path.join(folder_path, files[i+1]))
            if size1==size2:
                if int(files[i].split('.')[0]) > int(files[j].split('.')[0]):
                    os.remove(os.path.join(folder_path, files[i]))
                    print(os.path.join(folder_path, files[i]))
                    files.remove(files[i])  # 手动更新文件列表)
                else:
                    os.remove(os.path.join(folder_path, files[j]))
                    print(os.path.join(folder_path, files[j]))
                    files.remove(files[j])  # 手动更新文件列表
# %%
