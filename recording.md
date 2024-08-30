# task 1
- 简单分析内容,尝试去对齐进行解析服务

# task 2
- 成熟的技术去进行测试得到结果

# task 3
- 给出一个可行的解决思路：
we have :
1. gpt : 文本识别，版式识别 + 图片处理（有幻觉）
2. LayoutLMv3 ： 版式检测
3. 公式的检测与识别： mathpix ? YOLO UniMERNet
4. 表格识别 StructEqTable
5. OCR ：PaddleOCR

## method
1. 转成pdf,doc作为辅助内容
版面检测
- 随后各种识别全来一次 ： OCR，公式检测，公式识别，表格识别
- 最后GPT汇总信息，补充缺失的信息内容
- 根据不同layout的版块，去给出来对应的位置内容