import streamlit as st
import streamlit.components.v1 as components
import json

# =========================================================================
# ИКОНКИ И ССЫЛКИ GITHUB
# =========================================================================
GITHUB_RAW = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main"
GITHUB_FALLBACK = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master"

# 1. Иконка для шапки прогресс-бара (в папке icons/)
HEADER_ICON_MAIN = f"{GITHUB_RAW}/icons/blue.png"
HEADER_ICON_FALLBACK = f"{GITHUB_FALLBACK}/icons/blue.png"

# 2. Стандартная иконка-заглушка для карточек (в папке icons/blueprint/)
DEF_CARD_ICON_MAIN = f"{GITHUB_RAW}/icons/blueprint/icon_def_blue.png"
DEF_CARD_ICON_FALLBACK = f"{GITHUB_FALLBACK}/icons/blueprint/icon_def_blue.png"

def get_bp_icon_url(bp_id):
    return f"{GITHUB_RAW}/icons/blueprint/icon_{bp_id}.png"

def get_map_url(bp_id):
    return f"{GITHUB_RAW}/icons/blueprint/map_{bp_id}.png"

def get_scr_url(bp_id, index=1):
    if index == 1:
        return f"{GITHUB_RAW}/icons/blueprint/scr_{bp_id}.png"
    return f"{GITHUB_RAW}/icons/blueprint/scr_{bp_id}_{index}.png"

# =========================================================================
# БАЗА ДАННЫХ ЧЕРТЕЖЕЙ (77 ШТ.)
# =========================================================================
BLUEPRINTS_DATA = [
  # -------------------- ОРУЖИЕ (27 шт.) --------------------
  {"id": "Blueprint_M10_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "M10 Gordon", "EN_Short": "M10 Gordon", "UA_Short": "M10 Gordon", "RU_Full": "M10 Gordon: Прорезиненный слой", "EN_Full": "M10 Gordon: Rubber Layer", "UA_Full": "M10 Gordon: Гумовий шар", "RU_Desc": "Частично гасит отдачу.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Rhino_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "Rhino", "EN_Short": "Rhino", "UA_Short": "Rhino", "RU_Full": "Rhino: Переделка под дробь", "EN_Full": "Rhino: Buckshot Conversion", "UA_Full": "Rhino: Перероблення під дріб", "RU_Desc": "Связана с рассверливанием ствола и подгонкой деталей под новый тип боеприпаса.", "EN_Desc": "Boring out the barrel and adjusting parts to accommodate new ammunition.", "UA_Desc": "Розсвердлювання ствола та припасування деталей під новий тип боєприпасу.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_APB_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "АПБС", "EN_Short": "APSB", "UA_Short": "АПБС", "RU_Full": "АПБС: Установка балансира", "EN_Full": "APSB: Counterweight", "UA_Full": "АПБС: Встановлення балансира", "RU_Desc": "Балансир увеличивает стабильность оружия, уменьшая разброс при стрельбе.", "EN_Desc": "Enhances stability, reducing spread when firing.", "UA_Desc": "Збільшує стабільність зброї, що зменшує розкид під час стрільби.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_APB_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "АПБС", "EN_Short": "APSB", "UA_Short": "АПБС", "RU_Full": "АПБС: Индивидуальная подгонка", "EN_Full": "APSB: Individual Adjustment", "UA_Full": "АПБС: Індивідуальне припасування", "RU_Desc": "Моделирование рукоятки под стрелка повышает удобство обращения.", "EN_Desc": "Customizing the grip to match shooter's hand.", "UA_Desc": "Моделювання руків'я під стрільця підвищує зручність.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Integral_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "Integral-A", "EN_Short": "Integral-A", "UA_Short": "Integral-A", "RU_Full": "Integral-A: Уплотнитель муфты возвратного механизма", "EN_Full": "Integral-A: Return Mechanism Sleeve Tightener", "UA_Full": "Integral-A: Ущільнювач муфти зворотного механізму", "RU_Desc": "Увеличивает давление в стволе, повышая начальную скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, що підвищує початкову швидкість кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Zubr_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "«Зубр-19»", "EN_Short": "Zubr-19", "UA_Short": "«Зубр-19»", "RU_Full": "«Зубр-19»: Дополнительный нарез в стволе", "EN_Full": "Zubr-19: Extra Barrel Rifling", "UA_Full": "«Зубр-19»: Додатковий наріз у стволі", "RU_Desc": "Снижает разрушение пули в стволе, сохраняя её характеристики.", "EN_Desc": "Reduces bullet deterioration within the barrel.", "UA_Desc": "Зменшує руйнування кулі в стволі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Zubr_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "«Зубр-19»", "EN_Short": "Zubr-19", "UA_Short": "«Зубр-19»", "RU_Full": "«Зубр-19»: Анатомическая подгонка", "EN_Full": "Zubr-19: Anatomical Adjustment", "UA_Full": "«Зубр-19»: Анатомічне припасування", "RU_Desc": "Более удобная форма цевья повышает ускорение прицеливания.", "EN_Desc": "A more comfortable handguard shape contributes to increased aiming speed.", "UA_Desc": "Зручніша форма цівки прискорює прицілювання.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Gvintar_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "СВ «Винтарь»", "EN_Short": "VS Vintar", "UA_Short": "СГ «Гвинтар»", "RU_Full": "СВ «Винтарь»: Уплотнитель муфты возвратного механизма", "EN_Full": "VS Vintar: Return Mechanism Sleeve Tightener", "UA_Full": "СГ «Гвинтар»: Ущільнювач муфти зворотного механізму", "RU_Desc": "Увеличивает давление в стволе, повышая скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, що підвищує швидкість кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Gvintar_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "СВ «Винтарь»", "EN_Short": "VS Vintar", "UA_Short": "СГ «Гвинтар»", "RU_Full": "СВ «Винтарь»: Подгонка боевых упоров затвора", "EN_Full": "VS Vintar: Adjusted Bolt Locking Lugs", "UA_Full": "СГ «Гвинтар»: Припасування бойових упорів затвора", "RU_Desc": "Уменьшает утечку пороховых газов, увеличивая скорость пули.", "EN_Desc": "Reducing powder gas leakage leads to increased muzzle velocity.", "UA_Desc": "Зменшує витік порохових газів, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Grim_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "«Гром С-14»", "EN_Short": "Grom S-14", "UA_Short": "«Грім» С-14", "RU_Full": "«Гром С-14»: Каучуковый тыльник приклада", "EN_Full": "Grom S-14: Rubber Stock Rear", "UA_Full": "«Грім» С-14: Каучуковий тильник приклада", "RU_Desc": "Делает отдачу от выстрела значительно мягче.", "EN_Desc": "Effectively dampens recoil, providing a smoother shooting experience.", "UA_Desc": "Робить віддачу пострілу значно м'якшою.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Lavina_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "СА «Лавина»", "EN_Short": "AS Lavina", "UA_Short": "СА «Лавина»", "RU_Full": "СА «Лавина»: Подгонка боевых упоров затвора", "EN_Full": "AS Lavina: Adjusted Bolt Locking Lugs", "UA_Full": "СА «Лавина»: Припасування бойових упорів затвора", "RU_Desc": "Уменьшает утечку пороховых газов, увеличивая скорость пули.", "EN_Desc": "Reducing powder gas leakage leads to increased muzzle velocity.", "UA_Desc": "Зменшує витік порохових газів, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Lavina_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "СА «Лавина»", "EN_Short": "AS Lavina", "UA_Short": "СА «Лавина»", "RU_Full": "СА «Лавина»: Прорезиненный слой", "EN_Full": "AS Lavina: Rubber Layer", "UA_Full": "СА «Лавина»: Гумовий шар", "RU_Desc": "Частично гасит отдачу.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Kharod_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "Kharod", "EN_Short": "Kharod", "UA_Short": "Kharod", "RU_Full": "Kharod: Установка балансира", "EN_Full": "Kharod: Counterweight", "UA_Full": "Kharod: Встановлення балансира", "RU_Desc": "Балансир увеличивает стабильность оружия, снижая разброс.", "EN_Desc": "Counterweight enhances stability, reducing spread.", "UA_Desc": "Балансир збільшує стабільність зброї, зменшуючи розкид.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Kharod_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "Kharod", "EN_Short": "Kharod", "UA_Short": "Kharod", "RU_Full": "Kharod: Прорезиненное покрытие", "EN_Full": "Kharod: Rubber Coating", "UA_Full": "Kharod: Гумове покриття", "RU_Desc": "Прорезиненная поверхность амортизирует отдачу и укрепляет хват.", "EN_Desc": "Rubberized surface dampens recoil and enhances grip.", "UA_Desc": "Гумова поверхня амортизує віддачу та зміцнює хват.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Dnipro_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "«Днипро»", "EN_Short": "Dnipro", "UA_Short": "«Дніпро»", "RU_Full": "«Днипро»: Дополнительный нарез в стволе", "EN_Full": "Dnipro: Extra Barrel Rifling", "UA_Full": "«Дніпро»: Додатковий наріз у стволі", "RU_Desc": "Снижает разрушение пули в стволе.", "EN_Desc": "Reduces bullet deterioration within the barrel.", "UA_Desc": "Зменшує руйнування кулі в стволі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Dnipro_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "«Днипро»", "EN_Short": "Dnipro", "UA_Short": "«Дніпро»", "RU_Full": "«Днипро»: Переделка под калибр 7.62", "EN_Full": "Dnipro: Caliber Conversion 7.62", "UA_Full": "«Дніпро»: Перероблення під калібр 7.62", "RU_Desc": "Замена ствола под новый мощный калибр 7.62.", "EN_Desc": "Replaces the barrel to accommodate the 7.62 caliber.", "UA_Desc": "Заміна ствола під новий калібр 7.62.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_M701_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "M701 Super", "EN_Short": "M701 Super", "UA_Short": "M701 Super", "RU_Full": "M701 Super: Уплотнитель муфты возвратного механизма", "EN_Full": "M701 Super: Return Mechanism Sleeve Tightener", "UA_Full": "M701 Super: Ущільнювач муфти зворотного механізму", "RU_Desc": "Увеличивает давление в стволе, повышая скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_M701_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "M701 Super", "EN_Short": "M701 Super", "UA_Short": "M701 Super", "RU_Full": "M701 Super: Полимерная рукоятка", "EN_Full": "M701 Super: Polymer Handle", "UA_Full": "M701 Super: Полімерне руків'я", "RU_Desc": "Применение полимеров значительно снижает вес оружия.", "EN_Desc": "Polymers reduce overall weapon weight.", "UA_Desc": "Полімери значно знижують вагу зброї.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SVU_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "СВУ-МК С-3", "EN_Short": "SVU-MK S-3", "UA_Short": "СВУ-МК С-3", "RU_Full": "СВУ-МК С-3: Индивидуальная подгонка", "EN_Full": "SVU-MK S-3: Individual Adjustment", "UA_Full": "СВУ-МК С-3: Індивідуальне припасування", "RU_Desc": "Моделирование рукоятки под стрелка максимально повышает удобство.", "EN_Desc": "Customizing grip to match shooter's hand.", "UA_Desc": "Моделювання руків'я під стрільця підвищує зручність.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SVU_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "СВУ-МК С-3", "EN_Short": "SVU-MK S-3", "UA_Short": "СВУ-МК С-3", "RU_Full": "СВУ-МК С-3: Прорезиненный слой", "EN_Full": "SVU-MK S-3: Rubber Layer", "UA_Full": "СВУ-МК С-3: Гумовий шар", "RU_Desc": "Частично гасит отдачу при стрельбе.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу під час стрільби.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_M860_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "M860 Cracker", "EN_Short": "M860 Cracker", "UA_Short": "M860 Cracker", "RU_Full": "M860 Cracker: Магазинное питание", "EN_Full": "M860 Cracker: Magazine Feed", "UA_Full": "M860 Cracker: Магазинна подача", "RU_Desc": "Позволяет значительно быстрее перезаряжать дробовик.", "EN_Desc": "Allows for markedly faster reloading.", "UA_Desc": "Дає змогу значно швидше перезаряджати зброю.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_D12_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "«Сайга Д-12»", "EN_Short": "Saiga D-12", "UA_Short": "«Сайга» Д-12", "RU_Full": "«Сайга Д-12»: Чок", "EN_Full": "Saiga D-12: Choke", "UA_Full": "«Сайга» Д-12: Чок", "RU_Desc": "Насадка на ствол. Уменьшает разлёт дроби.", "EN_Desc": "A barrel attachment designed to reduce spread.", "UA_Desc": "Насадка на ствол. Зменшує розкид дробу.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_D12_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "«Сайга Д-12»", "EN_Short": "Saiga D-12", "UA_Short": "«Сайга» Д-12", "RU_Full": "«Сайга Д-12»: Ребаланс приклада", "EN_Full": "Saiga D-12: Rebalanced Stock", "UA_Full": "«Сайга» Д-12: Ребаланс приклада", "RU_Desc": "Центр тяжести смещён вперёд для более быстрого прицеливания.", "EN_Desc": "Center of gravity shifted forward to facilitate quicker aiming.", "UA_Desc": "Центр ваги зміщений уперед для швидшого прицілювання.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Ram2_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "Ram-2", "EN_Short": "Ram-2", "UA_Short": "Ram-2", "RU_Full": "Ram-2: Уплотнитель муфты возвратного механизма", "EN_Full": "Ram-2: Return Mechanism Sleeve Tightener", "UA_Full": "Ram-2: Ущільнювач муфти зворотного механізму", "RU_Desc": "Увеличивает давление в стволе, повышая скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Ram2_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "Ram-2", "EN_Short": "Ram-2", "UA_Short": "Ram-2", "RU_Full": "Ram-2: Автоматический двухпозиционный газовый регулятор", "EN_Full": "Ram-2: Automatic Two-Stage Gas Regulator", "UA_Full": "Ram-2: Автоматичний двопозиційний газовий регулятор", "RU_Desc": "Механизм для значительного уменьшения загрязнённости оружия.", "EN_Desc": "A mechanism that reduces weapon fouling.", "UA_Desc": "Механізм для зменшення забруднення зброї.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_MG_Upgrade_1", "type": "weapon", "scr_count": 1, "RU_Short": "РПМ-74", "EN_Short": "RPM-74", "UA_Short": "РКМ-74", "RU_Full": "РПМ-74: Прорезиненное покрытие", "EN_Full": "RPM-74: Rubber Coating", "UA_Full": "РКМ-74: Гумове покриття", "RU_Desc": "Цепкая прорезиненная поверхность амортизирует отдачу пулемета.", "EN_Desc": "Rubberized surface dampens recoil and enhances grip.", "UA_Desc": "Гумова поверхня амортизує віддачу та зміцнює хват.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_MG_Upgrade_2", "type": "weapon", "scr_count": 1, "RU_Short": "РПМ-74", "EN_Short": "RPM-74", "UA_Short": "РКМ-74", "RU_Full": "РПМ-74: Каучуковый тыльник приклада", "EN_Full": "RPM-74: Rubber Stock Rear", "UA_Full": "РКМ-74: Каучуковий тильник приклада", "RU_Desc": "Делает отдачу от выстрела значительно мягче.", "EN_Desc": "Effectively dampens recoil, providing a smoother shooting experience.", "UA_Desc": "Робить віддачу пострілу значно м'якшою.", "teleport_cmd": "XTeleportTo 0 0 0"},

  # -------------------- БРОНЯ И ШЛЕМЫ (50 шт.) --------------------
  {"id": "Blueprint_Heavy2_Military_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Берилл-5М»", "EN_Short": "Berill-5M", "UA_Short": "«Берил-5М»", "RU_Full": "Бронекостюм «Берилл-5М»: Питьевая система «Верблюд»", "EN_Full": "Berill-5M: Camel Hydration System", "UA_Full": "Бронекостюм «Берил-5М»: Система «Верблюд»", "RU_Desc": "Быстро восстановит водный баланс при длительных нагрузках.", "EN_Desc": "Ensures quick hydration during prolonged exertion.", "UA_Desc": "Швидко відновить водний баланс.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy2_Military_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«Берилл-5М»", "EN_Short": "Berill-5M", "UA_Short": "«Берил-5М»", "RU_Full": "Бронекостюм «Берилл-5М»: Свинцовый контейнер", "EN_Full": "Berill-5M: Lead Container", "UA_Full": "Бронекостюм «Берил-5М»: Свинцевий контейнер", "RU_Desc": "Способ уберечь себя от радиационного излучения артефактов.", "EN_Desc": "Protected from the radiation emitted by artifacts.", "UA_Desc": "Захист від радіаційного випромінювання артефактів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyAnomaly_Scientific_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "ССП-100", "EN_Short": "SSP-100", "UA_Short": "ССП-100", "RU_Full": "ССП-100 «Открытие»: Свинцовый контейнер", "EN_Full": "SSP-100: Lead Container", "UA_Full": "ССП-100 «Відкриття»: Свинцевий контейнер", "RU_Desc": "Защита от радиационного излучения артефактов.", "EN_Desc": "Protected from artifact radiation.", "UA_Desc": "Захист від радіації артефактів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyAnomaly_Scientific_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "ССП-100", "EN_Short": "SSP-100", "UA_Short": "ССП-100", "RU_Full": "ССП-100 «Открытие»: Арамидная подкладка", "EN_Full": "SSP-100: Aramid Lining", "UA_Full": "ССП-100 «Відкриття»: Арамідна підкладка", "RU_Desc": "Распределяет импульс от удара, останавливает осколки и пули.", "EN_Desc": "Disperses impact force, stopping shrapnel and bullets.", "UA_Desc": "Розподіляє імпульс від удару, зупиняє осколки та кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "ПСЗ-12В «Булат»", "EN_Short": "PSZ-12V Bulat", "UA_Short": "ПСЗ-12В «Булат»", "RU_Full": "ПСЗ-12В «Булат»: Свинцовый контейнер", "EN_Full": "PSZ-12V Bulat: Lead Container", "UA_Full": "ПСЗ-12В «Булат»: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек под артефакты.", "EN_Desc": "Lead container for artifacts.", "UA_Desc": "Свинцевий відсік під артефакти.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "ПСЗ-12В «Булат»", "EN_Short": "PSZ-12V Bulat", "UA_Short": "ПСЗ-12В «Булат»", "RU_Full": "ПСЗ-12В «Булат»: Питьевая система «Верблюд»", "EN_Full": "PSZ-12V Bulat: Camel Hydration System", "UA_Full": "ПСЗ-12В «Булат»: Система «Верблюд»", "RU_Desc": "Гидратор в рюкзак для выносливости.", "EN_Desc": "Hydrator in backpack for stamina.", "UA_Desc": "Гідратор у рюкзак для витривалості.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Броня Долга»", "EN_Short": "Duty Armor", "UA_Short": "«Броня Долгу»", "RU_Full": "ПСЗ-9Д «Броня \"Долга\"»: Питьевая система «Верблюд»", "EN_Full": "PSZ-9D Duty Armor: Camel Hydration", "UA_Full": "ПСЗ-9Д «Броня \"Долгу\"»: Система «Верблюд»", "RU_Desc": "Гидратор быстро восстановит водный баланс.", "EN_Desc": "Quick hydration during long raids.", "UA_Desc": "Швидке відновлення сил у ході вилазок.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«Броня Долга»", "EN_Short": "Duty Armor", "UA_Short": "«Броня Долгу»", "RU_Full": "ПСЗ-9Д «Броня \"Долга\"»: Арамидная подкладка", "EN_Full": "PSZ-9D Duty Armor: Aramid Lining", "UA_Full": "ПСЗ-9Д «Броня \"Долгу\"»: Арамідна підкладка", "RU_Desc": "Арамидная подкладка распределяет импульс от удара.", "EN_Desc": "Aramid lining disperses impact force.", "UA_Desc": "Арамідна підкладка зупиняє осколки.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyBattle_Spark_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "ПСЗ-9И «Сокол»", "EN_Short": "PSZ-9I Falcon", "UA_Short": "ПСЗ-9І «Сокіл»", "RU_Full": "ПСЗ-9И «Сокол»: Плексигласовый комбинезон со свинцовой сеткой", "EN_Full": "PSZ-9I Falcon: Plexiglas Suit with Lead Mesh", "UA_Full": "ПСЗ-9І «Сокіл»: Плексигласовий комбінезон", "RU_Desc": "Защищает от излучения и вредных веществ без потери подвижности.", "EN_Desc": "Protects against radiation without impeding mobility.", "UA_Desc": "Захищає від радіації та не сковує рухів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyBattle_Spark_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "ПСЗ-9И «Сокол»", "EN_Short": "PSZ-9I Falcon", "UA_Short": "ПСЗ-9І «Сокіл»", "RU_Full": "ПСЗ-9И «Сокол»: Свинцовый контейнер", "EN_Full": "PSZ-9I Falcon: Lead Container", "UA_Full": "ПСЗ-9І «Сокіл»: Свинцевий контейнер", "RU_Desc": "Защита от излучения артефактов.", "EN_Desc": "Lead container for radiation resistance.", "UA_Desc": "Захист від випромінювання артефактів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Neutral_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА»", "EN_Short": "SEVA Suit", "UA_Short": "«СЕВА»", "RU_Full": "Комбинезон «СЕВА»: Кольчужные вставки", "EN_Full": "SEVA Suit: Chainmail Inserts", "UA_Full": "Комбінезон «СЕВА»: Кольчужні вставки", "RU_Desc": "Кольчужное плетение спасает от ножевых и осколочных попаданий.", "EN_Desc": "Reinforced chainmail protective inserts.", "UA_Desc": "Кольчужні вставки рятують від порізів та осколків.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Neutral_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА»", "EN_Short": "SEVA Suit", "UA_Short": "«СЕВА»", "RU_Full": "Комбинезон «СЕВА»: Экранирующее покрытие", "EN_Full": "SEVA Suit: Protective Coating", "UA_Full": "Комбінезон «СЕВА»: Екранувальне покриття", "RU_Desc": "Работает по принципу клетки Фарадея.", "EN_Desc": "Operates akin to a Faraday cage.", "UA_Desc": "Працює за принципом клітки Фарадея.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА-В»", "EN_Short": "SEVA-V", "UA_Short": "«СЕВА-В»", "RU_Full": "Комбинезон «СЕВА-В»: Экранирующее покрытие", "EN_Full": "SEVA-V Suit: Protective Coating", "UA_Full": "Комбінезон «СЕВА-В»: Екранувальне покриття", "RU_Desc": "Защитное экранирование от аномальных полей.", "EN_Desc": "Anomalous discharge shielding.", "UA_Desc": "Екранування від аномальних розрядів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА-В»", "EN_Short": "SEVA-V", "UA_Short": "«СЕВА-В»", "RU_Full": "Комбинезон «СЕВА-В»: Арамидная подкладка", "EN_Full": "SEVA-V Suit: Aramid Lining", "UA_Full": "Комбінезон «СЕВА-В»: Арамідна подкладка", "RU_Desc": "Повышает пулестойкость комбинезона.", "EN_Desc": "Increased ballistic resistance.", "UA_Desc": "Підвищує кульовий захист костюма.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Spark_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА-И»", "EN_Short": "SEVA-I", "UA_Short": "«СЕВА-І»", "RU_Full": "Комбинезон «СЕВА-И»: Накладные карманы", "EN_Full": "SEVA-I Suit: Sewn-on Pockets", "UA_Full": "Комбінезон «СЕВА-І»: Накладні кишені", "RU_Desc": "Дополнительные карманы на рукавах и штанах.", "EN_Desc": "Extra pockets on pants and sleeves.", "UA_Desc": "Додаткові кишені для спорядження.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Spark_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА-И»", "EN_Short": "SEVA-I", "UA_Short": "«СЕВА-І»", "RU_Full": "Комбинезон «СЕВА-И»: Свинцовый контейнер", "EN_Full": "SEVA-I Suit: Lead Container", "UA_Full": "Комбінезон «СЕВА-І»: Свинцевий контейнер", "RU_Desc": "Защита от радиационного фона артефактов.", "EN_Desc": "Protects against artifact radiation.", "UA_Desc": "Захист від випромінювання артефактів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА-Д»", "EN_Short": "SEVA-D", "UA_Short": "«СЕВА-Д»", "RU_Full": "Комбинезон «СЕВА-Д»: Питьевая система «Верблюд»", "EN_Full": "SEVA-D Suit: Camel Hydration", "UA_Full": "Комбінезон «СЕВА-Д»: Система «Верблюд»", "RU_Desc": "Встроенный в рюкзак гидратор.", "EN_Desc": "Integrated hydration system.", "UA_Desc": "Вбудований у рюкзак гідратор.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_SEVA_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«СЕВА-Д»", "EN_Short": "SEVA-D", "UA_Short": "«СЕВА-Д»", "RU_Full": "Комбинезон «СЕВА-Д»: Арамидная подкладка", "EN_Full": "SEVA-D Suit: Aramid Lining", "UA_Full": "Комбінезон «СЕВА-Д»: Арамідна подкладка", "RU_Desc": "Арамидный баллистический слой.", "EN_Desc": "Aramid ballistic layer.", "UA_Desc": "Арамідний шар від куль.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»", "RU_Full": "Экзоскелет «Оператор»: Цельнотитановые составляющие", "EN_Full": "Operator: All-Titanium Components", "UA_Full": "Екзоскелет «Оператор»: Суцільнотитанові складники", "RU_Desc": "Сверхпрочный титановый экзокаркас.", "EN_Desc": "Titanium exoskeleton structure.", "UA_Desc": "Надміцний титановий каркас.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»", "RU_Full": "Экзоскелет «Оператор»: Сервомоторы рук", "EN_Full": "Operator: Arm Servos", "UA_Full": "Екзоскелет «Оператор»: Сервомотори рук", "RU_Desc": "Стабилизируют удержание оружия в руках.", "EN_Desc": "Counteract inertia and stabilize weapon handling.", "UA_Desc": "Стабілізують положення зброї в руках.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_3", "type": "armor", "scr_count": 1, "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»", "RU_Full": "Экзоскелет «Оператор»: Свинцовый контейнер", "EN_Full": "Operator: Lead Container", "UA_Full": "Екзоскелет «Оператор»: Свинцевий контейнер", "RU_Desc": "Защита от излучения артефактов.", "EN_Desc": "Artifact radiation container.", "UA_Desc": "Захист від радіації артефактів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_4", "type": "armor", "scr_count": 1, "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»", "RU_Full": "Экзоскелет «Оператор»: Доп. свинцовый контейнер", "EN_Full": "Operator: Lead Container #2", "UA_Full": "Екзоскелет «Оператор»: Дод. свинцевий контейнер", "RU_Desc": "Второй свинцовый контейнер.", "EN_Desc": "Second lead container.", "UA_Desc": "Другий свинцевий контейнер.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Цельнотитановые составляющие", "EN_Full": "Brummbar: All-Titanium Components", "UA_Full": "Екзоскелет «Брумбар»: Суцільнотитанові складники", "RU_Desc": "Титановые элементы каркаса наемников.", "EN_Desc": "Titanium exoskeleton construction.", "UA_Desc": "Титанові елементи каркаса наємників.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Система выведения ядовитых веществ", "EN_Full": "Brummbar: Poison Expulsion System", "UA_Full": "Екзоскелет «Брумбар»: Система виведення отрути", "RU_Desc": "Пневматическая очистка полостей респиратора.", "EN_Desc": "Pneumatic expulsion system for hazardous substances.", "UA_Desc": "Пневматичне очищення респіратора.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_3", "type": "armor", "scr_count": 1, "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Оснащение сервоприводов гидравлическими усилителям", "EN_Full": "Brummbar: Hydraulic Servos (Sprint)", "UA_Full": "Екзоскелет «Брумбар»: Гідравлічні підсилювачі", "RU_Desc": "Позволяет переходить на бег в тяжелом экзоскелете.", "EN_Desc": "Hydraulic amplifiers that enable running.", "UA_Desc": "Гідравлічні підсилювачі для швидкого бігу.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_4", "type": "armor", "scr_count": 1, "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Экранирующее покрытие", "EN_Full": "Brummbar: Protective Coating", "UA_Full": "Екзоскелет «Брумбар»: Екранувальне покриття", "RU_Desc": "Защитное экранирование сервоприводов.", "EN_Desc": "Protective shielding layer.", "UA_Desc": "Екранувальне покриття.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Система выведения ядовитых веществ", "EN_Full": "Exoskeleton: Poison Expulsion", "UA_Full": "Екзоскелет: Система виведення отрути", "RU_Desc": "Очистка респиратора от токсичных газов.", "EN_Desc": "Hazardous substance removal.", "UA_Desc": "Виведення небезпечних речовин.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Экранирующее покрытие", "EN_Full": "Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет: Екранувальне покриття", "RU_Desc": "Экранирующий защитный слой.", "EN_Desc": "Faraday cage shielding.", "UA_Desc": "Екранувальне покриття.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_3", "type": "armor", "scr_count": 1, "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Свинцовый контейнер", "EN_Full": "Exoskeleton: Lead Container", "UA_Full": "Екзоскелет: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек для артефакта.", "EN_Desc": "Lead container for artifacts.", "UA_Desc": "Свинцевий контейнер для артефакту.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_4", "type": "armor", "scr_count": 1, "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Дополнительный свинцовый контейнер", "EN_Full": "Exoskeleton: Lead Container #2", "UA_Full": "Екзоскелет: Дод. свинцевий контейнер", "RU_Desc": "Второй контейнер под артефакт.", "EN_Desc": "Second lead container.", "UA_Desc": "Другий свинцевий контейнер.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Цельнотитановые составляющие", "EN_Full": "Liberty Exoskeleton: Titanium Components", "UA_Full": "Екзоскелет «Воля»: Суцільнотитанові складники", "RU_Desc": "Легкий и прочный титановый каркас.", "EN_Desc": "Titanium exoskeleton construction.", "UA_Desc": "Титанові деталі конструкції.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Система выведения ядовитых веществ", "EN_Full": "Liberty Exoskeleton: Poison Expulsion", "UA_Full": "Екзоскелет «Воля»: Система виведення отрути", "RU_Desc": "Пневматическая очистка респиратора.", "EN_Desc": "Respirator gas purge system.", "UA_Desc": "Очищення порожнин респіратора.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_3", "type": "armor", "scr_count": 1, "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Экранирующее покрытие", "EN_Full": "Liberty Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет «Воля»: Екранувальне покриття", "RU_Desc": "Экранирующее защитное покрытие.", "EN_Desc": "Protective coating.", "UA_Desc": "Екранувальне покриття.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_4", "type": "armor", "scr_count": 1, "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Доп. экранирующее покрытие", "EN_Full": "Liberty Exoskeleton: Extra Coating", "UA_Full": "Екзоскелет «Воля»: Дод. екранувальне покриття", "RU_Desc": "Второй слой экранирования.", "EN_Desc": "Second layer of protective coating.", "UA_Desc": "Другий шар екранування.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»", "RU_Full": "Экзокостюм «Оплот»: Накладные карманы", "EN_Full": "Bulwark: Sewn-on Pockets", "UA_Full": "Екзокостюм «Оплот»: Накладні кишені", "RU_Desc": "Карманы на штанах и рукавах.", "EN_Desc": "Extra pockets on pants and sleeves.", "UA_Desc": "Додаткові кишені на рукавах.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»", "RU_Full": "Экзокостюм «Оплот»: Полиэтиленовая герметичная подкладка", "EN_Full": "Bulwark: Airtight Polyethylene Lining", "UA_Full": "Екзокостюм «Оплот»: Герметична підкладка", "RU_Desc": "Защита от ядовитых веществ и электрического тока.", "EN_Desc": "Airtight chemical and shock protection.", "UA_Desc": "Захист від токсинів та розрядів струму.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_3", "type": "armor", "scr_count": 1, "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»", "RU_Full": "Экзокостюм «Оплот»: Активные фильтры", "EN_Full": "Bulwark: Active Filters", "UA_Full": "Екзокостюм «Оплот»: Активні фільтри", "RU_Desc": "Активные фильтры нейтрализуют радионуклиды.", "EN_Desc": "Active filters neutralize radionuclides.", "UA_Desc": "Активні фільтри нейтралізують радіонукліди.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_4", "type": "armor", "scr_count": 1, "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»", "RU_Full": "Экзокостюм «Оплот»: Свинцовый контейнер", "EN_Full": "Bulwark: Lead Container", "UA_Full": "Екзокостюм «Оплот»: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек для артефакта.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Цельнотитановые составляющие", "EN_Full": "Cuirass: All-Titanium Components", "UA_Full": "Екзоскелет «Панцир»: Суцільнотитанові складники", "RU_Desc": "Усиленный титановый корпус Долга.", "EN_Desc": "Duty reinforced heavy titanium armor.", "UA_Desc": "Посилений титановий корпус Долгу.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Система выведения ядовитых веществ", "EN_Full": "Cuirass: Poison Expulsion System", "UA_Full": "Екзоскелет «Панцир»: Система виведення отрути", "RU_Desc": "Пневмосистема продувки респиратора.", "EN_Desc": "Hazardous gas expulsion.", "UA_Desc": "Очищення респіратора від газів.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_3", "type": "armor", "scr_count": 1, "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Экранирующее покрытие", "EN_Full": "Cuirass: Protective Coating", "UA_Full": "Екзоскелет «Панцир»: Екранувальне покриття", "RU_Desc": "Защитное экранирование.", "EN_Desc": "Protective shielding.", "UA_Desc": "Захисне екранування.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_4", "type": "armor", "scr_count": 1, "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Свинцовый контейнер", "EN_Full": "Cuirass: Lead Container", "UA_Full": "Екзоскелет «Панцир»: Свинцевий контейнер", "RU_Desc": "Контейнер под радиационные арты.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Напыленный защитный слой", "EN_Full": "Shield of Duty: Sprayed Layer", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Напилений шар", "RU_Desc": "Повышает износостойкость без увеличения веса.", "EN_Desc": "Enhances durability without extra weight.", "UA_Desc": "Підвищує зносостійкість без збільшення ваги.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1, "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Увеличенный рюкзак", "EN_Full": "Shield of Duty: Expanded Backpack", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Збільшений рюкзак", "RU_Desc": "Дополнительная ниша для вещей на молнии.", "EN_Desc": "Expanded zippered backpack section.", "UA_Desc": "Додаткова ніша для речей на блискавці.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_3", "type": "armor", "scr_count": 1, "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Экранирующее покрытие", "EN_Full": "Shield of Duty: Protective Coating", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Екранувальне покриття", "RU_Desc": "Защитное экранирование от аномалий.", "EN_Desc": "Protective shielding.", "UA_Desc": "Захисне екранування.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_4", "type": "armor", "scr_count": 1, "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Свинцовый контейнер", "EN_Full": "Shield of Duty: Lead Container", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек под артефакт.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy_Duty_Helmet_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Сфера-М20»", "EN_Short": "Sphere M20", "UA_Short": "«Сфера-М20»", "RU_Full": "Шлем «Сфера-М20»: Арамидная подкладка", "EN_Full": "Sphere M20: Aramid Lining", "UA_Full": "Шолом «Сфера-М20»: Арамідна підкладка", "RU_Desc": "Арамидная подкладка гасит импульс от ударов и пуль.", "EN_Desc": "Aramid lining disperses impact force.", "UA_Desc": "Арамідна підкладка зупиняє осколки.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Battle_Military_Helmet_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "Баллистический шлем", "EN_Short": "Ballistic Helmet", "UA_Short": "Балістичний шолом", "RU_Full": "Баллистический шлем: Арамидная подкладка", "EN_Full": "Ballistic Helmet: Aramid Lining", "UA_Full": "Балістичний шолом: Арамідна підкладка", "RU_Desc": "Останавливает осколки и пули.", "EN_Desc": "Stops bullets and shrapnel.", "UA_Desc": "Зупиняє осколки та кулі.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy_Svoboda_Helmet_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "«Маска-1»", "EN_Short": "Mask-1 Helmet", "UA_Short": "«Маска-1»", "RU_Full": "Шлем «Маска-1»: Арамидная подкладка", "EN_Full": "Mask-1 Helmet: Aramid Lining", "UA_Full": "Шолом «Маска-1»: Арамідна підкладка", "RU_Desc": "Защита головы от осколков.", "EN_Desc": "Head protection against shrapnel.", "UA_Desc": "Захист голови від осколків.", "teleport_cmd": "XTeleportTo 0 0 0"},
  {"id": "Blueprint_Heavy_Military_Helmet_Upgrade_1", "type": "armor", "scr_count": 1, "RU_Short": "Тактический шлем", "EN_Short": "Tactical Helmet", "UA_Short": "Тактичний шолом", "RU_Full": "Тактический шлем: Плексигласовые накладки с экранирующим покрытием", "EN_Full": "Tactical Helmet: Plexiglas Overlays", "UA_Full": "Тактичний шолом: Плексигласові накладки", "RU_Desc": "Защищает не только от бета-, но и от пси-излучения.", "EN_Desc": "Shields against beta- and psi-radiation.", "UA_Desc": "Захищає від бета- й псі-випромінювання.", "teleport_cmd": "XTeleportTo 0 0 0"}
]

SVG_CHECK_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzAwRTY3NiIgZmlsbC1vcGFjaXR5PSIwLjIiIHN0cm9rZT0iIzAwRTY3NiIgc3Ryb2tlLXdpZHRoPSIyIi8+PHBhdGggZD0iTTggMTJMMTEgMTVMMTYgOSIgc3Ryb2tlPSIjMDBFNjc2IiBzdHJva2Utd2lkdGg9IjIuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+"
SVG_CROSS_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzFFMjYzOCIgZmlsbC1vcGFjaXR5PSIwLjgiIHN0cm9rZT0iIzMzNDE1NSIgc3Ryb2tlLXdpZHRoPSIxLjUiLz48cGF0aCBkPSJNOSA5TDE1IDE1TTE1IDlMOSAxNSIgc3Ryb2tlPSIjNjQ3NDhCIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg=="

TEXTS = {
    "ru": {
        "header": "🛠️ Чертёжные схемы (Апгрейды)",
        "desc_bar": "Найдено чертежей",
        "cat_weapon": "🔫 Оружейные чертежи",
        "cat_armor": "🛡️ Чертежи брони и экипировки",
        "copy_tip": "Кликните для подробностей и карты",
        "summary_btn": "📥 Скачать команды недостающих чертежей",
        "teleport": "📍 Команда телепорта к чертежу:",
        "spawn": "📦 Команда для спавна в инвентарь:",
        "slide_map": "🗺️ Карта местности",
        "slide_scr": "📸 Скриншот тайника",
        "found": "НАЙДЕНО",
        "missing": "НЕ НАЙДЕНО"
    },
    "uk": {
        "header": "🛠️ Схеми креслень (Апгрейди)",
        "desc_bar": "Знайдено креслень",
        "cat_weapon": "🔫 Збройові креслення",
        "cat_armor": "🛡️ Креслення броні та екіпірування",
        "copy_tip": "Клікніть для деталей та карти",
        "summary_btn": "📥 Завантажити команди відсутніх креслень",
        "teleport": "📍 Команда телепорту до креслення:",
        "spawn": "📦 Команда для спавну в інвентар:",
        "slide_map": "🗺️ Карта розташування",
        "slide_scr": "📸 Скріншот схованки",
        "found": "ЗНАЙДЕНО",
        "missing": "НЕ ЗНАЙДЕНО"
    },
    "en": {
        "header": "🛠️ Blueprints (Upgrades)",
        "desc_bar": "Found Blueprints",
        "cat_weapon": "🔫 Weapon Blueprints",
        "cat_armor": "🛡️ Armor & Gear Blueprints",
        "copy_tip": "Click for details and location map",
        "summary_btn": "📥 Download missing blueprints commands",
        "teleport": "📍 Teleport command to blueprint:",
        "spawn": "📦 Inventory spawn command:",
        "slide_map": "🗺️ Location Map",
        "slide_scr": "📸 In-game Screenshot",
        "found": "FOUND",
        "missing": "NOT FOUND"
    }
}

def find_blueprints(raw_bytes):
    found = set()
    if not raw_bytes:
        return found
    for bp in BLUEPRINTS_DATA:
        b_id = bp["id"]
        if b_id.encode("ascii") in raw_bytes or b_id.encode("utf-16le") in raw_bytes:
            found.add(b_id)
    return found

def render_blueprints_section(raw_bytes, lang="ru", art_filter="all"):
    if not raw_bytes:
        return

    txt = TEXTS.get(lang, TEXTS["ru"])
    lp = "RU" if lang == "ru" else ("UA" if lang == "uk" else "EN")
    
    found_bps = find_blueprints(raw_bytes)

    total_count = len(BLUEPRINTS_DATA)
    total_found = sum(1 for b in BLUEPRINTS_DATA if b["id"] in found_bps)
    total_pct = int(total_found / total_count * 100) if total_count > 0 else 0

    weapons = [b for b in BLUEPRINTS_DATA if b["type"] == "weapon"]
    armors = [b for b in BLUEPRINTS_DATA if b["type"] == "armor"]

    # Стили модального окна
    st.markdown(f"""
    <style>
    .bp-modal-overlay {{
        display: none;
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(4, 6, 10, 0.85);
        backdrop-filter: blur(6px);
        z-index: 9999999 !important;
        align-items: center;
        justify-content: center;
        padding: 20px;
        box-sizing: border-box;
    }}
    .bp-modal-box {{
        background: #111520;
        border: 1px solid #1E2638;
        border-radius: 14px;
        max-width: 680px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
        padding: 22px 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9);
        position: relative;
        color: #F8FAFC;
    }}
    .bp-modal-close {{
        position: absolute;
        top: 14px; right: 16px;
        background: #1E2638;
        border: none;
        border-radius: 50%;
        width: 32px; height: 32px;
        color: #94A3B8;
        font-size: 1.1rem;
        cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        transition: all 0.2s ease;
    }}
    .bp-modal-close:hover {{
        background: #EF4444;
        color: #FFF;
    }}
    .bp-copy-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0A0D14;
        border: 1px solid #1E2638;
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    .bp-copy-row:hover {{
        border-color: #00E676;
        background: rgba(0, 230, 118, 0.05);
    }}
    .bp-copy-tag {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #94A3B8;
        background: #111520;
        border: 1px solid #1E2638;
        padding: 2px 8px;
        border-radius: 4px;
    }}
    .bp-copy-row:hover .bp-copy-tag {{
        color: #00E676;
        border-color: rgba(0, 230, 118, 0.4);
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #1E2638; margin: 40px 0 25px 0;'>", unsafe_allow_html=True)

    # 1. ЕДИНЫЙ ПРОГРЕСС-БАР (ИКОНКА blue.png)
    st.markdown(f"""
    <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 18px 22px; margin-bottom: 25px; display: flex; align-items: center; gap: 20px;">
        <img src="{HEADER_ICON_MAIN}" onerror="this.onerror=null; this.src='{HEADER_ICON_FALLBACK}';" style="width: 58px; height: 58px; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));" />
        <div style="flex-grow: 1;">
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #F8FAFC; font-size: 1.3rem; font-weight: 800;">{txt['header']}</span>
                <span style="color: #00E676; font-size: 0.95rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 10px;">{total_pct}%</span>
            </div>
            <div style="display: flex; justify-content: space-between; color: #94A3B8; font-size: 0.85rem; font-weight: 600; margin-bottom: 6px;">
                <span>{txt['desc_bar']}: <b style="color: #F8FAFC;">{total_found} / {total_count}</b></span>
            </div>
            <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {total_pct}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    categories = [
        (txt['cat_weapon'], weapons),
        (txt['cat_armor'], armors)
    ]

    # 2. СЕТКА КАРТОЧЕК (С АВТОМАТИЧЕСКОЙ ЗАГЛУШКОЙ icon_def_blue.png ЧЕРЕЗ CSS)
    for cat_name, items in categories:
        found_in_cat = sum(1 for item in items if item["id"] in found_bps)
        cat_title = f"{cat_name} [{found_in_cat}/{len(items)}]"

        filtered_items = []
        for item in items:
            is_f = item["id"] in found_bps
            if art_filter == "missing" and is_f:
                continue
            if art_filter == "found" and not is_f:
                continue
            filtered_items.append(item)

        if not filtered_items:
            continue

        with st.expander(cat_title, expanded=True):
            grid_html = '<div class="art-grid">\n'
            for bp in filtered_items:
                b_id = bp["id"]
                is_f = b_id in found_bps
                status_svg = f'<img src="{SVG_CHECK_B64}" width="18" height="18" />' if is_f else f'<img src="{SVG_CROSS_B64}" width="18" height="18" />'
                status_class = "tile-found" if is_f else "tile-missing"

                short_name = bp.get(f"{lp}_Short", bp["RU_Short"])
                full_name = bp.get(f"{lp}_Full", bp["RU_Full"])
                desc = bp.get(f"{lp}_Desc", bp["RU_Desc"])

                icon_url = get_bp_icon_url(b_id)
                map_url = get_map_url(b_id)
                scr_url = get_scr_url(b_id, 1)
                teleport_cmd = bp.get("teleport_cmd", "XTeleportTo 0 0 0")
                spawn_cmd = f"XCreateItemInInventoryByID {b_id} 0 1 1"

                # Двойной CSS-фон: сначала ищет icon_ID.png, если его нет — выводит icon_def_blue.png!
                img_css_bg = f"background-image: url('{icon_url}'), url('{DEF_CARD_ICON_MAIN}'), url('{DEF_CARD_ICON_FALLBACK}');"

                payload = json.dumps({
                    "id": b_id,
                    "title": full_name,
                    "desc": desc,
                    "found": is_f,
                    "map": map_url,
                    "scr": scr_url,
                    "teleport": teleport_cmd,
                    "spawn": spawn_cmd
                }).replace('"', '&quot;')

                grid_html += f'''
<div class="art-tile bp-clickable-tile {status_class}" data-bp="{payload}">
    <div class="tile-badge">{status_svg}</div>
    <div class="tile-img-container">
        <div class="tile-img" style="{img_css_bg}"></div>
    </div>
    <div class="tile-label-container">
        <div class="tile-label" title="{short_name}">{short_name}</div>
    </div>
    <div class="tooltip-box">
        <div style="font-weight: 700; color: #FFB000; font-size: 0.82rem; margin-bottom: 6px; border-bottom: 1px solid rgba(255,176,0,0.25); padding-bottom: 3px;">
            {full_name}
        </div>
        <div style="width: 100%; border-radius: 6px; overflow: hidden; margin-bottom: 6px; background: #0A0D14; border: 1px solid #1E2638; text-align: center;">
            <img src="{map_url}" onerror="this.parentElement.style.display='none';" style="width: 100%; max-height: 100px; object-fit: cover; display: block;" />
        </div>
        <div style="color: #CBD5E1; font-size: 0.74rem; line-height: 1.35; margin-bottom: 6px;">
            {desc}
        </div>
        <div style="color: #64748B; font-size: 0.68rem; border-top: 1px solid #1E2638; padding-top: 4px; text-align: center;">
            <span>{txt['copy_tip']}</span>
        </div>
    </div>
</div>'''
            grid_html += '</div>\n'
            st.markdown(f"<div>{grid_html.replace(chr(10), '')}</div>", unsafe_allow_html=True)

    # Скачивание файла со списком недостающих чертежей
    missing_bps = [b for b in BLUEPRINTS_DATA if b["id"] not in found_bps]
    if missing_bps:
        txt_content = "=========================================================\n"
        txt_content += "      СПИСОК НЕДОСТАЮЩИХ ЧЕРТЕЖЕЙ S.T.A.L.K.E.R. 2\n"
        txt_content += f"      Недостает схем: {len(missing_bps)} из {total_count}\n"
        txt_content += "=========================================================\n\n"
        
        txt_content += "▶ Команды спавна недостающих чертежей в инвентарь:\n"
        txt_content += "|".join([f"XCreateItemInInventoryByID {b['id']} 0 1 1" for b in missing_bps]) + "\n\n"
        
        txt_content += "▶ Координаты телепорта к недостающим чертежам:\n"
        for b in missing_bps:
            name = b.get(f"{lp}_Full", b["RU_Full"])
            t_cmd = b.get("teleport_cmd", "XTeleportTo 0 0 0")
            txt_content += f"  • {name}: {t_cmd}\n"

        st.markdown("<br/>", unsafe_allow_html=True)
        st.download_button(
            label=txt['summary_btn'],
            data=txt_content,
            file_name="Missing_Blueprints.txt",
            mime="text/plain",
            key="dl_blueprints"
        )

    # JS-модальное окно
    components.html(f"""
    <script>
    try {{
        const pDoc = window.parent.document;

        let modalEl = pDoc.getElementById('bp-dynamic-modal');
        if(!modalEl) {{
            modalEl = pDoc.createElement('div');
            modalEl.id = 'bp-dynamic-modal';
            modalEl.className = 'bp-modal-overlay';
            modalEl.innerHTML = `
                <div class="bp-modal-box">
                    <button class="bp-modal-close" id="bp-modal-close-btn">&times;</button>
                    <div id="bp-modal-content"></div>
                </div>
            `;
            pDoc.body.appendChild(modalEl);

            modalEl.addEventListener('click', function(e) {{
                if(e.target === modalEl || e.target.id === 'bp-modal-close-btn') {{
                    modalEl.style.display = 'none';
                }}
            }});
        }}

        pDoc.addEventListener('click', function(e) {{
            let tile = e.target.closest('.bp-clickable-tile');
            if(tile) {{
                let rawData = tile.getAttribute('data-bp');
                if(rawData) {{
                    let data = JSON.parse(rawData);
                    let statusColor = data.found ? '#00E676' : '#EF4444';
                    let statusBg = data.found ? 'rgba(0, 230, 118, 0.1)' : 'rgba(239, 68, 68, 0.1)';
                    let statusText = data.found ? '{txt["found"]}' : '{txt["missing"]}';

                    let contentHtml = `
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E2638; padding-bottom: 12px; margin-bottom: 15px;">
                            <h3 style="color: #FFB000; margin: 0; font-size: 1.25rem; font-weight: 800;">${{data.title}}</h3>
                            <span style="color: ${{statusColor}}; background: ${{statusBg}}; border: 1px solid ${{statusColor}}; border-radius: 6px; padding: 4px 10px; font-size: 0.8rem; font-weight: 700;">${{statusText}}</span>
                        </div>

                        <!-- КАРТА (ПЕРВАЯ) -->
                        <div style="margin-bottom: 12px;">
                            <div style="color: #FFB000; font-size: 0.82rem; font-weight: 700; margin-bottom: 4px;">{txt['slide_map']}</div>
                            <div style="width: 100%; border-radius: 8px; overflow: hidden; border: 1px solid #1E2638; background: #0A0D14; text-align: center;">
                                <img src="${{data.map}}" onerror="this.parentElement.style.display='none';" style="width: 100%; max-height: 380px; object-fit: contain; display: block;" />
                            </div>
                        </div>

                        <!-- СКРИНШОТ (ВТОРОЙ) -->
                        <div style="margin-bottom: 15px;">
                            <div style="color: #FFB000; font-size: 0.82rem; font-weight: 700; margin-bottom: 4px;">{txt['slide_scr']}</div>
                            <div style="width: 100%; border-radius: 8px; overflow: hidden; border: 1px solid #1E2638; background: #0A0D14; text-align: center;">
                                <img src="${{data.scr}}" onerror="this.parentElement.style.display='none';" style="width: 100%; max-height: 380px; object-fit: contain; display: block;" />
                            </div>
                        </div>

                        <!-- ОПИСАНИЕ -->
                        <div style="background: #0A0D14; border-left: 3px solid #FFB000; border-radius: 6px; padding: 10px 14px; margin-bottom: 16px; color: #CBD5E1; font-size: 0.9rem; line-height: 1.45;">
                            ${{data.desc}}
                        </div>

                        <!-- ТЕЛЕПОРТ -->
                        <div style="margin-bottom: 10px;">
                            <span style="color: #FFB000; font-size: 0.82rem; font-weight: 700;">{txt['teleport']}</span>
                            <div class="bp-copy-row bp-btn-copy" data-copy="${{data.teleport}}">
                                <code style="color: #00E676; font-size: 0.86rem; background: transparent;">${{data.teleport}}</code>
                                <span class="bp-copy-tag">📋 Копировать</span>
                            </div>
                        </div>

                        <!-- СПАВН -->
                        <div>
                            <span style="color: #FFB000; font-size: 0.82rem; font-weight: 700;">{txt['spawn']}</span>
                            <div class="bp-copy-row bp-btn-copy" data-copy="${{data.spawn}}">
                                <code style="color: #00E676; font-size: 0.86rem; background: transparent; word-break: break-all;">${{data.spawn}}</code>
                                <span class="bp-copy-tag">📋 Копировать</span>
                            </div>
                        </div>
                    `;

                    pDoc.getElementById('bp-modal-content').innerHTML = contentHtml;
                    modalEl.style.display = 'flex';
                }}
            }}

            let copyBtn = e.target.closest('.bp-btn-copy');
            if(copyBtn) {{
                let text = copyBtn.getAttribute('data-copy');
                if(text) {{
                    pDoc.defaultView.navigator.clipboard.writeText(text).then(() => {{
                        let tag = copyBtn.querySelector('.bp-copy-tag');
                        if(tag) {{
                            let prev = tag.innerText;
                            tag.innerText = "✅ Скопировано!";
                            tag.style.color = "#00E676";
                            setTimeout(() => {{ tag.innerText = prev; tag.style.color = ""; }}, 1400);
                        }}
                    }});
                }}
            }}
        }});
    }} catch(e) {{
        console.error(e);
    }}
    </script>
    """, height=0, width=0)
