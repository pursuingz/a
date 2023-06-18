import SeqCompress
import os
import shutil
import time
import py7zr

start_time1 = time.time()

# 打开原始fasta文件，并读取其中的序列和头部信息
with open('input.fasta', 'r') as f:
    
    sequence = ''
    for line in f:
        sequence += line
        #sequence += '\n'
# 压缩序列
header_info , lower_case_info , non_ACGT_info , Substring_info , compressed_seq = SeqCompress.compress(sequence)

# 将压缩结果写入新文件中
os.mkdir('./temp')
with open('./temp/Heads_file.txt', 'w') as f:
    f.write(header_info)  # 写入头部信息
with open('./temp/Lowercase_file.txt', 'w') as f:
    f.write(lower_case_info)  # 写入小写字母列表
with open('./temp/Non_ATCG_file.txt', 'w') as f:
    f.write(non_ACGT_info)  # 写入非ATCG字母信息
with open('./temp/Substring_file.txt', 'w') as f:
    f.write(Substring_info)  # 写入分离的重复子段
with open('./temp/main_file.txt', 'w') as f:
    f.write(compressed_seq)  # 写入二进制编码后的序列
with py7zr.SevenZipFile('seqcompress.7z', 'w') as archive:
    archive.writeall('./temp', 'base')

end_time1 = time.time()
shutil.rmtree('./temp')


seqcompress_time = end_time1 - start_time1

# 返回使用SeqCompress算法压缩的时间
print("使用SeqCompress算法压缩的时间为 %f 秒" % seqcompress_time)

start_time2 = time.time()

# 直接使用7z压缩原fasta文件
with py7zr.SevenZipFile('normal.7z', 'w') as archive:
    archive.write('input.fasta', 'base')

end_time2 = time.time()
compress_7z_time = end_time2 - start_time2

# 返回直接使用7z压缩fasta文件的时间
print("直接使用7z压缩fasta文件的时间为 %f 秒" % compress_7z_time)