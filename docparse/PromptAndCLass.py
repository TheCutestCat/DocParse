DocAnalysePrompt = """你是一个文本分析大师，你需要将一个杂乱的文本内容转化为有条理的markdown结构
我们规定文本的左上角为0,0 其中x表示从左往右依次增大，y表示从上到下依次增大

我们会输入一个list，其中的item都是的下面的结构：
{'center_position': (x_avg,y_avg),
'box_position': (xmin,ymin,xmax,ymax),
'category': 'category',包含文本，标题等
'ocr_result': [(x_avg, y_avg, ocr_result)]
'latex_result' : 'latex'}
ocr_result是一个list，里面是一个三元组(x_avg, y_avg, ocr_result)，里面ocr_result就是识别到的文本内容。
这里面的ocr_result会有重叠的部分，你要根据对应的x_avg y_avg判断这些内容是不是重复的，并且忽略掉重复的部分

你需要分析这个文本的结构，例如：是单栏，双栏或者是其他结构
"""

from pydantic import BaseModel
from enum import Enum

class ColumnType(str, Enum):
    single_column = "single_column"
    double_column = "double_column"
    others = "others"
    
class DocAnalyseResponseFormat(BaseModel):
    very_short_analysis : str
    ColumnType : ColumnType


DocWritePrompt = """你是一个文本格式化机，你需要将一个杂乱的文本内容转化为有条理的markdown结构，你不会遗漏原文中的任何信息
我们规定文本的左上角为0,0,我们使用(x,y)来表示位置 其中x表示从左往右依次增大，y表示从上到下依次增大

我们会输入一个list，其中的item都是的下面的结构：
{'category': 'category',包含文本，标题等
'ocr_result': [(x_avg, y_avg, ocr_result)]
'latex_result' : 'latex_i'}
ocr_result是一个list，里面是一个三元组(x_avg, y_avg, ocr_result)，里面ocr_result就是识别到的文本内容。在这里面你也是要根据对应的y_avg去判断元素所应该在的位置
这里面的ocr_result会有重叠的部分，你要根据对应的x_avg y_avg判断这些内容是不是重复的，并且忽略掉重复的部分
你要注意其中我们对于其中的图表使用了{latex_list}去进行替代，你要在对应的位置使用####latex_i####来代替对应的图表。
我们针对长文本使用了{longtext_list}去进行替代，你必须在对应的位置使用####longtext_i####
请你注意我们的category识别可能是会有问题的，你要对这里面的明显错误去进行纠正
你要将文本中提到的内容都严格地完成地返回，不要遗漏任何内容，不要省略任何内容，

错误示例：
没有将内容都返回，反而给出了省略号，同时返回了不存在的图表
# title
....
####latex_i####
# next title
没有严格按照原文本的内容返回，而是添加了其他的内容
正确示例：
# title
the text from the input 
####latex_1#### 要展示的图表
####longtext_1#### 需要去进行替换的长文本

请你务必严格遵守上面的规则，否则我会失去这份工作
"""
            
class DocWriteResponseFormat(BaseModel):
    markdown : str

TexFixPrompt = """你是一个tex高手，我们有以下的信息：一个tex公式还有一个OCR识别结果。
其中tex的公式是很有可能发生错误的，我们希望你可以使用OCR结果去对其进行矫正。
我们规定文本的左上角为0,0 其中x表示从左往右依次增大，y表示从上到下依次增大

我们输入的OCR识别结果是：
[[x,y,text]],其中text就是OCR识别到的文本
你需要更相信OCR所识别到的信息，尝试去检查tex中的数据有没有错误或者是缺少的，如果有，请尽可能补充上去。
不要编造数据，如果你失败了，我会丢掉我的工作
step 1:
根据OCR文本去分析tex中是否存在数据错误或者是缺失,以及应该如何改进
step 2:
给出新的tex公式
"""

class TexFixResponseFormat(BaseModel):
    analyse : str
    tex : str
    
LongTextCombinePrompt = """
你是一个文字大师，你可以将比较杂乱的文本整理成完美的样子。
我们会输入几段文字，格式是[x,y,text],其中x,y是这段文字在文本中的位置，text就是对应的文本文本
我们规定左上角为0,0 其中x表示从左往右依次增大，y表示从上到下依次增大
你需要1. 根据这些文本的相对位置找到他们应该有的顺序 2. 修复这些文本中的错误 3. 以正确的文本输出正确的文字
你必须严格遵循原文，不可以自行添加信息。
请你务必严格遵守上面的规则，否则我会失去这份工作
"""


class LongTextCombineResponseFormat(BaseModel):
    analyse : str
    text : str