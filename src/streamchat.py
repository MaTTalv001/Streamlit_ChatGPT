import streamlit as st
import os
import openai
from streamlit_chat import message


#openai.api_key = "xxxxxxxx"
openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("ChatGPT APIに相談してみるアプリ")

if "generated" not in st.session_state:
   st.session_state.generated = []
if "past" not in st.session_state:
   st.session_state.past = []
if "mes_list" not in st.session_state:
   st.session_state.mes_list = []


bot_character = st.selectbox("誰に相談したいですか" , ["上品な男性", "上品な女性", "フレンドリーな男性", "フレンドリーな女性", "優しいおばあちゃん", "鬼軍曹", "チャラ男", "ギャル"])
advise_level = st.selectbox("どれくらい聞きたいですか" , ["三文以内で", "簡単に", "詳しく"])

system_role = {"role": "system", "content": "あなたは{}です。性格や口調はそれに合わせてください。その上で、親身になって質問者に寄り添った回答を{}お願いします。似たような具体的事例があればそれを教えてあげてもいいかもしれません。".format(bot_character,advise_level)}


if st.session_state.mes_list == []:
   st.session_state.mes_list.append(system_role)

def chatgpt_Q(system_role, messages_list, query):
  st.session_state.mes_list[0] = system_role
  messages_list.append({"role": "user", "content": query })
  st.session_state.past.append(query)
  res = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo",
      messages = messages_list
  )
  res_content = res["choices"][0]["message"]["content"]
  messages_list.append({"role": "assistant", "content": res_content})
  st.session_state.generated.append(res_content)
  
  return messages_list


with st.form("相談フォーム"):
  user_message = st.text_input("相談内容は？")

  submitted = st.form_submit_button("相談する")
  if submitted:
    
    conversation = chatgpt_Q(system_role, st.session_state.mes_list, user_message)
    # 挙動確認用。通常はコメントアウト
    # st.write(conversation)
    if st.session_state["generated"]:
      for i in range(len(st.session_state.generated) - 1, -1, -1):
          message(st.session_state.generated[i], key = str(i), avatar_style = "icons")
          message(st.session_state.past[i], is_user = True, key = str(i) + "_user", avatar_style = "thumbs")




reset_btn = st.sidebar.button("会話をリセットする")
if reset_btn:
   st.session_state.generated = []
   st.session_state.past = []
   st.session_state.mes_list = []
    
