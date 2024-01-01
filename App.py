#左側にドイツ語を書くと文法の間違いを修正してくれる。
import os
import openai
import streamlit as st
import difflib
import diff_viewer


#LANGUAGES = {"ドイツ語作文の文法チェック" : "EN", "日本語の誤字脱字チェック" : "JA", "丁寧表現変換" : "DE"}
#TRANSLATORMODEL = {"Gpt-4" : "0", "Chat GPT" : "1"}

def openai_api_load():    
    APIKEYINPUT = st.sidebar.text_input('OpenAI API Key', type='password')
    openai.api_key = APIKEYINPUT
    APIKEYOUTPUT = openai.api_key
    if APIKEYOUTPUT.startswith('sk-'):
        st.warning('API key is set correctly!', icon='✅')
        return True
    else:
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        return False

def Chatgpttranslator(text):
    #プロンプト生成
    prompt_template = """あなたはコードレビュアーです。入力されたプログラムに間違いがあれば修正し、使われていない変数などがあれば削除されたプログラムを返してください。
                        プログラムの入力がない場合、「プログラムを入力してください。問題をチェックできます」と返してください。
                        入力されたプログラムに問題がない場合はプログラムをそのまま返してください。
                        """
    CHATCOMPLETIONS_MODEL = "gpt-3.5-turbo-16k"
    #CHATCOMPLETIONS_MODEL = "gpt-4"
    promptchat = f"{prompt_template}\n\nQ: {text}\n"
    response = openai.ChatCompletion.create(
        model=CHATCOMPLETIONS_MODEL,
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": text},
        ]
    )['choices'][0]['message']['content'].strip(" \n")
    return response

def Chatgptexplain(gpt_input,gpt_output):
    #プロンプト生成
    prompt_template = """あなたはコードレビュアーです。inputされたプログラムの文法的な間違いが修正されたプログラムのoutputを読み、それぞれがなぜ修正されたか説明してください。
                        回答は箇条書きにしてください。
                        回答は日本語で返してください。
                        また、inputに何も入力されていない場合、「プログラムをチェックします」と返してください。
                        """
    CHATCOMPLETIONS_MODEL = "gpt-3.5-turbo-16k"
    #CHATCOMPLETIONS_MODEL = "gpt-4"
    promptchat = f"{prompt_template}\n\nInput:{gpt_input}\noutput:{gpt_output}"
    response = openai.ChatCompletion.create(
        model=CHATCOMPLETIONS_MODEL,
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": gpt_input},
            {"role": "user", "content": gpt_output},
        ]
    )['choices'][0]['message']['content'].strip(" \n")
    return response

def main():
    st.title("コードチェッカー")
    openai_api_load()
    main_container = st.container()
    left_col, right_col = main_container.columns(2)
    
    input_text = left_col.text_area('コードを入力してください', height=500)

    if input_text is not None:
        translated_text=Chatgpttranslator(text=input_text)
        input_lines = input_text.split('\n')
        translated_lines = translated_text.split('\n')
        output_txt = translated_text
    else:
        output_txt ="text here"
    
    right_col.text_area(
        "AIによって提案されたコード",
        value= output_txt,
        height=500,
    )
    
    gpt_explain=Chatgptexplain(input_text,output_txt,)

    st.write(f'比較結果：')
    lang="none"
    st.write(diff_viewer.diff_viewer(old_text=input_text, new_text=output_txt, lang=lang))
    st.write(gpt_explain)
    
if __name__ =="__main__":
    main()