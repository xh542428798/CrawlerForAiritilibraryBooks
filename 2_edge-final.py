
#%%
import time
import base64

# pip install selenium
# pip install msedge-selenium-tools
from msedge.selenium_tools import Edge, EdgeOptions
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#%%
options = EdgeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = Edge(options=options, executable_path=r".\msedgedriver.exe") # 相应的浏览器的驱动位置
# 打开登录页面
browser.get("https://ebooks.airitilibrary.cn/Detail/Detail?PublicationID=P20200813237&DetailSourceType=0")

#%%
#在点击m某个的时候会打开新窗口，需要切换窗口
handles = browser.window_handles #查询窗口总数，返回一个包含所有窗口句柄handles的列表
print('老窗口句柄为：{0}'.format(handles))

#%% 
wait = WebDriverWait(browser, 4)
button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnReadOnline"]')))
button.click()

handles = browser.window_handles #查询窗口总数，返回一个包含所有窗口句柄handles的列表
print('新窗口句柄为：{0}'.format(handles))

handles = browser.window_handles #再次获取窗口句柄handles
print('新窗口句柄为：{0}'.format(handles))
#新老句柄列表可以看出，新出现的句柄在列表里面排在后面
browser.switch_to.window(handles[-1])#执行切换窗口操作


#%% 获取当前页面的源码
page_source = browser.page_source

# 保存页面源码到文件
with open('page_source.html', 'w', encoding='utf-8') as f:
    f.write(page_source)
#%%
# df = pd.DataFrame(columns=["step","Pagenum","Img"])
for step in range(0,1027):
    print("step开始",step)
    # 获取包含 base64 图片的元素
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'L1_0_0')))
    image_src = element.get_attribute('src')
    # 获取page按钮
    time.sleep(2)
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler2"]')))
    element.click()
    time.sleep(2)
    element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pageNum"]')))
    pageNum = element.get_attribute('value')
    # 显示获取到的图片 src
    print(pageNum) #,"。Src:", image_src)
    # print(pageNum,"。Src:", image_src)
    # 保存image，将image_src base64转成jpeg
    sss= image_src.replace("data:image/jpeg;base64,","")
    # print(len(sss)) # print(imagedata)
    imagedata = base64.b64decode(sss)
    # 保存
    file = open('./jpeg/{}.jpeg'.format(pageNum),"wb")
    file.write(imagedata)
    file.close()

    # df.loc[len(df)]=[step,pageNum,image_src]
    print("step结束了",step)
  
    # 下一页
    buttonNext=WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="next_page"]')))
    # buttonNext = browser.find_element_by_xpath('//*[@id="next_page"]')
    buttonNext.click()
    # df.to_csv('./tmp.csv',index=False,encoding='gbk')

    # 休息2s
    time.sleep(2)

#%%
df.to_csv('./page31-42.csv',index=False,encoding='gbk')
#%%
element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggler2"]')))
element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pageNum"]')))
text = element.text
print(text)

element.get_attribute('innerHTML')
element.get_attribute('value')
#%%
thiselement=browser.find_element_by_xpath('//*[@id="L1_0_0"]')
# 获取元素中的图片 src
image_src = thiselement.get_attribute('src')

# 显示获取到的图片 src
print("Image Src:", image_src)
# browser.get("https://ebooks.airitilibrary.cn/pdfViewer/index.aspx?Token=04B6EAC8-53B3-4195-981D-FDE1E2DB4907&GoToPage=-1")
#%%  ！！！！！！！！！！！！！！！！注意修改账号密码🍖🍖🍖🍖
# # 等待元素出现，定位用户名和密码输入框，并输入相应的值
# 显式等待直到元素可见



print("All Finished!") 

# element = browser.find_element_by_xpath('//*[@id="form1"]/div[3]/div[2]')
# element.text
# # 获取元素的某个属性的值
# print(element.get_attribute("attribute_name"))

# %%
