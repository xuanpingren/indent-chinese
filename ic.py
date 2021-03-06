# 功能：将中文文本对齐排版
# 参数：
#   n=20  每行20个字
#   s=2   段与段空两行
#   o=output.txt 输出文件名
# 用法：
#   python ic.py input.txt  (默认每行20字，段与段空2行)
#   python ic.py o=output.txt input.txt
#   python ic.py n=40 s=1 input.txt (每行40字，段与段空1行)
#   python ic.py s=3 input.txt
# 2015-04-28, 2016-09-28

import sys, os, codecs, time

########### 设置参数 ##########
t = time.localtime()
default_output_filename = 'output-' + \
    '-'.join([str(t.tm_year), str(t.tm_mon), str(t.tm_mday), str(t.tm_hour), str(t.tm_min), str(t.tm_sec)]) + \
    '.txt'
para = {'n':20, 's':2, 'o':default_output_filename}
for a in sys.argv[1:]:
    a = a.strip()
    if a.find('n=') == 0:
        para['n'] = int(a[2:])
    elif a.find('s=') == 0:
        para['s'] = int(a[2:])
    elif a.find('o=') == 0:
        para['o'] = a[2:]
    else:
        para['i'] = a

if not 'i' in para:
    print('输入要转的文件名')
    sys.exit()
if para['n'] < 1:
    print('n必须大于等于1')
    sys.exit()
    
def is_dos(lines):
    ''' 判定是不是dos系统的换行符 '''
    
    for x in lines:
        if x.find('\r\n') >= 0:
            return True
        
    return False


def combine_lines(lines):
    ''' 将只有一个换行符所有行相连接 '''
    
    result = []
    lst = []
    for line in lines:
        if line.strip() == '':
            if len(lst) > 0:
                result.append(''.join(lst))
                lst = []
        else:
            lst.append(line.strip() + chr(12288))
    result.append(''.join(lst))
    return result


def indent_it(all_lines, para):
    ''' 对齐所有行 '''
    
    result = []
    newline = '\n'
    if is_dos(all_lines):
        newline = '\r\n'
    
    # 微软Notepad把文件第一个字符存为0xfeff，如果有，去掉它
    if ord(all_lines[0][0]) == 0xfeff:  
        all_lines[0] = all_lines[0][1:]
        
    combined_lines = combine_lines(all_lines)
    total_num = len(combined_lines)
    line_num = 0
    for line in combined_lines:
        line_num += 1
        
        temp = ''
        # 半角变全角
        for c in line:
            if c == ' ':  # 空格特别处理 http://www.cnblogs.com/kaituorensheng/p/3554571.html
                temp += chr(12288)
            elif 0x21 <= ord(c) <= 0x7e:
                temp += chr(ord(c) + 65248)
            else:
                temp += c
        line = temp
        
        if len(line) <= para['n']:
            result.append(line + (para['s'] + 1)*newline)
        else:
            n = para['n']
            while line != '':
                result.append(line[0:n] + newline)
                line = line[min(n,len(line)):]
            if line_num < total_num:
                result.append(para['s']*newline)
        
    return result

if not os.path.exists(para['i']):
    print(para['i'] + '不存在')
    sys.exit()
    
f1 = codecs.open(para['i'], 'r', 'utf-8')
f2 = codecs.open(para['o'], 'w', 'utf-8')
all_lines = f1.readlines()
for line in indent_it(all_lines, para):
    f2.write(line)
f1.close()
f2.close()
print('转好的文件放在' + para['o'])
