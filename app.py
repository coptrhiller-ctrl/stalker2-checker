import streamlit as st
import streamlit.components.v1 as components
import struct
import ctypes
import os
import re
import subprocess
import random
from datetime import datetime
from collections import deque

# Настройка страницы (боковое меню скрыто по умолчанию)
st.set_page_config(
    page_title="S.T.A.L.K.E.R. 2 — Чекер Артефактов",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Инициализация состояний (State)
if "art_filter" not in st.session_state: 
    st.session_state.art_filter = "all"
if "stalker_id" not in st.session_state: 
    st.session_state.stalker_id = f"S.T.A.L.K.E.R. #{random.randint(100, 999)}"
if "processed_file_id" not in st.session_state: 
    st.session_state.processed_file_id = None
if "show_celebration" not in st.session_state: 
    st.session_state.show_celebration = False
if "lang" not in st.session_state: 
    st.session_state.lang = "ru"
if "show_chances" not in st.session_state: 
    st.session_state.show_chances = False
if "stage_idx" not in st.session_state: 
    st.session_state.stage_idx = 0

# =========================================================================
# СЛОВАРИ ПЕРЕВОДОВ И ДАННЫХ (RU, UK, EN)
# =========================================================================
T = {
    "ru": {
        "title": "Чекер Артефактов",
        "desc_1": "Тут вы легко сможете проверить какие артефакты вы уже собрали а какие еще остались для достижения",
        "desc_2": "«Собиратель чудес»",
        "desc_3": "(69 артов) а так же для ачивки",
        "desc_4": "«Все страньше и страньше»",
        "desc_5": "(6 архиартефактов)",
        "settings_title": "⚙️ Настройки",
        "show_chances": "Показывать шансы выпадения",
        "stage_select": "Ваш этап прохождения:",
        "stages": [
            "🟢 Старт игры, Малая Зона", 
            "🔵 После квеста «За семью замками»", 
            "🟡 Выполнил квесты в НИИЧАЗ", 
            "🔴 Штурмовал «Дугу»"
        ],
        "pda_title": "📡 ПДА: Активность",
        "pda_sub": "Последние проверки сталкеров",
        "pda_empty": "В Зоне пока тихо...<br/>Загрузите сохранение первым!",
        "upload_title": "📁 Инструкция по загрузке файла сохранения",
        "upload_text": "📁 Перетащите или загрузите по клику ваш файл <b>CampaignsSave.sav</b> в поле ниже.",
        "upload_btn": "Загрузите ваш файл сохранения (.sav)",
        "btn_all": "Показать все",
        "btn_hide_f": "Скрыть собранные",
        "btn_hide_m": "Скрыть не собранные",
        "celeb_all_title": "🏆 АБСОЛЮТНАЯ ЛЕГЕНДА ЗОНЫ!",
        "celeb_all_text": "Собраны абсолютно все артефакты и архиартефакты!",
        "celeb_base_title": "🏆 ПОЗДРАВЛЯЕМ!",
        "celeb_base_text": "Достижение «Собиратель чудес» выполнено! Вы нашли все 69 артефактов.",
        "celeb_weird_title": "🌀 ОТЛИЧНАЯ РАБОТА!",
        "celeb_weird_text": "Достижение «Все страньше и страньше» выполнено! Все архиартефакты у вас.",
        "celeb_desc": "Ваши старания окупились сполна. Зона уважает таких сталкеров.",
        "dl_btn": "📥 Скачать недостающие артефакты и команды",
        "base_arts": "Базовые",
        "arch_arts": "Архи"
    },
    "uk": {
        "title": "Чекер Артефактів",
        "desc_1": "Тут ви легко зможете перевірити які артефакти ви вже зібрали, а які ще залишилися для досягнення",
        "desc_2": "«Збирач чудес»",
        "desc_3": "(69 артів), а також для ачівки",
        "desc_4": "«Дедалі дивніше і дивніше»",
        "desc_5": "(6 архіартефактів)",
        "settings_title": "⚙️ Налаштування",
        "show_chances": "Показувати шанси випадіння",
        "stage_select": "Ваш етап проходження:",
        "stages": [
            "🟢 Старт гри, Мала Зона", 
            "🔵 Після квесту «За сімома замками»", 
            "🟡 Виконав квести в НДІЧАЗ", 
            "🔴 Штурмував «Дугу»"
        ],
        "pda_title": "📡 КПК: Активність",
        "pda_sub": "Останні перевірки сталкерів",
        "pda_empty": "У Зоні поки тихо...<br/>Завантажте збереження першим!",
        "upload_title": "📁 Інструкція із завантаження файлу збереження",
        "upload_text": "📁 Перетягніть або завантажте по кліку ваш файл <b>CampaignsSave.sav</b> у поле нижче.",
        "upload_btn": "Завантажте ваш файл збереження (.sav)",
        "btn_all": "Показати всі",
        "btn_hide_f": "Приховати зібрані",
        "btn_hide_m": "Приховати не зібрані",
        "celeb_all_title": "🏆 АБСОЛЮТНА ЛЕГЕНДА ЗОНИ!",
        "celeb_all_text": "Зібрано абсолютно всі артефакти та архіартефакти!",
        "celeb_base_title": "🏆 ВІТАЄМО!",
        "celeb_base_text": "Досягнення «Збирач чудес» виконано! Ви знайшли всі 69 артефактів.",
        "celeb_weird_title": "🌀 ЧУДОВА РОБОТА!",
        "celeb_weird_text": "Досягнення «Дедалі дивніше і дивніше» виконано! Всі архіартефакти у вас.",
        "celeb_desc": "Ваші старання окупилися сповна. Зона поважає таких сталкерів.",
        "dl_btn": "📥 Завантажити артефакти яких не вистачає та команди",
        "base_arts": "Базові",
        "arch_arts": "Архі"
    },
    "en": {
        "title": "Artifact Checker",
        "desc_1": "Here you can easily check which artifacts you have already collected and which are still missing for the",
        "desc_2": "\"Wonder Gatherer\"",
        "desc_3": "(69 arts) achievement, as well as for the",
        "desc_4": "\"Curiouser and Curiouser\"",
        "desc_5": "(6 arch-artifacts) achievement.",
        "settings_title": "⚙️ Settings",
        "show_chances": "Show artifact drop chances",
        "stage_select": "Your progression stage:",
        "stages": [
            "🟢 Game Start, Lesser Zone", 
            "🔵 After \"Behind Seven Seals\"", 
            "🟡 Completed SIRCAA quests", 
            "🔴 Assualted \"Duga\""
        ],
        "pda_title": "📡 PDA: Activity",
        "pda_sub": "Recent stalker checks",
        "pda_empty": "It's quiet in the Zone...<br/>Be the first to upload a save!",
        "upload_title": "📁 Save file upload instructions",
        "upload_text": "📁 Drag and drop or click to upload your <b>CampaignsSave.sav</b> file below.",
        "upload_btn": "Upload your save file (.sav)",
        "btn_all": "Show all",
        "btn_hide_f": "Hide found",
        "btn_hide_m": "Hide missing",
        "celeb_all_title": "🏆 ABSOLUTE ZONE LEGEND!",
        "celeb_all_text": "You have collected absolutely all artifacts and arch-artifacts!",
        "celeb_base_title": "🏆 CONGRATULATIONS!",
        "celeb_base_text": "\"Wonder Gatherer\" achieved! You found all 69 artifacts.",
        "celeb_weird_title": "🌀 GREAT JOB!",
        "celeb_weird_text": "\"Curiouser and Curiouser\" achieved! All arch-artifacts found.",
        "celeb_desc": "Your efforts have paid off. The Zone respects such stalkers.",
        "dl_btn": "📥 Download missing artifacts and spawn commands",
        "base_arts": "Base",
        "arch_arts": "Arch"
    }
}

# Шансы выпадения артефактов в зависимости от этапа (Ранг Скифа)
DROP_CHANCES = [
    {"🔘": "80%", "🔵": "20%", "🟣": "0%", "🟡": "0%"},      # Новичок
    {"🔘": "50%", "🔵": "48%", "🟣": "1.9%", "🟡": "0.1%"},   # Опытный
    {"🔘": "30%", "🔵": "59%", "🟣": "10%", "🟡": "1%"},      # Ветеран
    {"🔘": "10%", "🔵": "65%", "🟣": "20%", "🟡": "5%"}       # Мастер
]

# Перевод названий категорий
def get_cat_name(cat_ru_name, lang):
    if lang == "ru": return cat_ru_name
    map_uk = {
        "1. 🌌 ГРАВИТАЦИОННЫЕ АРТЕФАКТЫ": "1. 🌌 ГРАВІТАЦІЙНІ АРТЕФАКТИ",
        "2. 🔥 ТЕРМИЧЕСКИЕ АРТЕФАКТЫ": "2. 🔥 ТЕРМІЧНІ АРТЕФАКТИ",
        "3. ⚡ ЭЛЕКТРИЧЕСКИЕ АРТЕФАКТЫ": "3. ⚡ ЕЛЕКТРИЧНІ АРТЕФАКТИ",
        "4. 🧪 ХИМИЧЕСКИЕ АРТЕФАКТЫ": "4. 🧪 ХІМІЧНІ АРТЕФАКТИ",
        "5. 🌀 СТРАННЫЕ АРТЕФАКТЫ (Ачивка «Все страньше и страньше»)": "5. 🌀 ДИВНІ АРТЕФАКТИ (Ачівка «Дедалі дивніше»)"
    }
    map_en = {
        "1. 🌌 ГРАВИТАЦИОННЫЕ АРТЕФАКТЫ": "1. 🌌 GRAVITATIONAL ARTIFACTS",
        "2. 🔥 ТЕРМИЧЕСКИЕ АРТЕФАКТЫ": "2. 🔥 THERMAL ARTIFACTS",
        "3. ⚡ ЭЛЕКТРИЧЕСКИЕ АРТЕФАКТЫ": "3. ⚡ ELECTRICAL ARTIFACTS",
        "4. 🧪 ХИМИЧЕСКИЕ АРТЕФАКТЫ": "4. 🧪 CHEMICAL ARTIFACTS",
        "5. 🌀 СТРАННЫЕ АРТЕФАКТЫ (Ачивка «Все страньше и страньше»)": "5. 🌀 WEIRD ARTIFACTS (Curiouser and Curiouser)"
    }
    return map_uk.get(cat_ru_name, cat_ru_name) if lang == "uk" else map_en.get(cat_ru_name, cat_ru_name)

# =========================================================================
# ГЛОБАЛЬНАЯ ЛЕНТА ПРОВЕРОК (ПДА АКТИВНОСТЬ)
# =========================================================================
@st.cache_resource
def get_recent_checks():
    # Храним последние 15 проверок в оперативной памяти сервера
    return deque(maxlen=15)

# =========================================================================
# CUSTOM CSS / GAME INVENTORY GRID STYLES + HOVER TOOLTIP
# =========================================================================
st.markdown("""
<style>
    /* Глубокий тёмный фон */
    .stApp {
        background-color: #080A0F;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* ОГРАНИЧЕНИЕ ШИРИНЫ КОНТЕЙНЕРА И УВЕЛИЧЕННЫЙ ОТСТУП СВЕРХУ */
    .main .block-container,
    [data-testid="stMainBlockContainer"],
    [data-testid="block-container"],
    .stMainBlockContainer {
        max-width: 1020px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Зона загрузки файлов - РАСТЯНУТА И ОТЦЕНТРИРОВАНА */
    [data-testid="stFileUploader"] {
        background-color: #111520 !important;
        border: 2px dashed #FFB000 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        transition: all 0.3s ease;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #FFC107 !important;
        box-shadow: 0 0 20px rgba(255, 176, 0, 0.2);
    }

    [data-testid="stFileUploader"] section {
        padding: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"],
    [data-testid="stFileUploaderDropzone"] {
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ЧИСТЫЙ ПЕРЕВОД КНОПКИ БЕЗ НАЛОЖЕНИЯ ТЕКСТА */
    [data-testid="stFileUploaderDropzone"] button {
        font-size: 0 !important;
        padding: 8px 18px !important;
    }
    [data-testid="stFileUploaderDropzone"] button * {
        display: none !important;
    }
    [data-testid="stFileUploaderDropzone"] button::after {
        content: "📁 Выбрать файл" !important;
        font-size: 0.9rem !important;
        color: #E2E8F0 !important;
        display: inline-block !important;
    }

    /* ЧИСТЫЙ ПЕРЕВОД ТЕКСТА ЛИМИТА БЕЗ НАЛОЖЕНИЯ */
    [data-testid="stFileUploaderDropzone"] small {
        font-size: 0 !important;
        margin-top: 6px !important;
        display: block !important;
    }
    [data-testid="stFileUploaderDropzone"] small * {
        display: none !important;
    }
    [data-testid="stFileUploaderDropzone"] small::after {
        content: "До 200 МБ на файл • SAV" !important;
        font-size: 0.85rem !important;
        color: #94A3B8 !important;
        display: block !important;
    }

    /* СТИЛИ КНОПОК ФИЛЬТРАЦИИ С МЯГКОЙ ОБВОДКОЙ */
    .stButton > button {
        width: 100% !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Активная кнопка (Primary) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #1A2234 0%, #111520 100%) !important;
        border: 1px solid #FFB000 !important;
        color: #FFB000 !important;
        box-shadow: 0 0 16px rgba(255, 176, 0, 0.35), inset 0 0 10px rgba(255, 176, 0, 0.1) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 22px rgba(255, 176, 0, 0.5) !important;
        transform: translateY(-1px);
    }

    /* Неактивная кнопка (Secondary) */
    .stButton > button[kind="secondary"] {
        background: #111520 !important;
        border: 1px solid #1E2638 !important;
        color: #94A3B8 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #3A4256 !important;
        color: #F8FAFC !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        transform: translateY(-1px);
    }

    /* СТИЛЬ ССЫЛКИ В ПОДВАЛЕ */
    .steam-footer-link {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        text-decoration: none !important;
        color: #64748B !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.2s ease !important;
    }
    .steam-footer-link:hover {
        color: #CBD5E1 !important;
        text-decoration: underline !important;
    }
    .steam-footer-link img {
        opacity: 0.75;
        transition: opacity 0.2s ease, transform 0.2s ease;
    }
    .steam-footer-link:hover img {
        opacity: 1 !important;
        transform: scale(1.1);
    }

    /* СЕТКА ГАЛЕРЕИ С ЦЕНТРИРОВАНИЕМ НЕПОЛНЫХ РЯДОВ */
    .art-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        padding: 10px 0;
    }

    /* КОМПАКТНАЯ КАРТОЧКА-ПЛИТКА АРТЕФАКТА */
    .art-tile {
        position: relative;
        background: #111520;
        border-radius: 12px;
        border: 1px solid #1E2638;
        padding: 5px 0 0 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        height: 128px; 
        width: 135px;
        flex: 0 0 135px;
        cursor: pointer;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
        overflow: visible !important;
        box-sizing: border-box;
    }
    .art-tile:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
        border-color: #334155;
        z-index: 9999 !important;
    }

    /* ВСПЛЫВАЮЩАЯ ПОДСКАЗКА СТРОГО ПРИ НАВЕДЕНИИ (HOVER TOOLTIP) */
    .art-tile .tooltip-box {
        visibility: hidden;
        opacity: 0;
        width: 235px;
        background-color: #141A26;
        color: #F8FAFC;
        text-align: left;
        border-radius: 8px;
        padding: 10px 12px;
        border: 1px solid #FFB000;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.85);
        position: absolute;
        z-index: 99999 !important;
        bottom: 108%;
        left: 50%;
        transform: translateX(-50%) translateY(5px);
        transition: opacity 0.2s ease, visibility 0.2s ease, transform 0.2s ease;
        pointer-events: none;
        font-size: 0.78rem;
        line-height: 1.35;
    }

    .art-tile:hover .tooltip-box {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }

    /* Свечение для НАЙДЕННЫХ артефактов */
    .tile-found {
        border-color: #00E676 !important;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.3) !important;
        background: radial-gradient(circle at center, rgba(0, 230, 118, 0.08) 0%, #111520 80%);
    }
    .tile-found:hover {
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.5) !important;
    }

    .tile-missing {
        opacity: 0.65;
    }
    .tile-missing:hover {
        opacity: 1;
    }

    .tile-badge {
        position: absolute;
        top: 6px;
        right: 6px;
        z-index: 2;
    }

    /* ПЛОТНЫЙ КОНТЕЙНЕР КАРТИНКИ */
    .tile-img-container {
        width: 100%;
        height: 88px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0;
    }
    .tile-img {
        width: 78px;
        height: 78px;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.6));
    }

    /* БЛОК НАЗВАНИЯ ВНИЗУ КАРТОЧКИ */
    .tile-label-container {
        width: 100%;
        background: #0A0D14;
        border-top: 1px solid #1E2638;
        padding: 5px 4px;
        text-align: center;
        box-sizing: border-box;
        border-radius: 0 0 11px 11px;
        transition: all 0.2s ease;
    }
    .art-tile:hover .tile-label-container {
        background: #131926;
        border-top-color: rgba(255, 176, 0, 0.4);
    }
    .art-tile.tile-found .tile-label-container {
        border-top-color: rgba(0, 230, 118, 0.25);
        background: rgba(0, 230, 118, 0.05);
    }

    .tile-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #F1F5F9;
        text-align: center;
        line-height: 1.15;
        width: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
    }

    [data-testid="stMetric"] {
        background-color: #111520;
        border: 1px solid #1E2638;
        border-radius: 12px;
        padding: 16px;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #FFB000 0%, #E69500 100%) !important;
        color: #0A0D14 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 176, 0, 0.25) !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #FFC107 0%, #FFB000 100%) !important;
        box-shadow: 0 0 25px rgba(255, 176, 0, 0.5) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)


# =========================================================================
# ВЕРХНЕЕ МЕНЮ (ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКА)
# =========================================================================
lang_map = {"🇷🇺": "ru", "🇺🇦": "uk", "🇬🇧": "en"}
inv_lang = {"ru": 0, "uk": 1, "en": 2}

# Размещаем переключатель аккуратно справа сверху
col_space, col_lang = st.columns([8.5, 1.5])
with col_lang:
    selected_flag = st.radio(
        "Language", 
        ["🇷🇺", "🇺🇦", "🇬🇧"], 
        index=inv_lang[st.session_state.lang], 
        horizontal=True, 
        label_visibility="collapsed"
    )
    if lang_map[selected_flag] != st.session_state.lang:
        st.session_state.lang = lang_map[selected_flag]
        st.rerun()

lang = st.session_state.lang
ui = T[lang]

# =========================================================================
# БОКОВАЯ ПАНЕЛЬ (SIDEBAR): НАСТРОЙКИ И ПДА АКТИВНОСТЬ
# =========================================================================
st.sidebar.markdown(f"<h3 style='color: #F8FAFC; margin-bottom: 10px;'>{ui['settings_title']}</h3>", unsafe_allow_html=True)
show_chances = st.sidebar.toggle(ui['show_chances'], value=st.session_state.show_chances)
st.session_state.show_chances = show_chances

if show_chances:
    stage = st.sidebar.selectbox(ui['stage_select'], options=ui['stages'], index=st.session_state.stage_idx)
    st.session_state.stage_idx = ui['stages'].index(stage)

st.sidebar.markdown("<hr style='border-color: #1E2638; margin: 20px 0;'>", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="color: #F8FAFC; margin: 0; font-size: 1.4rem; font-weight: 800;">{ui['pda_title']}</h2>
    <span style="color: #94A3B8; font-size: 0.85rem;">{ui['pda_sub']}</span>
</div>
""", unsafe_allow_html=True)

feed = get_recent_checks()
if not feed:
    st.sidebar.markdown(f"""
    <div style="text-align: center; color: #64748B; font-size: 0.9rem; padding: 25px; border: 1px dashed #1E2638; border-radius: 10px; background: rgba(17, 21, 32, 0.5);">
        {ui['pda_empty']}
    </div>
    """, unsafe_allow_html=True)
else:
    for item in feed:
        achievements = ""
        if item['base'] == 69: achievements += "🏆 "
        if item['weird'] == 6: achievements += "🌀"
            
        border_color = '#00E676' if achievements else '#1E2638'
        bg_color = 'rgba(0, 230, 118, 0.05)' if achievements else '#111520'
        
        st.sidebar.markdown(f"""
        <div style="background-color: {bg_color}; border: 1px solid #1E2638; border-left: 3px solid {border_color}; border-radius: 8px; padding: 12px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="color: #F8FAFC; font-weight: 700; font-size: 0.95rem;">{item['name']} {achievements}</span>
                <span style="color: #64748B; font-size: 0.75rem;">{item['time']}</span>
            </div>
            <div style="color: #CBD5E1; font-size: 0.85rem; display: flex; gap: 15px; font-weight: 500;">
                <span>{ui['base_arts']}: <b style="color: {'#00E676' if item['base']==69 else '#E2E8F0'};">{item['base']}/69</b></span>
                <span>{ui['arch_arts']}: <b style="color: {'#00E676' if item['weird']==6 else '#E2E8F0'};">{item['weird']}/6</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# АВТО-КОМПИЛЯЦИЯ КРАКЕН-ДЕКОДЕРА ДЛЯ LINUX (STREAMLIT CLOUD)
# =========================================================================
@st.cache_resource
def get_linux_decompressor():
    so_path = os.path.abspath("libooz.so")
    if os.path.exists(so_path):
        return so_path

    try:
        if os.path.exists("ooz_src") and not os.path.exists(so_path):
            import shutil
            shutil.rmtree("ooz_src", ignore_errors=True)

        if not os.path.exists("ooz_src"):
            res = subprocess.run("git clone https://github.com/powzix/ooz.git ooz_src", shell=True, capture_output=True, text=True)
            if res.returncode != 0:
                st.error(f"Ошибка клонирования репозитория: {res.stderr}")
                return None

        clean_stdafx = """#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
#include <sys/stat.h>
#include <immintrin.h>

typedef uint8_t uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;
typedef uint64_t uint64;
typedef int8_t int8;
typedef int16_t int16;
typedef int32_t int32;
typedef int64_t int64;
typedef uint8_t byte;

#define WINAPI
#define HINSTANCE void*
#define HMODULE void*
#define __forceinline inline __attribute__((always_inline))

#undef _rotl
#define _rotl(x, r) (((uint32_t)(x) << (r)) | ((uint32_t)(x) >> (32 - (r))))

#undef _byteswap_ulong
#define _byteswap_ulong __builtin_bswap32

#undef _byteswap_ushort
#define _byteswap_ushort __builtin_bswap16

#undef _byteswap_uint64
#define _byteswap_uint64 __builtin_bswap64

static inline unsigned char _BitScanReverse(unsigned long *Index, uint32_t Mask) {
    if (Mask == 0) return 0;
    *Index = 31 - __builtin_clz(Mask);
    return 1;
}

static inline unsigned char _BitScanForward(unsigned long *Index, uint32_t Mask) {
    if (Mask == 0) return 0;
    *Index = __builtin_ctz(Mask);
    return 1;
}
"""
        with open("ooz_src/stdafx.h", "w") as f:
            f.write(clean_stdafx)

        kraken_cpp = "ooz_src/kraken.cpp"
        with open(kraken_cpp, "r") as f:
            code = f.read()

        if "void LoadLib()" in code:
            code = code.split("void LoadLib()")[0]
        elif "int main(" in code:
            code = code.split("int main(")[0]

        relaxed_fn = """
        #include <stdint.h>
        extern "C" int64_t OozKraken_Decompress(const unsigned char *src, int64_t src_len, unsigned char *dst, int64_t dst_len) {
            KrakenDecoder *dec = Kraken_Create();
            int offset = 0;
            size_t remaining_dst = (size_t)dst_len;
            size_t remaining_src = (size_t)src_len;
            const unsigned char *p = src;
            while (remaining_dst != 0) {
                if (!Kraken_DecodeStep(dec, dst, offset, remaining_dst, p, remaining_src)) { Kraken_Destroy(dec); return offset > 0 ? offset : -1; }
                if (dec->src_used == 0) { Kraken_Destroy(dec); return offset > 0 ? offset : -1; }
                p += dec->src_used;
                remaining_src -= dec->src_used;
                remaining_dst -= dec->dst_used;
                offset += dec->dst_used;
            }
            Kraken_Destroy(dec);
            return offset;
        }
        """
        with open(kraken_cpp, "w") as f:
            f.write(code + "\n" + relaxed_fn)

        compile_cmd = "cd ooz_src && g++ -O3 -shared -fPIC -msse4.1 -w -o ../libooz.so kraken.cpp bitknit.cpp lzna.cpp"
        res = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)

        if res.returncode != 0:
            st.error(f"Ошибка компиляции декомпрессора:\n{res.stderr}")
            return None

        if os.path.exists(so_path):
            return so_path
    except Exception as e:
        st.error(f"Исключение при сборке: {e}")
    return None

# =========================================================================
# БАЗА ДАННЫХ АРТЕФАКТОВ (SID, Название, Вес, Эффекты)
# =========================================================================
CATEGORIES = [
    {
        "name": "1. 🌌 ГРАВИТАЦИОННЫЕ АРТЕФАКТЫ",
        "items": [
            ("GArtifactGoldFish", "🔘 Золотая рыбка", "0.35 кг", "+10% Радиация, +3 кг Вес"),
            ("GArtifactStoneDrop", "🔘 Каменное сердце", "0.65 кг", "+10% Радиация, +3 кг Вес"),
            ("GArtifactGravy", "🔘 Грави", "0.65 кг", "-10% Радиация, +3 кг Вес"),
            ("GArtifactWrenched", "🔘 Выверт", "0.40 кг", "+10% Физическая защита"),
            ("GArtifactBloodStone", "🔘 Кровь камня", "0.55 кг", "+10% Радиация, +3 кг Вес"),
            ("GArtifactTrunk", "🔘 Канифоль", "0.40 кг", "+1.5 /с Выносливость, +2 кг Вес"),
            ("GArtifactSponge", "🔘 Вихрь", "0.30 кг", "+7% Физическая защита, +1.5 /с Выносливость, -10% Радиация"),
            ("GArtifactPlane", "🔘 Галька", "0.30 кг", "+7% Физическая защита, +1.5 /с Выносливость, +10% Радиация"),
            ("GArtifactLandSlug", "🔘 Медуза", "0.40 кг", "+10% Физическая защита, +10% Радиация"),
            ("GArtifactSpring", "🔵 Пружина", "0.45 кг", "+15% Радиация, +6 кг Вес"),
            ("GArtifactGraphiteBlock", "🔵 Корона", "0.60 кг", "+10% Физическая защита, +2.5 /с Выносливость, +15% Радиация"),
            ("GArtifactHedgehog", "🔵 Мухоловка", "0.35 кг", "-15% Радиация, +6 кг Вес"),
            ("GArtifactNightStar", "🟣 Ночная звезда", "0.60 кг", "+25% Радиация, +9 кг Вес"),
            ("GArtifactSplitStone", "🟣 Битый камень", "0.60 кг", "+25% Физическая защита, +25% Радиация"),
            ("GArtifactBud", "🟣 Бутон", "0.40 кг", "+25% Физическая защита, +5.0 /с Выносливость, +25% Радиация"),
            ("GArtifactCompass", "🟡 Компас", "0.50 кг", "+90% Физическая защита, +50% Радиация"),
            ("GArtifactRubiksCube", "🟡 Кубик-Рубик", "0.40 кг", "+50% Физическая защита, +50% Радиация")
        ]
    },
    {
        "name": "2. 🔥 ТЕРМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("FArtifactFireBall", "🔘 Огненный шар", "0.50 кг", "+10% Термозащита, -10% Радиация"),
            ("FArtifactSteak", "🔘 Бифштекс", "0.55 кг", "+5% Сопротивление кровотечению, +10% Радиация"),
            ("FArtifactGlass", "🔘 Полость", "0.40 кг", "+3% Сопротивление кровотечению, +2 кг Вес, +10% Радиация"),
            ("FArtifactBurntHunk", "🔘 Вертушка", "0.35 кг", "+5% Сопротивление кровотечению, -10% Радиация"),
            ("FArtifactResin", "🔘 Лира", "0.50 кг", "+3% Сопротивление кровотечению, +2 кг Вес"),
            ("FArtifactDrops", "🔘 Капля", "0.45 кг", "+10% Термозащита, +10% Радиация"),
            ("FArtifactEye", "🔘 Глаз", "0.40 кг", "+10% Термозащита"),
            ("FArtifactCrystal", "🔘 Кристалл", "0.65 кг", "+10% Термозащита, +10% Радиация"),
            ("FArtifactMomsBeads", "🟣 Мамины Бусы", "0.40 кг", "+10% Сопротивление кровотечению, +15% Радиация"),
            ("FArtifactBakedBolts", "🔵 Брак", "0.55 кг", "+5% Сопротивление кровотечению, +3 кг Вес, +15% Радиация"),
            ("FArtifactDeadSponge", "🔵 Мёртвая губка", "0.30 кг", "+10% Сопротивление кровотечению, +15% Радиация"),
            ("FArtifactHellishHedgehog", "🔵 Магма", "0.55 кг", "+10% Термозащита, +3 кг Вес, +15% Радиация"),
            ("FArtifactPlasma", "🔵 Плазма", "0.50 кг", "+15% Термозащита, -15% Радиация"),
            ("FArtifactCandle", "🟣 Лепесток", "0.30 кг", "+20% Сопротивление кровотечению, +25% Радиация"),
            ("FArtifactFireworks", "🟣 Мясная зажигалка", "0.40 кг", "+20% Термозащита, +25% Радиация"),
            ("FArtifactCore", "🟣 Факел", "0.55 кг", "+15% Термозащита, +6 кг Вес, +25% Радиация"),
            ("FArtifactRingOmnipotence", "🟡 Гиперкуб", "0.60 кг", "+35% Термозащита, +40% Кровотечение, +50% Радиация")
        ]
    },
    {
        "name": "3. ⚡ ЭЛЕКТРИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("EArtifactFlash", "🔘 Вспышка", "0.30 кг", "+10% Электрозащита, +10% Радиация"),
            ("EArtifactSnowflake", "🔘 Снежинка", "0.30 кг", "+2.5 /с Выносливость, +10% Радиация"),
            ("EArtifactDummy", "🔘 Пустышка", "0.45 кг", "+2.5 /с Выносливость"),
            ("EArtifactBattery", "🔘 Батарейка", "0.40 кг", "+2.5 /с Выносливость, +10% Радиация"),
            ("EArtifactJellyFish", "🔘 Сапфир", "0.65 кг", "+1.5 /с Выносливость, +3% Кровотечение"),
            ("EArtifactWorm", "🔘 Крысиный король", "0.35 кг", "+7% Электрозащита, +3% Кровотечение, -10% Радиация"),
            ("EArtifactSparkler", "🔘 Бенгальский огонь", "0.40 кг", "+10% Электрозащита, -10% Радиация"),
            ("EArtifactChocolate", "🔘 Шоколадка", "0.40 кг", "+10% Электрозащита, +10% Радиация"),
            ("EArtifactSoul", "🔵 Душа", "0.40 кг", "+5.0 /с Выносливость, +15% Радиация"),
            ("EArtifactMoonlight", "🔵 Лунный свет", "0.55 кг", "+15% Электрозащита, +15% Радиация"),
            ("EArtifactTow", "🔵 Урок труда", "0.40 кг", "+2.5 /с Выносливость, +5% Кровотечение, +15% Радиация"),
            ("EArtifactThunderHedgehog", "🔵 Фонарь", "0.55 кг", "+15% Электрозащита, -15% Радиация"),
            ("EArtifactCloud", "🔵 Арфа", "0.40 кг", "+10% Электрозащита, +5% Кровотечение, +15% Радиация"),
            ("EArtifactAtom", "🟣 Блик", "0.30 кг", "+20% Электрозащита, +25% Радиация"),
            ("EArtifactRazor", "🟣 Морская звезда", "0.55 кг", "+5.0 /с Выносливость, +10% Кровотечение, +25% Радиация"),
            ("EArtifactCrystalGlass", "🟣 Гребень", "0.45 кг", "+7.5 /с Выносливость, +25% Радиация"),
            ("EArtifactDope", "🟡 Грозовая ягода", "0.50 кг", "+12.5 /с Выносливость, +50% Радиация")
        ]
    },
    {
        "name": "4. 🧪 ХИМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("CArtifactCrystalThorn", "🔘 Кристальная колючка", "0.50 кг", "-10% Радиация"),
            ("CArtifactThorn", "🔘 Колючка", "0.35 кг", "-10% Радиация"),
            ("CArtifactChunkMeat", "🔘 Ломоть мяса", "0.45 кг", "+10% Химзащита, +10% Радиация"),
            ("CArtifactBubble", "🔵 Пузырь", "0.40 кг", "-15% Радиация"),
            ("CArtifactSlug", "🔘 Слизняк", "0.60 кг", "-10% Радиация"),
            ("CArtifactSlime", "🔘 Слизь", "0.65 кг", "+10% Прочность экипировки, -10% Радиация"),
            ("CArtifactKryptonite", "🔘 Плесень", "0.55 кг", "+10% Химзащита, +10% Радиация"),
            ("CArtifactBung", "🔘 Рог", "0.30 кг", "+10% Прочность экипировки, +10% Химзащита, +10% Радиация"),
            ("CArtifactCottonWool", "🔘 Скорлупа", "0.30 кг", "+10% Химзащита, +10% Прочность экипировки, +10% Радиация"),
            ("CArtifactMica", "🔘 Слюда", "0.40 кг", "-10% Радиация"),
            ("CArtifactBun", "🔵 Колобок", "0.45 кг", "+15% Химзащита, +10% Прочность экипировки, +15% Радиация"),
            ("CArtifactEchinus", "🔵 Морской еж", "0.35 кг", "-15% Радиация"),
            ("CArtifactRosin", "🔵 Завтрак туриста", "0.35 кг", "+15% Химзащита, +20% Прочность экипировки, +15% Радиация"),
            ("CArtifactPlasticine", "🔵 Инфузория", "0.35 кг", "+15% Химзащита, +20% Прочность экипировки, +15% Радиация"),
            ("CArtifactPellicle", "🟣 Плёнка", "0.35 кг", "+20% Химзащита, -25% Радиация"),
            ("CArtifactBouncyBall", "🟣 Попрыгунчик", "0.40 кг", "-25% Радиация"),
            ("CArtifactDevilsMushroom", "🟣 Чёртов гриб", "0.45 кг", "+20% Химзащита, +30% Прочность экипировки, +25% Радиация"),
            ("CArtifactLiquidStone", "🟡 Жидкий камень", "0.60 кг", "+35% Химзащита, +40% Прочность экипировки, -50% Радиация")
        ]
    },
    {
        "name": "5. 🌀 СТРАННЫЕ АРТЕФАКТЫ (Ачивка «Все страньше и страньше»)",
        "items": [
            ("AArtifactWeirdWater", "🌀 Странная вода", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdBall", "🌀 Странный мяч", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdNut", "🌀 Странная гайка", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdBolt", "🌀 Странный болт", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdKettle", "🌀 Странный котелок", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdFlower", "🌀 Странный цветок", "0.50 кг", "Аномальный квестовый артефакт")
        ]
    }
]

SVG_CHECK_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzAwRTY3NiIgZmlsbC1vcGFjaXR5PSIwLjIiIHN0cm9rZT0iIzAwRTY3NiIgc3Ryb2tlLXdpZHRoPSIyIi8+PHBhdGggZD0iTTggMTJMMTEgMTVMMTYgOSIgc3Ryb2tlPSIjMDBFNjc2IiBzdHJva2Utd2lkdGg9IjIuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+"
SVG_CROSS_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzFFMjYzOCIgZmlsbC1vcGFjaXR5PSIwLjgiIHN0cm9rZT0iIzMzNDE1NSIgc3Ryb2tlLXdpZHRoPSIxLjUiLz48cGF0aCBkPSJNOSA5TDE1IDE1TTE1IDlMOSAxNSIgc3Ryb2tlPSIjNjQ3NDhCIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg=="

# ФУНКЦИЯ ДЛЯ ГЕНЕРАЦИИ СТРОКИ С ИКОНКОЙ И ЦВЕТОМ ТЕКСТА
def format_stat_with_icon(stat_text):
    stat_clean = stat_text.strip()
    stat_lower = stat_clean.lower()
    icon_name = None
    
    if "вес" in stat_lower or "weight" in stat_lower:
        icon_name = "Texture_Icon_Weight.png"
    elif "радиация" in stat_lower or "radiation" in stat_lower:
        icon_name = "Texture_Icon_Radiation.png"
    elif "физическая защита" in stat_lower or "physical" in stat_lower:
        icon_name = "Texture_Icon_PhysicalProtection.png"
    elif "выносливость" in stat_lower or "stamina" in stat_lower:
        icon_name = "Texture_Icon_EnergyRegen.png"
    elif "термозащита" in stat_lower or "thermal" in stat_lower:
        icon_name = "Texture_Icon_ThermalProtection.png"
    elif "кровотечени" in stat_lower or "bleeding" in stat_lower:
        icon_name = "Texture_Icon_Bleeding.png"
    elif "электрозащита" in stat_lower or "electrical" in stat_lower:
        icon_name = "Texture_Icon_ElectricalProtection.png"
    elif "химзащита" in stat_lower or "chemical" in stat_lower:
        icon_name = "Texture_Icon_ChemicalProtection.png"
    elif "прочность" in stat_lower or "durability" in stat_lower:
        icon_name = "T_Icon_Durability_Armor.png"

    if "радиация" in stat_lower or "radiation" in stat_lower:
        is_good = stat_lower.startswith("-")
    else:
        is_good = not stat_lower.startswith("-") if (stat_lower.startswith("+") or stat_lower.startswith("-")) else None

    if is_good is True:
        text_color = "#00E676"  # Салатовый
    elif is_good is False:
        text_color = "#FF5252"  # Красный
    else:
        text_color = "#CBD5E1"  # Нейтральный серый

    if icon_name:
        img_main = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/{icon_name}"
        img_master = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/{icon_name}"
        return f'<div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; color: {text_color}; font-weight: 600;"><img src="{img_main}" onerror="this.onerror=null; this.src=\'{img_master}\';" style="width: 15px; height: 15px; object-fit: contain;" /><span>{stat_clean}</span></div>'
    else:
        return f'<div style="margin-bottom: 3px; color: {text_color}; font-weight: 500;">• {stat_clean}</div>'

# =========================================================================
# РАСПАКОВКА И ЧТЕНИЕ В ПАМЯТИ
# =========================================================================
def decompress_sav(bytes_data):
    if len(bytes_data) < 8:
        return None

    uncompressed_size = struct.unpack("<I", bytes_data[:4])[0]
    compressed_data = bytes_data[4:]

    so_path = get_linux_decompressor()
    
    if so_path and os.path.exists(so_path):
        try:
            lib = ctypes.cdll.LoadLibrary(so_path)
            dst_buf = ctypes.create_string_buffer(uncompressed_size)
            
            if hasattr(lib, "OozKraken_Decompress"):
                fn = lib.OozKraken_Decompress
                fn.argtypes = [ctypes.c_char_p, ctypes.c_int64, ctypes.c_char_p, ctypes.c_int64]
                fn.restype = ctypes.c_int64
                res = fn(compressed_data, len(compressed_data), dst_buf, uncompressed_size)
                if res > 0:
                    return dst_buf.raw
        except Exception:
            pass

    try:
        for dll_name in ["./ooz_decompress.dll", "./oo2core_9_win64.dll"]:
            if os.path.exists(dll_name):
                lib = ctypes.cdll.LoadLibrary(dll_name)
                dst_buf = ctypes.create_string_buffer(uncompressed_size)
                fn = lib.OodleLZ_Decompress
                fn.argtypes = [ctypes.c_char_p, ctypes.c_int64, ctypes.c_char_p, ctypes.c_int64, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int64, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int64, ctypes.c_int]
                fn.restype = ctypes.c_int64
                res = fn(compressed_data, len(compressed_data), dst_buf, uncompressed_size, 0,0,0,None,0,None,None,None,0,0)
                if res == uncompressed_size:
                    return dst_buf.raw
    except Exception:
        pass
        
    return None

def find_sids(raw_bytes):
    found = set()
    if not raw_bytes: return found
    for cat in CATEGORIES:
        for item in cat["items"]:
            sid = item[0]
            if sid.encode("ascii") in raw_bytes or sid.encode("utf-16le") in raw_bytes:
                found.add(sid)
    return found

# =========================================================================
# ИНТЕРФЕЙС ГЛАВНОГО ЭКРАНА
# =========================================================================
st.markdown(f"""
<div style="text-align: center; padding: 0 0 5px 0;">
    <div style="display: inline-block; background: rgba(255, 176, 0, 0.1); border: 1px solid rgba(255, 176, 0, 0.3); border-radius: 20px; padding: 4px 16px; color: #FFB000; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;">
        ☢️ S.T.A.L.K.E.R. 2 • Patch v1.9
    </div>
    <h1 style="color: #F8FAFC; font-size: 2.8rem; font-weight: 800; margin: 0; display: flex; align-items: center; justify-content: center; gap: 14px; flex-wrap: wrap;">
        <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/Header.png" 
             onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/Header.png';" 
             style="width: 60px; height: 60px; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(255,176,0,0.3));" />
        <span>{ui['title']}</span>
    </h1>
</div>

<div style="margin: 20px auto; width: 100%; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.4); border: 1px solid #1E2638;">
    <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/info_{lang}.png"
         onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/info_{lang}.png';"
         style="width: 100%; display: block; object-fit: cover;" />
</div>

<div style="text-align: center;">
    <p style="color: #94A3B8; font-size: 0.98rem; margin-top: 10px; max-width: 850px; margin-left: auto; margin-right: auto; line-height: 1.6;">
        {ui['desc_1']} 
        <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/chud.png" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/chud.png';" style="width: 22px; height: 22px; vertical-align: sub; margin: 0 2px;" />
        <b style="color: #FFA600;">{ui['desc_2']}</b> {ui['desc_3']} 
        <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/stran.png" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/stran.png';" style="width: 22px; height: 22px; vertical-align: sub; margin: 0 2px;" />
        <b style="color: #FFA600;">{ui['desc_4']}</b> {ui['desc_5']}
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander(ui['upload_title'], expanded=True):
    instruction_html = f"""<div style="text-align: center; color: #94A3B8; font-size: 0.92rem; line-height: 1.6; padding: 4px 0;">
<p style="margin-top: 0; font-weight: 600; color: #F1F5F9; font-size: 0.96rem;">
{ui['upload_text']}
</p>
<div style="margin-top: 12px;">
<div style="color: #FFB000; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.5px; margin-bottom: 4px;">
STEAM:
</div>
<div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap;">
<code class="copy-path" data-copy="C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\STEAM\\SaveGames" 
      style="color: #00E676; background: #111520; padding: 6px 12px; border-radius: 6px; border: 1px solid #1E2638; cursor: pointer; font-weight: 600; font-size: 0.85rem;">
C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\STEAM\\SaveGames
</code>
</div>
</div>
<div style="margin-top: 12px;">
<div style="color: #FFB000; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.5px; margin-bottom: 4px;">
GAME PASS / EPIC GAMES:
</div>
<div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap;">
<code class="copy-path" data-copy="C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\SaveGames" 
      style="color: #00E676; background: #111520; padding: 6px 12px; border-radius: 6px; border: 1px solid #1E2638; cursor: pointer; font-weight: 600; font-size: 0.85rem;">
C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\SaveGames
</code>
</div>
</div>
</div>"""
    
    if hasattr(st, "html"):
        st.html(instruction_html)
    else:
        st.markdown(instruction_html, unsafe_allow_html=True)

uploaded_file = st.file_uploader(ui['upload_btn'], type=["sav"])

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    raw_data = decompress_sav(bytes_data)

    if raw_data is None:
        st.error("❌ Не удалось расшифровать файл сохранения. Убедитесь, что это файл формата S.T.A.L.K.E.R. 2.")
    else:
        found_sids = find_sids(raw_data)

        base_found = 0
        base_total = 69
        weird_found = 0
        weird_total = 6

        for cat in CATEGORIES:
            is_weird = "СТРАННЫЕ" in cat["name"]
            for item in cat["items"]:
                sid = item[0]
                if sid in found_sids:
                    if is_weird: 
                        weird_found += 1
                    else: 
                        base_found += 1

        total_all_arts = base_total + weird_total
        total_found_arts = base_found + weird_found
        total_missing_arts = total_all_arts - total_found_arts

        base_pct = int(base_found / base_total * 100)
        weird_pct = int(weird_found / weird_total * 100)

        # =========================================================================
        # ЛОГИРОВАНИЕ ПРОВЕРКИ (ПДА АКТИВНОСТЬ) И ПРАЗДНОВАНИЕ (САЛЮТ)
        # =========================================================================
        current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        if st.session_state.processed_file_id != current_file_id:
            st.session_state.processed_file_id = current_file_id
            
            global_feed = get_recent_checks()
            global_feed.appendleft({
                "name": st.session_state.stalker_id,
                "base": base_found,
                "weird": weird_found,
                "time": datetime.now().strftime("%H:%M")
            })
            
            if base_found == base_total or weird_found == weird_total:
                st.balloons()
                st.session_state.show_celebration = True
            else:
                st.session_state.show_celebration = False

        if st.session_state.get("show_celebration", False):
            if base_found == base_total and weird_found == weird_total:
                celeb_title = ui['celeb_all_title']
                celeb_text = ui['celeb_all_text']
            elif base_found == base_total:
                celeb_title = ui['celeb_base_title']
                celeb_text = ui['celeb_base_text']
            elif weird_found == weird_total:
                celeb_title = ui['celeb_weird_title']
                celeb_text = ui['celeb_weird_text']
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, rgba(0,230,118,0.08) 0%, rgba(255,176,0,0.08) 100%); 
                        border: 1px solid rgba(0,230,118,0.4); border-radius: 12px; padding: 18px 20px; 
                        margin: 25px 0 15px 0; text-align: center; box-shadow: 0 0 25px rgba(0,230,118,0.15);">
                <h3 style="color: #00E676; margin: 0 0 5px 0; font-weight: 800; font-size: 1.4rem; letter-spacing: 0.5px;">{celeb_title}</h3>
                <p style="color: #F8FAFC; font-weight: 600; margin: 0 0 5px 0; font-size: 1.05rem;">{celeb_text}</p>
                <p style="color: #94A3B8; margin: 0; font-size: 0.9rem; font-style: italic;">{ui['celeb_desc']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 18px 20px; display: flex; align-items: center; gap: 18px;">
                <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/art.png"
                     onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/art.png';"
                     style="width: 65px; height: 65px; object-fit: contain; flex-shrink: 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));" />
                <div style="flex-grow: 1;">
                    <div style="color: #94A3B8; font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;">
                        {ui['desc_2']} (69)
                    </div>
                    <div style="display: flex; align-items: baseline; justify-content: space-between;">
                        <span style="color: #F8FAFC; font-size: 1.8rem; font-weight: 800;">{base_found} / {base_total}</span>
                        <span style="color: #00E676; font-size: 0.95rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 10px;">
                            {base_pct}%
                        </span>
                    </div>
                    <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 8px; margin-top: 10px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {base_pct}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 18px 20px; display: flex; align-items: center; gap: 18px;">
                <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/arch.png"
                     onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/arch.png';"
                     style="width: 65px; height: 65px; object-fit: contain; flex-shrink: 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));" />
                <div style="flex-grow: 1;">
                    <div style="color: #94A3B8; font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;">
                        {ui['desc_4']} (6)
                    </div>
                    <div style="display: flex; align-items: baseline; justify-content: space-between;">
                        <span style="color: #F8FAFC; font-size: 1.8rem; font-weight: 800;">{weird_found} / {weird_total}</span>
                        <span style="color: #00E676; font-size: 0.95rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 10px;">
                            {weird_pct}%
                        </span>
                    </div>
                    <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 8px; margin-top: 10px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {weird_pct}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # =========================================================================
        # 3 КНОПКИ ФИЛЬТРАЦИИ
        # =========================================================================
        f_col1, f_col2, f_col3 = st.columns(3)

        with f_col1:
            if st.button(f"{ui['btn_all']} [{total_all_arts}]", use_container_width=True, type="primary" if st.session_state.art_filter == "all" else "secondary"):
                st.session_state.art_filter = "all"
                st.rerun()

        with f_col2:
            if st.button(f"{ui['btn_hide_f']} [{total_found_arts}]", use_container_width=True, type="primary" if st.session_state.art_filter == "missing" else "secondary"):
                st.session_state.art_filter = "missing"
                st.rerun()

        with f_col3:
            if st.button(f"{ui['btn_hide_m']} [{total_missing_arts}]", use_container_width=True, type="primary" if st.session_state.art_filter == "found" else "secondary"):
                st.session_state.art_filter = "found"
                st.rerun()

        st.markdown("<br/>", unsafe_allow_html=True)

        # =========================================================================
        # ВЫВОД КАТЕГОРИЙ И АРТЕФАКТОВ
        # =========================================================================
        for cat in CATEGORIES:
            cat_found_count = sum(1 for item in cat["items"] if item[0] in found_sids)
            cat_total_count = len(cat["items"])
            
            cat_title_display = get_cat_name(cat['name'], lang)
            cat_title = f"{cat_title_display} [{cat_found_count}/{cat_total_count}]"

            filtered_items = []
            for item in cat["items"]:
                sid = item[0]
                is_found = sid in found_sids
                
                if st.session_state.art_filter == "missing" and is_found:
                    continue
                if st.session_state.art_filter == "found" and not is_found:
                    continue
                    
                filtered_items.append(item)

            if not filtered_items:
                continue

            with st.expander(cat_title, expanded=True):
                grid_html = '<div class="art-grid">\n'
                
                for idx, item in enumerate(filtered_items):
                    sid, ru_name, weight, effects = item[0], item[1], item[2], item[3]
                    is_found = sid in found_sids
                    
                    status_svg = f'<img src="{SVG_CHECK_B64}" width="18" height="18" />' if is_found else f'<img src="{SVG_CROSS_B64}" width="18" height="18" />'
                    status_class = "tile-found" if is_found else "tile-missing"
                    
                    clean_name = ru_name[2:] if len(ru_name) > 2 else ru_name
                    
                    # Логика шансов выпадения
                    chance_badge = ""
                    chance_tooltip = ""
                    
                    if st.session_state.show_chances and "СТРАННЫЕ" not in cat["name"]:
                        marker = ru_name[0]  # Извлекаем маркер из названия (🔘, 🔵, 🟣, 🟡)
                        if marker in DROP_CHANCES[st.session_state.stage_idx]:
                            chance_val = DROP_CHANCES[st.session_state.stage_idx][marker]
                            chance_badge = f"<span style='color: #FFB000; background: rgba(255,176,0,0.15); padding: 1px 4px; border-radius: 4px; font-size: 0.65rem; margin-left: 4px;'>{chance_val}</span>"
                            chance_tooltip = f"<span style='color: #00E676; float: right; background: rgba(0,230,118,0.1); padding: 2px 6px; border-radius: 6px; font-size: 0.75rem;'>Drop: {chance_val}</span>"

                    img_url_main = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/{sid}.png"
                    img_url_master = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/{sid}.png"
                    
                    img_style = f"background-image: url('{img_url_main}'), url('{img_url_master}');"
                    
                    weight_icon_url = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/Texture_Icon_Weight.png"
                    weight_icon_master = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/Texture_Icon_Weight.png"
                    
                    effects_formatted = "".join([format_stat_with_icon(eff) for eff in effects.split(",")])
                    
                    tile_code = f'''<div class="art-tile {status_class}" data-copy="XCreateItemInInventoryByID {sid} 0 1 1">
                        <div class="tile-badge">{status_svg}</div>
                        <div class="tile-img-container">
                            <div class="tile-img" style="{img_style}"></div>
                        </div>
                        <div class="tile-label-container">
                            <div class="tile-label">{clean_name}{chance_badge}</div>
                        </div>
                        <div class="tooltip-box">
                            <div style="font-weight: 700; color: #FFB000; font-size: 0.82rem; margin-bottom: 6px; border-bottom: 1px solid rgba(255,176,0,0.25); padding-bottom: 3px; display: flex; justify-content: space-between; align-items: center;">
                                <span>{clean_name}</span> {chance_tooltip}
                            </div>
                            <div style="display: flex; align-items: center; gap: 6px; color: #CBD5E1; font-size: 0.75rem; margin-bottom: 6px;">
                                <img src="{weight_icon_url}" onerror="this.onerror=null; this.src='{weight_icon_master}';" style="width: 15px; height: 15px; object-fit: contain;" />
                                <span><b>Вес:</b> {weight}</span>
                            </div>
                            <div style="font-size: 0.74rem; line-height: 1.35; margin-bottom: 6px;">
                                {effects_formatted}
                            </div>
                            <div style="color: #64748B; font-size: 0.68rem; border-top: 1px solid #1E2638; padding-top: 4px; text-align: center;">
                                <span>Click to copy ID</span>
                            </div>
                        </div>
                    </div>'''
                    
                    grid_html += tile_code
                
                grid_html += '</div>\n'
                
                if hasattr(st, "html"):
                    st.html(grid_html)
                else:
                    st.markdown(f"<div>{grid_html.replace(chr(10), '')}</div>", unsafe_allow_html=True)

        # Текстовый файл с командами
        missing_base = [item for cat in CATEGORIES if "СТРАННЫЕ" not in cat["name"] for item in cat["items"] if item[0] not in found_sids]
        missing_weird = [item for cat in CATEGORIES if "СТРАННЫЕ" in cat["name"] for item in cat["items"] if item[0] not in found_sids]

        missing_total = len(missing_base) + len(missing_weird)

        txt_content = "=========================================================\n"
        txt_content += "      СПИСОК НЕДОСТАЮЩИХ АРТЕФАКТОВ S.T.A.L.K.E.R. 2\n"
        txt_content += f"      Недостает артефактов: {missing_total} из {base_total + weird_total}\n"
        txt_content += "=========================================================\n\n"

        for cat in CATEGORIES:
            missing_in_cat = [item for item in cat["items"] if item[0] not in found_sids]
            if missing_in_cat:
                txt_content += f"📋 {get_cat_name(cat['name'], lang)}:\n"
                for sid, ru_name, weight, effects in missing_in_cat:
                    txt_content += f"  • {ru_name} ({sid})\n    Вес: {weight} | Эффекты: {effects}\n"
                txt_content += "\n"

        txt_content += "=========================================================\n"
        txt_content += "КОМАНДЫ ДЛЯ СПАВНА НЕДОСТАЮЩИХ АРТЕФАКТОВ В ИНВЕНТАРЬ\n"
        txt_content += "=========================================================\n"
        txt_content += "Скопируйте нужный текст ниже (Ctrl+C), откройте консоль в игре и вставьте (Ctrl+V):\n\n"

        if not missing_base and not missing_weird:
            txt_content += "У вас собраны абсолютно все артефакты! Команды не требуются.\n"
        else:
            if missing_base:
                txt_content += "▶ Команда для базовых артефактов:\n"
                txt_content += "|".join([f"XCreateItemInInventoryByID {s[0]} 0 1 1" for s in missing_base]) + "\n\n"
            if missing_weird:
                txt_content += "▶ Команда для странных артефактов:\n"
                txt_content += "|".join([f"XCreateItemInInventoryByID {s[0]} 0 1 1" for s in missing_weird]) + "\n\n"

        st.markdown("<br/>", unsafe_allow_html=True)
        st.download_button(
            label=ui['dl_btn'],
            data=txt_content,
            file_name="Missing_Artifacts.txt",
            mime="text/plain"
        )

# =========================================================================
# МИНИМАЛИСТИЧНЫЙ ПОДВАЛ (FOOTER)
# =========================================================================
st.markdown("""
<div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #1E2638; text-align: center; display: flex; align-items: center; justify-content: center;">
    <a href="https://steamcommunity.com/sharedfiles/filedetails/?id=3743147617" target="_blank" rel="noopener noreferrer" class="steam-footer-link">
        <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/steam.png" 
             onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/steam.png';" 
             style="width: 20px; height: 20px; object-fit: contain;" />
        <span>Специально для руководства в Steam by Ethern</span>
    </a>
</div>
""", unsafe_allow_html=True)

# =========================================================================
# ИНЪЕКЦИЯ СКРИПТА ДЛЯ КОПИРОВАНИЯ КОМАНД И ПУТЕЙ В БУФЕР ОБМЕНА
# =========================================================================
components.html("""
<script>
try {
    const parentDoc = window.parent.document;
    parentDoc.addEventListener('click', function(e) {
        let copyPath = e.target.closest('.copy-path');
        let tile = e.target.closest('.art-tile');
        
        if(copyPath) {
            let pathText = copyPath.getAttribute('data-copy');
            if(pathText && parentDoc.hasFocus()) {
                parentDoc.defaultView.navigator.clipboard.writeText(pathText).then(() => {
                    let codeEl = copyPath.tagName === 'CODE' ? copyPath : copyPath.parentElement.querySelector('code');
                    if(codeEl) {
                        let orig = codeEl.innerText;
                        codeEl.innerText = "✅ Copied!";
                        setTimeout(() => { codeEl.innerText = orig; }, 1500);
                    }
                });
            }
        } else if(tile) {
            let cmd = tile.getAttribute('data-copy');
            if(cmd && parentDoc.hasFocus()) {
                parentDoc.defaultView.navigator.clipboard.writeText(cmd).then(() => {
                    // Ищем элемент с текстом внутри .tooltip-box
                    let tooltip = tile.querySelector('.tooltip-box div:last-child span');
                    if(tooltip) {
                        let originalText = tooltip.innerText;
                        tooltip.innerText = "✅ Copied!";
                        tooltip.style.color = "#00E676";
                        setTimeout(() => { 
                            tooltip.innerText = originalText;
                            tooltip.style.color = "#64748B";
                        }, 1200);
                    }
                }).catch(err => console.error("Clipboard err:", err));
            }
        }
    });
} catch(err) {
    console.log("Iframe cross-origin restriction for clipboard.");
}
</script>
""", height=0, width=0)
