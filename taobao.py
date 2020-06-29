from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from urllib.parse import quote
import json
from selenium.common.exceptions import TimeoutException

max_page=100
KEYWORD='ipad'
base_url='https://s.taobao.com/search?q='+quote(KEYWORD)    #quote将中文URL编码化
'''
无界面模式，但会跳转到登录界面，可以手动登录，也可以直接用selenium模拟点击登录，当然也可以打开network持续日志显示，截获登录时的url和表单格式！
options=webdriver.ChromeOptions()
options.add_argument('--headless')
browser=webdriver.Chrome(options=options)
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])    #以开发者模式打开
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) #不加载图片，加快访问速度
browser = webdriver.Chrome(chrome_options=chrome_options)

#browser=webdriver.Chrome()     #普通浏览器初始化
wait=WebDriverWait(browser,30)  #显式等待时间设置
def get_one_page(page):
    print('正在爬取%d页' % page)
    try:
        browser.get(base_url)   #
        if page>1 :
            #EC.等待条件，和WebDriverWait对象搭配使用，使得浏览器加载出对应节点后再开始解析提取信息！参数为一个元组！！！
            #By.选择方式
            input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
            submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear() #清空！！一般会有默认值！
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        return parse_products()
    except TimeoutException:
        print('ERROR!!!!')
def parse_products():
    html=browser.page_source
    doc=pq(html)    #pq对象初始化
    items=doc('#mainsrp-itemlist .items .item').items()     #必须用.items()方法，得到一个生成器！！
    for item in items:
        yield{
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
     
def save_to_file(item):
    with open(r'C:\Users\19233\Desktop\ret.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
    print('成功保存')
def main(page):
    for item in get_one_page(page):
        save_to_file(item)
if __name__=='__main__':
    for page in range(1,max_page+1):
        main(page)
    browser.close()     #最后需要关闭浏览器！！
    print('全部保存完毕！！！')