from collections import defaultdict

import numpy as np
import streamlit as st
from wordler import Wordler, find_best_guess

"""
------------ Header ------------
"""
st.title("Wordle cheater")

caption = "\n".join(["1. Enter a word",
                     "2. Each letter in the word will be shown.",
                     "3. Click on each letter to input your guess result on Wordle.",
                     "4. Suggestions will show.",
                     "5. Repeat"])

st.caption(caption)

"""
------------ Declare variables ------------
"""

not_exist = Wordler.not_exist
wrong_pos = Wordler.wrong_pos
correct = Wordler.correct
next_state = {
    not_exist: wrong_pos,
    wrong_pos: correct,
    correct: not_exist
}
colormap = {
    not_exist: 'grey',
    wrong_pos: 'orange',
    correct: 'green'
}

wordler_key = 'wordler'
word_path = './words5.txt'

if wordler_key in st.session_state:
    wordler = st.session_state[wordler_key]
else:
    wordler = Wordler(word_path)
    st.session_state[wordler_key] = wordler

"""
------------ Input boxes ------------
"""

cols_input = st.columns(6)

text_inputs = [col.text_input(f"Word {i}") for i, col in enumerate(cols_input, start=1)]


def proc_text(text_):
    return list(text_.upper()[:5]) + ["*"] * max((5 - len(text_), 0))


texts_col_wise = [proc_text(t) for t in text_inputs if t]
texts_row_wise = [row for row in np.array(texts_col_wise).T]

word_states = defaultdict(lambda: set())

if texts_row_wise:
    cols = st.columns(len(texts_row_wise))

    for c, (text, col) in enumerate(zip(texts_row_wise, cols)):
        for r, t in enumerate(text):
            btn_key = f'btn_{r}_{c}'
            btn_state_key = btn_key + '_state'
            clicked = col.button(str(t), key=btn_key)
            if state := st.session_state.get(btn_state_key):
                if clicked:
                    state = next_state[state]
                    st.session_state[btn_state_key] = state
            else:
                state = not_exist
                st.session_state[btn_state_key] = not_exist
            col.markdown(f'<p style="color:{colormap[state].capitalize()}">{state}</p>', unsafe_allow_html=True)
            word_states[state].add((t, c))


"""
------------ Suggestion boxes ------------
"""

if len(word_states) > 0:
    hints = wordler.get_hint(word_states)
    best_guess = find_best_guess(hints)
    st.subheader(f"{len(hints)} suggestion(s)")
    st.text("Our best guess(es)")
    st.code("\n".join(best_guess))
    st.text("All suggestions")
    st.code("\n".join(hints))
