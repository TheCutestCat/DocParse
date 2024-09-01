from utils import load_json,\
    openai_wrapper,\
    single_page_sort,\
    post_process_replace
from PromptAndCLass import DocAnalysePrompt,\
    DocAnalyseResponseFormat,\
    DocWritePrompt,\
    DocWriteResponseFormat,\
    TexFixPrompt,\
    TexFixResponseFormat,\
    LongTextCombinePrompt,\
    LongTextCombineResponseFormat

import os

if __name__ == "__main__":
    
    import argparse

    parser = argparse.ArgumentParser(description="Process document LLM")
    parser.add_argument('--doc_llm_path', type=str, default='./data/doc_llm.json', help='Path to the document LLM JSON file')
    parser.add_argument('--save_folder_path', type=str, default='./output/', help='Path to save the output')

    args = parser.parse_args()

    doc_llm = load_json(args.doc_llm_path)
    save_folder_path = args.save_folder_path
    for idx,single_page_llm in enumerate(doc_llm):
        # if idx == 0 or idx == 2:
        #     continue
        
        name2longtext = {}
        longtext_list = []
        # long context solution
        for idx,res in enumerate(single_page_llm):
            if "ocr_result" in res and "latex_result" not in res:
                # 这意味着这是一个纯文本信息
                if len(res['ocr_result']) > 3:
                    # combine these long context
                    ocr_result = res['ocr_result']
                    ocr_result = sorted(ocr_result, key=lambda x: (x[1], x[0])) # sort to makr it better for LLM
                    avg_x0, avg_x1 = sum(x[0] for x in ocr_result) / len(ocr_result), sum(x[1] for x in ocr_result) / len(ocr_result)

                    longtextcombine_result = openai_wrapper(LongTextCombinePrompt,ocr_result,LongTextCombineResponseFormat)
                    longtextcombine_result = longtextcombine_result.text
                    
                    # use the name to replace them
                    longtext_name = f"longtext_{idx}"
                    name2longtext[longtext_name] = longtextcombine_result
                    longtext_list.append(longtext_name)
                    
                    res['ocr_result'] = [[avg_x0,avg_x1,longtext_name]]
                    
        
        # latex table correction with OCR result
        for res in single_page_llm:
            if "latex_result" in res and "ocr_result" in res:
                latex_result = res['latex_result']
                ocr_result = res['ocr_result']
                ocr_result = sorted(ocr_result, key=lambda x: (x[1], x[0])) # sort to makr it better for LLM
                texfix_result = openai_wrapper(TexFixPrompt,f"tex : {latex_result}, OCR : {ocr_result}",TexFixResponseFormat)
                texfix_result = texfix_result.tex
                res["latex_result"] = texfix_result
                
        # long latex result correction

        # short info for column type
        DocAnalysePage = [{'center_position': item['center_position'], 'box_position': item['box_position'], 'category': item['category']} for item in single_page_llm]
        DocAnalyse_result =  openai_wrapper(DocAnalysePrompt,DocAnalysePage,DocAnalyseResponseFormat)

        # sort the element with column type || use name to replace latex
        name2latex,latex_name_list,page = single_page_sort(DocAnalyse_result, single_page_llm)
        print(f"{latex_name_list} : latex_name_list")

        # add latex_name_list to prompt
        DocWritePrompt = DocWritePrompt.replace("{latex_list}", str(latex_name_list))
        DocWritePrompt = DocWritePrompt.replace("{longtext_list}", str(longtext_list))
        result =  openai_wrapper(DocWritePrompt,page,DocWriteResponseFormat)
        markdown_result = result.markdown

        # replace the longtext
        pattern_longcontext = r"####(longtext_\d+)####"
        markdown_result = post_process_replace(pattern_longcontext,name2longtext,markdown_result)
        
        # replace the latex with original tex or an image
        pattern_table_image = r"####(latex_\d+)####"
        final_result = post_process_replace(pattern_table_image,name2latex,markdown_result,latex2image = True,save_folder_path = save_folder_path)

        with open(os.path.join(save_folder_path, f'page_{idx}.md'), 'w') as file:
            file.write(final_result)
