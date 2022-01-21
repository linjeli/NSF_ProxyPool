from bs4 import BeautifulSoup
import requests
import os
import time
import numpy as np

headers = {
    'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
user_id_file = './user_id.txt'
out_path = './out_data'

def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

def readUserId():
    '''
    读取 user_id 文件
    :return: user_id_lists
    '''
    user_id_lists = []
    with open(user_id_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            user_id_lists.append(line)
    # print(user_id_lists)
    return user_id_lists


def get(user_id, start, pagesize):
    url = f'https://scholar.google.com/citations?user={user_id}&hl=en&cstart={start}&pagesize={pagesize}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            items = soup.select('.gsc_a_tr')
            if items is not None:
                count = len(items)
                for item in items:
                    paper_name = item.select_one('td > a').text
                    co_author = item.select_one('.gs_gray').text
                    year = item.select_one('.gsc_a_y > span').text
                    publisher = item.select('.gs_gray')[1].text.split(",")[:-1]
                    f.write(f'{paper_name}\n{co_author}\n{publisher}\n{year}\n\n')
                    print(f'{paper_name}\n{co_author}\n{publisher}\n{year}\n')
                field = soup.find_all('a', {"class": "gsc_prf_inta gs_ibl"})
                for i in field:
                    f.write(i.text)
                    print(i.text)
                    pass
                return count
            else:
                print(f'用户ID：{user_id} 没有更多数据')
                return None
        else:
            print('访问失败，请检查user_id或链接地址')
    except Exception as e:
        print(f'用户ID：{user_id} 没有更多数据')
        return None

if __name__ == '__main__':
    mkdir(out_path)
    user_id_lists = readUserId()
    pagesize = '100'    # 每页显示条数，最大100
    for user_id in user_id_lists:
        user_file = os.path.join(out_path + '/' + user_id + '.txt')
        f = open(user_file, 'a+', encoding='utf-8')
        total = 0
        for start in range(0, 10000, int(pagesize)):
            print('正在采集用户ID：', user_id, start, pagesize)
            count = get(user_id, start, pagesize)
            if count is not None:
                total += count
            else:
                break
        f.write('\n\n用户ID：{} 的数据一共有：{}条\n'.format(user_id, total))
        print('用户ID：{} 的数据一共有：{}条'.format(user_id, total))
        f.close()
    print('程序完成！')