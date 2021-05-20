
import json
import requests
import time
import argparse
def get_user_info(path, temp):
    f = open(path, 'r')

    f = f.read()
    f = f.split('\n')
    f = [item for item in f if item != '']
    # return f
    for i in range(len(f)):
        temp_f = f[i].strip('\x00')
        temp_f = json.loads(temp_f)
        temp.append(temp_f)
    return temp

def download_image(i):
    temp = []
    n=0

    path = '/home/shuo/Documents/AI_learning/umdy/collected_user/collect_user_{}.txt'.format(i)
    temp = get_user_info(path, temp)
    ooo = dict()
    for item in temp:
        ooo[item[2]] = item[1]
    for item in ooo:
        try:
            image_url = '/home/shuo/Documents/AI_learning/umdy/user_image/{}.png'.format(item)
            with open(image_url, 'wb') as handle:
                response = requests.get(ooo[item], stream=True)
                n+=1
                if not response.ok:
                    print(image_url, response)
                if n%100==0:
                    print(n)
                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
        except:
            continue



if  __name__ =='__main__':
    start = time.time()
    main_arg_parser = argparse.ArgumentParser(description="non_function_generator")
    main_arg_parser.add_argument('-n', type=str, default='1', help='data_path')

    args = main_arg_parser.parse_args()
    download_image(args.n)