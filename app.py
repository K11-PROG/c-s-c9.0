import streamlit as st
import json, os
from datetime import date

st.set_page_config(page_title='Catholic Saints Calendar', layout='centered')
st.markdown('## ✅ Catholic Saints Calendar — Minimal (August 2025, English)')

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f'Required file not found: {path}')
        st.stop()
    except Exception as e:
        st.error(f'Error loading {path}: {e}')
        st.stop()

calendar = load_json(os.path.join('data','calendar_2025_en.json'))
meditations = load_json(os.path.join('data','meditations_2025_en.json'))

st.caption('Loaded data files:')
st.write(list(os.listdir('data')))

st.markdown('---')
st.title('📅 Saints & Meditations — August 2025 (EN)')

selected = st.date_input('Select date', value=date(2025,8,1), min_value=date(2025,8,1), max_value=date(2025,8,31))
date_key = selected.isoformat()

entry = next((e for e in calendar if e.get('date')==date_key), None)

if entry:
    st.header(f"{entry.get('date')} — {entry.get('saint')}")
    st.write(f"**Feast type:** {entry.get('type')}")
    st.write(f"**Liturgical color:** {entry.get('color')}")
    st.markdown('### Meditation')
    st.info(meditations.get(date_key, 'No meditation available.'))
else:
    st.warning('No calendar entry for this date in the minimal dataset.')

st.markdown('---')
st.markdown('### ✍️ Personal notes (saved locally)')
notes_dir = 'notes'
os.makedirs(notes_dir, exist_ok=True)
notes_path = os.path.join(notes_dir, f"{date_key}.txt")
initial = ''
if os.path.exists(notes_path):
    try:
        with open(notes_path,'r',encoding='utf-8') as nf:
            initial = nf.read()
    except Exception:
        initial = ''
note = st.text_area('Your note for this date:', value=initial, height=200)
if st.button('Save note'):
    try:
        with open(notes_path,'w',encoding='utf-8') as nf:
            nf.write(note)
        st.success('Note saved locally.')
    except Exception as e:
        st.error(f'Failed to save note: {e}')
