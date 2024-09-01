# DocParse
我们将gptpdf和PDF-Extract-kit融合到一起，得到相对不错的效果。对应的结果在/output/文件夹
# 步骤
1. 我们首先对当前很多pdf解析在线服务做测试，观察方法的优缺点，记录在 data/third_party_test_result/result_analyse.md
2. 确定了使用PDF-Extract-Kit作为信息提取框架，加上GPT对信息做矫正的思路
3. 完成相对简单的第一页和第三页
4. 对第二页出现的“长文本” 以及 “长表”设计信息验证增强（就是把OCR数据也放上去） + 使用关键词代替对应的长文本，从而降低了输入GPT的数据长度

# 复现
1. 安装PDF-Extract-Kit，这里有几个版本冲突的地方：
    - pillow的版本冲突，需要卸载后安装8.4.0的，安装之前需要安装对应的依赖：
        ```shell
        sudo apt-get install libjpeg-dev zlib1g-dev
        pip install pillow==8.4.0
        ```
    - paddle版本问题
        ```shell
        pip install paddle==3.0.0b1
        ```
    - tex转图片的pillow版本问题，因为版本比较低，所以只能用默认输入法
        ```python
        fontText = ImageFont.load_default()
        ```
2. 将`pdf-steps.ipynb`拷贝到`PDF-Extract-Kit/`中，只需要运行到 ```def process_ocr_result(ocr_reuslt):```，后面的是OPENAI测试程序
3. 得到对应的doc_llm.json，并保存到`data/`
4. ```shell
    python docparse/main/py --doc_llm_path ./data/doc_llm.json --save_folder_path ./output/
    ````

# 改进
1. 表格的提取里面很多数据都漏了，而且很多数据错误，最后必须要用OCR数据来补充。
2. 开源的TexLive做的表格识别效果非常强，可以参考一下应该如何实现的[link](https://github.com/QianJianTech/LaTeXLive)
3. 这里我们没有做公式检测，这里也是可以添加进去的
4. 目前都是for循环，可以批量优化一下，加快速度