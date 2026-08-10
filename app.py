import streamlit as st
import struct
import ctypes
import os
import re
import subprocess

st.set_page_config(
    page_title="S.T.A.L.K.E.R. 2 — Чекер Артефактов",
    page_icon="☢️",
    layout="centered"
)

# =========================================================================
# АВТО-КОМПИЛЯЦИЯ КРАКЕН-ДЕКОДЕРА ДЛЯ LINUX (STREAMLIT CLOUD)
# =========================================================================
@st.cache_resource
def get_linux_decompressor():
    so_path = os.path.abspath("libooz.so")
    if os.path.exists(so_path):
        return so_path

    try:
        # 1. Скачиваем открытый исходник ooz
        if not os.path.exists("ooz_src"):
            subprocess.run("git clone https://github.com/powzix/ooz.git ooz_src", shell=True, check=True)

        # 2. Создаем чистый Linux-заголовок stdafx.h (без Windows.h)
        clean_stdafx = """#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>

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
"""
        with open("ooz_src/stdafx.h", "w") as f:
            f.write(clean_stdafx)

        # 3. Модифицируем kraken.cpp для расслабленной проверки длины
        kraken_cpp = "ooz_src/kraken.cpp"
        with open(kraken_cpp, "r") as f:
            code = f.read()

        if "OozKraken_Decompress" not in code:
            code = code.replace("int main(", "int main_unused(")

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

        # 4. Компилируем .so библиотеку (ТОЛЬКО существующие файлы!)
        compile_cmd = "cd ooz_src && g++ -O3 -shared -fPIC -w -o ../libooz.so kraken.cpp bitknit.cpp lzna.cpp"
        subprocess.run(compile_cmd, shell=True, check=True)

        if os.path.exists(so_path):
            return so_path
    except Exception as e:
        st.error(f"Ошибка компиляции декомпрессора на сервере: {e}")
    return None

# =========================================================================
# БАЗА ДАННЫХ АРТЕФАКТОВ
# =========================================================================
CATEGORIES = [
    {
        "name": "1. 🌌 ГРАВИТАЦИОННЫЕ АРТЕФАКТЫ",
        "items": [
            ("GArtifactGoldFish", "🔘 Золотая рыбка"),
            ("GArtifactStoneDrop", "🔘 Каменное сердце"),
            ("GArtifactGravy", "🔘 Грави"),
            ("GArtifactWrenched", "🔘 Выверт"),
            ("GArtifactBloodStone", "🔘 Кровь камня"),
            ("GArtifactTrunk", "🔘 Канифоль"),
            ("GArtifactSponge", "🔘 Вихрь"),
            ("GArtifactPlane", "🔘 Галька"),
            ("GArtifactLandSlug", "🔘 Медуза"),
            ("GArtifactSpring", "🔵 Пружина"),
            ("GArtifactGraphiteBlock", "🔵 Корона"),
            ("GArtifactHedgehog", "🔵 Мухоловка"),
            ("GArtifactNightStar", "🟣 Ночная звезда"),
            ("GArtifactSplitStone", "🟣 Битый камень"),
            ("GArtifactBud", "🟣 Бутон"),
            ("GArtifactCompass", "🟡 Компас"),
            ("GArtifactRubiksCube", "🟡 Кубик-Рубик")
        ]
    },
    {
        "name": "2. 🔥 ТЕРМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("FArtifactFireBall", "🔘 Огненный шар"),
            ("FArtifactSteak", "🔘 Бифштекс"),
            ("FArtifactGlass", "🔘 Полость"),
            ("FArtifactBurntHunk", "🔘 Вертушка"),
            ("FArtifactResin", "🔘 Лира"),
            ("FArtifactDrops", "🔘 Капли"),
            ("FArtifactEye", "🔘 Глаз"),
            ("FArtifactCrystal", "🔘 Кристалл"),
            ("FArtifactMomsBeads", "🟣 Мамины Бусы"),
            ("FArtifactBakedBolts", "🔵 Брак"),
            ("FArtifactDeadSponge", "🔵 Мёртвая губка"),
            ("FArtifactHellishHedgehog", "🔵 Магма"),
            ("FArtifactPlasma", "🔵 Плазма"),
            ("FArtifactCandle", "🟣 Лепесток"),
            ("FArtifactFireworks", "🟣 Мясная зажигалка"),
            ("FArtifactCore", "🟣 Факел"),
            ("FArtifactRingOmnipotence", "🟡 Гиперкуб")
        ]
    },
    {
        "name": "3. ⚡ ЭЛЕКТРИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("EArtifactFlash", "🔘 Вспышка"),
            ("EArtifactSnowflake", "🔘 Снежинка"),
            ("EArtifactDummy", "🔘 Пустышка"),
            ("EArtifactBattery", "🔘 Батарейка"),
            ("EArtifactJellyFish", "🔘 Сапфир"),
            ("EArtifactWorm", "🔘 Крысиный король"),
            ("EArtifactSparkler", "🔘 Бенгальский огонь"),
            ("EArtifactChocolate", "🔘 Шоколадка"),
            ("EArtifactSoul", "🔵 Душа"),
            ("EArtifactMoonlight", "🔵 Лунный свет"),
            ("EArtifactTow", "🔵 Урок труда"),
            ("EArtifactThunderHedgehog", "🔵 Фонарь"),
            ("EArtifactCloud", "🔵 Арфа"),
            ("EArtifactAtom", "🟣 Блик"),
            ("EArtifactRazor", "🟣 Морская звезда"),
            ("EArtifactCrystalGlass", "🟣 Гребень"),
            ("EArtifactDope", "🟡 Грозовая ягода")
        ]
    },
    {
        "name": "4. 🧪 ХИМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("CArtifactCrystalThorn", "🔘 Кристальная колючка"),
            ("CArtifactThorn", "🔘 Колючка"),
            ("CArtifactChunkMeat", "🔘 Ломоть мяса"),
            ("CArtifactBubble", "🔵 Пузырь"),
            ("CArtifactSlug", "🔘 Слизняк"),
            ("CArtifactSlime", "🔘 Слизь"),
            ("CArtifactKryptonite", "🔘 Плесень"),
            ("CArtifactBung", "🔘 Рог"),
            ("CArtifactCottonWool", "🔘 Скорлупа"),
            ("CArtifactMica", "🔘 Слюда"),
            ("CArtifactBun", "🔵 Колобок"),
            ("CArtifactEchinus", "🔵 Морской еж"),
            ("CArtifactRosin", "🔵 Завтрак туриста"),
            ("CArtifactPlasticine", "🔵 Инфузория"),
            ("CArtifactPellicle", "🟣 Плёнка"),
            ("CArtifactBouncyBall", "🟣 Попрыгунчик"),
            ("CArtifactDevilsMushroom", "🟣 Чёртов гриб"),
            ("CArtifactLiquidStone", "🟡 Жидкий камень")
        ]
    },
    {
        "name": "5. 🌀 СТРАННЫЕ АРТЕФАКТЫ (Ачивка «Все страньше и страньше»)",
        "items": [
            ("AArtifactWeirdWater", "🌀 Странная вода"),
            ("AArtifactWeirdBall", "🌀 Странный мяч"),
            ("AArtifactWeirdNut", "🌀 Странная гайка"),
            ("AArtifactWeirdBolt", "🌀 Странный болт"),
            ("AArtifactWeirdKettle", "🌀 Странный котелок"),
            ("AArtifactWeirdFlower", "🌀 Странный цветок")
        ]
    }
]

# =========================================================================
# РАСПАКОВКА И ЧТЕНИЕ В ПАМЯТИ
# =========================================================================
def decompress_sav(bytes_data):
    if len(bytes_data) < 8:
        return None

    uncompressed_size = struct.unpack("<I", bytes_data[:4])[0]
    compressed_data = bytes_data[4:]

    # Собираем декомпрессор для Linux
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

    # Резервный поиск DLL если запускается локально на Windows
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
        for sid, _ in cat["items"]:
            if sid.encode("ascii") in raw_bytes or sid.encode("utf-16le") in raw_bytes:
                found.add(sid)
    return found

# =========================================================================
# ИНТЕРФЕЙС САЙТА
# =========================================================================
st.title("☢️ S.T.A.L.K.E.R. 2 — Чекер Артефактов")
st.markdown("Узнайте свой прогресс достижений **«Собиратель чудес»** (69 артов) и **«Все страньше и страньше»** без установки программ!")

st.info("💡 Загрузите ваш файл **CampaignsSave.sav** (обычно лежит по пути: `AppData/Local/Stalker2/Saved/STEAM/SaveGames/`)")

uploaded_file = st.file_uploader("Перетащите сюда файл сохранения (.sav)", type=["sav"])

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
            for sid, _ in cat["items"]:
                if sid in found_sids:
                    if is_weird: weird_found += 1
                    else: base_found += 1

        st.markdown("---")
        st.subheader("🏆 Прогресс по достижениям:")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="«Собиратель чудес» (69 артов)", value=f"{base_found} / {base_total}", delta=f"{int(base_found/base_total*100)}%")
            st.progress(base_found / base_total)
        with col2:
            st.metric(label="«Все страньше и страньше» (6 артов)", value=f"{weird_found} / {weird_total}", delta=f"{int(weird_found/weird_total*100)}%")
            st.progress(weird_found / weird_total)

        st.markdown("---")
        st.subheader("📋 Подробный чек-лист по категориям:")

        for cat in CATEGORIES:
            with st.expander(cat["name"], expanded=True):
                for sid, ru_name in cat["items"]:
                    if sid in found_sids:
                        st.markdown(f"✅ **{ru_name}** (`{sid}`)")
                    else:
                        st.markdown(f"❌ <span style='color:gray;'>{ru_name} (`{sid}`)</span>", unsafe_allow_bytes=True)

        missing_base = [sid for cat in CATEGORIES if "СТРАННЫЕ" not in cat["name"] for sid, _ in cat["items"] if sid not in found_sids]
        missing_weird = [sid for cat in CATEGORIES if "СТРАННЫЕ" in cat["name"] for sid, _ in cat["items"] if sid not in found_sids]

        txt_content = "=== НЕДОСТАЮЩИЕ АРТЕФАКТЫ ===\n\n"
        if missing_base:
            txt_content += "▶ Команда для базовых артефактов («Собиратель чудес»):\n"
            txt_content += "|".join([f"XCreateItemInInventoryByID {s} 0 1 1" for s in missing_base]) + "\n\n"
        if missing_weird:
            txt_content += "▶ Команда для странных артефактов («Все страньше и страньше»):\n"
            txt_content += "|".join([f"XCreateItemInInventoryByID {s} 0 1 1" for s in missing_weird]) + "\n\n"

        st.download_button(
            label="📥 Скачать команды спавна недостающих артефактов (Missing_Artifacts.txt)",
            data=txt_content,
            file_name="Missing_Artifacts.txt",
            mime="text/plain"
        )
