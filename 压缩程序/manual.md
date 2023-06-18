# SeqCompress使用手册

为使用7z进行压缩，请在工作区的python环境中安装py7zr包

```python
pip install py7zr
```

使用SeqCompress包的compress函数即可获得header_info , lower_case_info , non_ACGT_info , Substring_info , compressed_seq的信息，将其写入Heads_file.txt，Lowercase_file.txt，Non_ATCG_file.txt，Substring_file.txt ，main_file.txt即可，之后使用py7zr包压缩成7z文件。

若需要测试其他的数据，请将需要压缩的fasta文件的文件名改为`input.fasta`，运行`demo.py`可进行测试压缩。压缩后会生成名为`seqcompress.7z`和`normal.7z`的压缩包，分别对应于使用SeqCompress算法和直接使用7z进行压缩的时间。