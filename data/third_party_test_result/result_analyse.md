# Page 1
- gptpdf : good
- jina ai : bad 缺少markdown格式里面的 - 所对应的内容
- pypdf : bad 1. 文本没有断句，缺失格式：1. 章节 + 点
- pdf_extract_kit : good


# page 2 
- gptpdf : bad, 但是表格出现了严重错误(已经标出)，第一个数据数据有少量错误，第二个识别失败，大量数据都是编造的。无法识别*p **p
- jina ai : bad 没能识别成功
- pypdf : bad 没能识别成功
- pdf_extract_kit : bad 表格被当作了图片从而没有去进行表格化的model操作。 但是文本检测到了 *p


# page 3
- gptpdf : bad 图片不能识别到这里面的位置信息，只有最简单的表格有解
- jina ai : bad 无法识别图片
- pypdf : bad 无法识别
- pdf_extract_kit : 将表格当成了图片，没有进行识别图片的操作

# 总结
1. GPT在识别的时候容易出现幻觉，尤其是在表格数据上，要谨慎使用。 用来做汇总不错
2. pdf_extract_kit中的layout功能应该优先使用
3. doc转成pdf，就变成了pdf版本的识别任务。。


prompt : """
这些是经过OCR的数据，你可以完全信任
这些是图片解析所得到的数据，你应该XXX
"""