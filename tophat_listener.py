import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time
from email_Utils import send_email_message

my_email = "xingzhi2@illinois.edu"
my_passwd = "Abel!!AP01"

endSession = False
receivers = ["abelliu2018@gmail.com", "juefeic2@illinois.edu", "lanzhou981028@gmail.com", "xinhang2@illinois.edu"]
sender = "courselytest@gmail.com"

class_duration = 7200


def timeit(func):
    """一个计时器"""

    def wrapper(*args, **kwargs):
        start = time.clock()
        response = func(*args, **kwargs)
        end = time.clock()
        print('time spend:', end - start)
        return response

    return wrapper


def service_shutdown(signum, frame):
    """signal handler for SIGINT"""
    print(f"received signal {signum}, {frame}")
    print("close up gracefully")
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"tophat listener结束于:{current_time}")
    global class_duration
    class_duration = 0


@timeit
def listen_unanswered():
    global class_duration
    while class_duration > 0:
        start_time = time.time()
        try:
            questions = driver.find_element_by_xpath(
                """//*[@id="flux-app"]/div/div[2]/div[1]/span/div[1]/div[1]/div/div[2]/div/span/span""")
            # print(questions.text)
            if questions.text != "0":
                msg = "您的教授提出来一个新tophat问题，快去回答吧"
                subject = "请按时回答tophat问题"
                send_email_message(sender, receivers, msg, subject)
                time.sleep(100)
            else:
                time.sleep(3)

        except selenium.common.exceptions.NoSuchElementException as e:
            print("class has not started?")
            time.sleep(60)

        finally:
            end_time = time.time()
            delta_time = end_time - start_time
            class_duration -= delta_time
            # print(f"time pass:{delta_time}, left time: {class_duration}")


if __name__ == '__main__':
    url = "https://app.tophat.com/e/416004/lecture/"
    # 设置chrome选项
    chrome_options = Options()
    # chrome_options.add_argument('--headless')# 运行时关闭窗口
    # 使用同一目录下的chromedriver.exe进行模拟
    driver_path = os.path.join(os.path.abspath("."), "chromedriver_2.36")
    print(driver_path)
    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
    # 请求网页
    driver.get(url)
    time.sleep(1)

    driver.find_element_by_id("username").send_keys(my_email)
    driver.find_element_by_id("password").send_keys(my_passwd)
    driver.find_element_by_xpath("""//*[@id="flux-app"]/div/div[2]/main/div/div/form/div[3]/div/button""").click()

    time.sleep(8)  # wait for loading the page
    listen_unanswered()

    driver.quit()
