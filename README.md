# DocParse
我们是直接将doc转化pdf，随后将gptpdf和PDF-Extract-kit融合到一起，得到相对不错的效果。对应的结果在`/output/`文件夹
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
# 问题
### `Page_0.md`
- 开头和结尾都被LLM添加了一些不存在的词

### `Page_0.md`
- 对文本添加了新的内容，尤其是对开头，添加了新单词还有一个格式
- `Table 4`中的图表没有识别到 * ** ***
- `Table 5`中有数据错误：P value列：`0.037` `0.003` `0.02` `0.089` `0.047` `0.006`，全都是多添加了一个 `0`

### `Page_2.md`
- `Simple Uniform Table` 中的蓝色link 被识别成了：blueA link example
- `Table with Merged Cells`中d下面的格没有合并起来



# 改进
1. 表格的提取里面存在数据错误，LLM去做这类内容检测还是容易出现错误，最好是可以有更新的方法
2. 开源的TexLive做的表格识别效果非常强，可以参考一下应该如何实现的[link](https://github.com/QianJianTech/LaTeXLive)
3. 这里我们没有做公式检测，这里也是可以添加进去的
4. 目前都是for循环，可以批量优化一下，加快速度
5. 优化prompt，减少LLM添加的信息和文本结构