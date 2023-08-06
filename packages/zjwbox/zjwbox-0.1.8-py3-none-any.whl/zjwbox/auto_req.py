import requests
import parsel, re
from lxml import etree
import time, random
from pyppeteer import launch, launcher
import asyncio
import nest_asyncio
import warnings, re
from tqdm import tqdm, trange
from faker import Faker



warnings.filterwarnings("ignore")
nest_asyncio.apply()


source_pages = []
window_pages = []
launcher.DEFAULT_ARGS.remove("--enable-automation")

async def source_page(url: str) -> None:
    browser = await launch({"headless":False,"dumpio":True,"autoClose":False,"args":["--no-sandbox","--window-size=1366.850"]})
    page = await browser.newPage()
    await page.goto(url)
    text = await page.content()
    source_pages.append(text)
    await browser.close()


async def window_page(url: str) -> None:
    temp_str = ""
    rand_UA = []
    fake = Faker()
    for _ in range(10):
        rand_UA.append( fake.user_agent() )
    pypp_UA = random.choice(rand_UA)
    browser = await launch(
        {
             "headless":False,
             "dumpio":True,
             "autoClose":False,
             "userDataDir":r"D:\\temporary",
              "args":[
                  "--no-sandbox",
                  "--window-size=1366.850",
                  f"--user-agent={pypp_UA}"
              ]
        }
    )
    page = await browser.newPage()
    await page.goto(url)

    try:
        cont_click = await page.querySelector(" div.fold-page-text > span")
        await cont_click.click()
    except:
        pass

    try:
        p_labels = await page.querySelectorAll(selector=" div > div > p")
        for p in p_labels:
            p_text = await (await p.getProperty("textContent")).jsonValue()
            if p_text == " ":
                pass
            else:
                temp_str += p_text.strip()
        window_pages.append(temp_str)
        await browser.close()
    except Exception as e:
        print(f"浏览器发生错误！\n{e}")


def get_window_page(urls):
    for url in urls:
        asyncio.get_event_loop().run_until_complete(window_page(url))
    return window_pages


def get_source_page(urls: list) -> list:
    for url in urls:
        asyncio.get_event_loop().run_until_complete(source_page(url))
    return source_pages


def extra(text, type_extra="font", super_mode=False) -> all:
    if type_extra == "own":
        selector = parsel.Selector(text)
        xpath = etree.HTML(text)
        return selector, xpath

    if super_mode:
        pass

    if type_extra == "font":
        font_text = []
        string = text
        pattern = r"<p>(.*?)</p>"
        font_texts = re.findall(string=string, pattern=pattern)
        for f in font_texts:
            if "&nbsp" or "<br>" or "<br/>" or "<" in f:
                deal_f = re.sub(string=f, pattern=r"[&nbsp, (<\[a-z\]>.*?<\[a-z\]>)]", repl="")
                font_text.append(deal_f.strip())
            else:
                font_text.append(f)

        return font_text




if __name__ == "__main__":
    # urls = ["https://blog.csdn.net/weixin_41846313/article/details/84718739"]
    urls = ["https://wenku.baidu.com/view/7bb441e6a88271fe910ef12d2af90242a995ab1c.html?fr=aladdin664466&ind=1"]
    # selector, xpath = extra(text=text[0], type_extra="own")
    # print(selector, xpath)
    text = get_window_page(urls)
    print(text)