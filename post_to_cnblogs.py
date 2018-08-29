# coding=utf-8

'''
博客园markdown一键POST文章脚本,需要手动更改的部分:
    1.登录博客园之后cookie中的.CNBlogsCookie字段的值
    2.markdown源文件的目录
'''

import sys
import re
import requests
import yaml
from bs4 import BeautifulSoup

config = {
    'md_dir': './blog/source/', # markdown源文件的目录
}

cnblogs_cookie = {
    '.CNBlogsCookie': '此处为修改处',
}

postdata = {
    'Editor$Edit$Advanced$chkComments': 'on',
    'Editor$Edit$Advanced$chkDisplayHomePage': 'on',
    'Editor$Edit$Advanced$chkMainSyndication': 'on',
    'Editor$Edit$Advanced$ckbPublished': 'on',
    'Editor$Edit$Advanced$tbEnryPassword': '',
    'Editor$Edit$Advanced$txbEntryName': '',
    'Editor$Edit$Advanced$txbExcerpt': '',
    'Editor$Edit$Advanced$txbTag': '推荐向',
    'Editor$Edit$EditorBody': 'test_content_test',
    'Editor$Edit$lkbPost': '发布',
    'Editor$Edit$txbTitle': 'test_title_test',
}



def main(mdfilename):
    global config
    global cnblogs_cookie
    global postdata

    mdhead = '' # md头配置
    mdcontent = '' # md文章内容
    with open('%s%s'%(config['md_dir'], mdfilename)) as f:
        mdsource = f.read().split('\n---\n')
        mdhead = mdsource[0].strip('---').strip()
        mdcontent = '\n---\n'.join(mdsource[1:])
    article_config = yaml.load(mdhead)
    postdata['Editor$Edit$txbTitle'] = article_config['title']
    postdata['Editor$Edit$Advanced$txbTag'] = ', '.join(article_config['tags'])
    postdata['Editor$Edit$EditorBody'] = mdcontent

    resp_get = requests.get('https://i.cnblogs.com/EditPosts.aspx?opt=1', cookies=cnblogs_cookie)
    soup = BeautifulSoup(resp_get.text, 'html5lib')
    postdata['__VIEWSTATE'] = soup.select('#__VIEWSTATE')[0].get('value')
    postdata['__VIEWSTATEGENERATOR'] = soup.select('#__VIEWSTATEGENERATOR')[0].get('value')

    resp_post = requests.post('https://i.cnblogs.com/EditPosts.aspx?opt=1', data=postdata, cookies=cnblogs_cookie)
    if '发布成功' in resp_post.text:
        print('[*]POST Article To Cnblogs Successful')
    else:
        print('[*]POST Article To Cnblogs Failed')

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print('Usage:\n\tpython post_to_cnblogs.py "xxx.md"')
    else:
        main(sys.argv[1])
