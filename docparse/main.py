from utils import load_json,\
    openai_wrapper,\
    single_page_sort,\
    post_process_replace
from PromptAndCLass import DocAnalysePrompt,\
    DocAnalyseResponseFormat,\
    DocWritePrompt,\
    DocWriteResponseFormat

import os

if __name__ == "__main__":
    doc_llm = load_json('./data/doc_llm.json')
    save_folder_path= "./output/"
    for idx,single_page_llm in enumerate(doc_llm):
        if idx == 0 or idx == 2:
            continue

        # short info for column type
        DocAnalysePage = [{'center_position': item['center_position'], 'box_position': item['box_position'], 'category': item['category']} for item in single_page_llm]
        DocAnalyse_result =  openai_wrapper(DocAnalysePrompt,DocAnalysePage,DocAnalyseResponseFormat)

        # sort the element with column type || use name to replace latex
        name2latex,latex_name_list,page = single_page_sort(DocAnalyse_result, single_page_llm)
        print(name2latex)

        # add latex_name_list to prompt
        DocWritePrompt = DocWritePrompt.replace("{latex_list}", str(latex_name_list))
        result =  openai_wrapper(DocWritePrompt,page,DocWriteResponseFormat)
        markdown_result = result.markdown

        # replace the latex with original tex or an image
        pattern = r"####(latex_\d+)####"
        final_result = post_process_replace(pattern,name2latex,markdown_result,latex2image = True,save_folder_path = save_folder_path)

        with open(os.path.join(save_folder_path, f'page_{idx}.md'), 'w') as file:
            file.write(final_result)
