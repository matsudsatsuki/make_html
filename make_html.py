import streamlit as st
from bs4 import BeautifulSoup

# Streamlit UIの設定
st.title('HTML変換ツール')

# ユーザー入力を取得
user_input_html = st.text_area("HTMLを入力してください", '<div>Hello, World!</div>')

# スタイルの設定
text_color = st.color_picker('テキスト色を選択してください', '#000000')
background_color = st.color_picker('背景色を選択してください', '#ffffff')
font_size = st.slider('フォントサイズを選択してください', 10, 36, 14)
font_family = st.text_input('フォント名を入力してください', 'Arial')

# タブ名の設定
tab_names = {
    '①メイン': st.text_input('メインタブの名前を入力してください', '①メイン'),
    '①サブ': st.text_input('サブタブの名前を入力してください', '①サブ')
}

# プレーヤー名の設定
player_names = {
    '②A': st.text_input('プレーヤーAの名前を入力してください', '②A'),
    '②B': st.text_input('プレーヤーBの名前を入力してください', '②B'),
    '②C': st.text_input('プレーヤーCの名前を入力してください', '②C'),
    '②D': st.text_input('プレーヤーDの名前を入力してください', '②D')
}

# HTMLを解析してスタイルを適用
soup = BeautifulSoup(user_input_html, 'html.parser')

# タイトルの設定
title = st.text_input('タイトルを入力してください', 'タイトル')

# <html>タグが存在しない場合の処理
if soup.html is None:
    html_tag = soup.new_tag("html")
    soup.append(html_tag)

if soup.head is None:
    head_tag = soup.new_tag("head")
    soup.html.insert(0, head_tag)

if soup.title is None:
    title_tag = soup.new_tag("title")
    soup.head.append(title_tag)

soup.title.string = title

# スタイルの適用
style = soup.new_tag('style')
style.string = f'''
    html {{
        font-size: {font_size}px;
        font-family: '{font_family}', sans-serif;
    }}
    body {{
        background-color: {background_color};
    }}
    .tab {{
        border: 1px solid {text_color};
        color: {text_color};
    }}
    .tabtitle {{
        background-color: {background_color};
        border-color: {text_color};
        color: {text_color};
    }}
    .player {{
        border-bottom-color: {text_color};
    }}
    .player b {{
        border-right-color: {text_color};
    }}
'''
soup.head.append(style)

# タブ名とプレーヤー名の変更
for tab in soup.select('.tab'):
    tab_title = tab.select_one('.tabtitle')
    if tab_title:
        tab_name = tab_title.get_text(strip=True)
        tab_title.string = tab_names.get(tab_name, tab_name)

    for player in tab.select('.player'):
        player_name = player.select_one('b').get_text(strip=True)
        player.select_one('b').string = player_names.get(player_name, player_name)

# 変換されたHTMLを表示
st.write('変換されたHTML:')
st.markdown(str(soup), unsafe_allow_html=True)
