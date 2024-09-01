from latex2png import tex2pil
import uuid

def double_column_sort(data):
    # 分组
    group1 = [item for item in data if item['center_position'][0] < 800]
    group2 = [item for item in data if item['center_position'][0] >= 800]

    # 按照 center_position 的第二个元素进行排序
    group1_sorted = sorted(group1, key=lambda x: x['center_position'][1])
    group2_sorted = sorted(group2, key=lambda x: x['center_position'][1])

    # 合并排序后的两组
    return group1_sorted + group2_sorted

import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")
base_url= os.getenv("OPENAI_BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url)

def openai_wrapper(system_messages,input_messages,response_format,model="gpt-4o-2024-08-06"):
    system_messages = {"role": "system", "content": f"{system_messages}"}
    input_messages = {"role": "user", "content": f"{input_messages}"}
    
    messages = [system_messages]
    messages.append(input_messages)
    
    completion = client.beta.chat.completions.parse(
        model= model,
        messages=messages,
        response_format=response_format,
    )
    completion_result = completion.choices[0].message

    if completion_result.parsed:
        result = completion_result.parsed
        return result
    else:
        print(completion_result.refusal)

def post_process_replace(pattern,replace_dict,markdown_result,latex2image = False,save_folder_path = None):
    if not latex2image:
        import re
        replaced_result = re.sub(pattern, lambda match: replace_dict.get(match.group(1), match.group(0)), markdown_result)
        return replaced_result
    else:
        replace_dict_image = {}
        for key,value in replace_dict.items():
            # value : tex 
            image = tex2pil(value)[0]
            unique_id = str(uuid.uuid4())
            image_save_path = os.path.join(save_folder_path,f"{unique_id}.jpg")
            image.save(image_save_path)

            replace_dict_image[key] = f"![example]({unique_id}.jpg)"
        
        import re
        replaced_result = re.sub(pattern, lambda match: replace_dict_image.get(match.group(1), match.group(0)), markdown_result)
            
        return replaced_result


def chat_completion(system_message,user_message,model="gpt-4o-mini"):
    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user","content": user_message}
    ])

    return completion.choices[0].message.content

import copy
from PromptAndCLass import ColumnType

def single_page_sort(DocAnalyse_result,single_page_llm):
    # 单栏
    if DocAnalyse_result.ColumnType is ColumnType.single_column:
        page = copy.deepcopy(single_page_llm)
        page = sorted(page, key=lambda x: x['center_position'][1])

        name2latex = {}
        latex_name_list = []
        for index,item in enumerate(page):
            if 'box_position' in item : del item['box_position']
            if 'center_position' in item : del item['center_position']
            if 'latex_result' in item:
                name2latex[f"latex_{index}"] = item['latex_result']
                latex_name_list.append(f"latex_{index}")
                item['latex_result'] = f"latex_{index}"
                if 'ocr_result' in item:
                    del item['ocr_result']
            else :
                if "ocr_result" in item : item['ocr_result'] = sorted( item['ocr_result'], key=lambda x: x[1])
        return name2latex,latex_name_list,page
    
    # 双栏
    elif DocAnalyse_result.ColumnType is ColumnType.double_column:
        page = copy.deepcopy(single_page_llm)
        page = double_column_sort(page)

        name2latex = {}
        latex_name_list = []
        for index,item in enumerate(page):
            if 'box_position' in item : del item['box_position']
            # if 'center_position' in item : del item['center_position']
            if 'latex_result' in item:
                name2latex[f"latex_{index}"] = item['latex_result']
                latex_name_list.append(f"latex_{index}")
                item['latex_result'] = f"latex_{index}"
                if 'ocr_result' in item:
                    del item['ocr_result']
            else :
                if "ocr_result" in item : item['ocr_result'] = sorted( item['ocr_result'], key=lambda x: x[1])
        return name2latex,latex_name_list,page
    else:
        raise ValueError('the input text is not one of single_column or double_column')




