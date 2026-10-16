"""Transliteration of 1926 unit and group names for English figures/tables."""
import re
_T = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya'}
OVR = {"губ.": "gub.", "АССР": "ASSR", "АО": "AO", "округ": "okrug", "обл.": "obl.", "Немцев Поволжья АССР": "Volga German ASSR",
       "Вотская АО": "Votyak (Udmurt) AO", "Марийская АО": "Mari AO", "Калмыцкая АО": "Kalmyk AO", "Коми-Пермяцкий округ": "Komi-Permyak okrug",
       "Русские": "Russians", "Татары": "Tatars", "Чуваши": "Chuvash", "Мордва": "Mordva", "Марийцы": "Mari", "Вотяки": "Votyaks (Udmurts)",
       "Башкиры": "Bashkirs", "Мишари": "Mishars", "Украинцы": "Ukrainians", "Евреи": "Jews", "Немцы": "Germans", "Казаки": "Kazakhs",
       "Карелы, финны, вепсы": "Karelians, Finns, Veps", "Калмыки": "Kalmyks", "Коми-пермяки": "Komi-Permyaks", "Прочие": "Others",
       "Всё население": "All"}
UNIT_EN = {"Астраханская губ.": "Astrakhan", "Башкирская АССР": "Bashkir ASSR", "Брянская губ.": "Bryansk", "Верхнекамский округ": "Verkhnekamsk okrug", "Воронежская губ.": "Voronezh",
           "Вотская АО": "Votyak AO", "Вятская губ.": "Vyatka", "Златоустовский округ": "Zlatoust okrug", "Ирбитский округ": "Irbit okrug", "Ишимский округ": "Ishim okrug", "Калмыцкая АО": "Kalmyk AO",
           "Карельская АССР": "Karelian ASSR", "Коми-Пермяцкий округ": "Komi-Permyak okrug", "Кунгурский округ": "Kungur okrug", "Курганский округ": "Kurgan okrug", "Курская губ.": "Kursk",
           "Ленинградская губ.": "Leningrad", "Марийская АО": "Mari AO", "Мурманская губ.": "Murmansk", "Немцев Поволжья АССР": "Volga German ASSR", "Нижегородская губ.": "Nizhny Novgorod",
           "Новгородская губ.": "Novgorod", "Оренбургская губ.": "Orenburg", "Орловская губ.": "Orel", "Пензенская губ.": "Penza", "Пермский округ": "Perm okrug", "Псковская губ.": "Pskov",
           "Самарская губ.": "Samara", "Сарапульский округ": "Sarapul okrug", "Саратовская губ.": "Saratov", "Свердловский округ": "Sverdlovsk okrug", "Смоленская губ.": "Smolensk",
           "Сталинградская губ.": "Stalingrad", "Тагильский округ": "Tagil okrug", "Тамбовская губ.": "Tambov", "Татарская АССР": "Tatar ASSR", "Тобольский округ": "Tobolsk okrug",
           "Троицкий округ": "Troitsk okrug", "Тюменский округ": "Tyumen okrug", "Ульяновская губ.": "Ulyanovsk", "Уральская обл.": "Ural oblast", "Челябинский округ": "Chelyabinsk okrug",
           "Череповецкая губ.": "Cherepovets", "Чувашская АССР": "Chuvash ASSR", "Шадринский округ": "Shadrinsk okrug",
           "Башкирская АССР ": "Bashkir ASSR", "Бурято-Монгольская АССР": "Buryat-Mongol ASSR", "Вятский район": "Vyatka region", "Дагестанская АССР": "Dagestan ASSR", "Дальне-Восточный край": "Far Eastern krai",
           "Западный район": "Western region", "Казакская АССР": "Kazak ASSR", "Киргизская АССР": "Kirgiz ASSR", "Крымская АССР": "Crimean ASSR", "Ленинградско-Карельский район": "Leningrad-Karelian region",
           "Нижне-Волжский район": "Lower Volga region", "Северный район": "Northern region", "Северо-Кавказский край": "North Caucasus krai", "Сибирский край": "Siberian krai",
           "Средне-Волжский район": "Middle Volga region", "Уральская область": "Ural oblast", "Центрально-Промышленный район": "Central Industrial region", "Центрально-Черноземный район": "Central Black Earth region",
           "Якутская АССР": "Yakut ASSR"}
NAT_EN = {"Русские": "Russians", "Татары": "Tatars", "Башкиры": "Bashkirs", "Мишари": "Mishars", "Чуваши": "Chuvash", "Марийцы": "Mari", "Мордва": "Mordva", "Вотяки": "Votyaks", "Удмурты": "Udmurts",
          "Калмыки": "Kalmyks", "Карелы": "Karelians", "Карелы, финны, вепсы": "Karelians", "Коми-пермяки": "Komi-Permyaks", "Немцы": "Germans", "Украинцы": "Ukrainians", "Евреи": "Jews", "Казаки": "Kazakhs", "Казахи": "Kazakhs"}
SUBJ_EN = {"Астраханская область": "Astrakhan", "Брянская область": "Bryansk", "Волгоградская область": "Volgograd", "Воронежская область": "Voronezh", "Кировская область": "Kirov",
           "Курганская область": "Kurgan", "Курская область": "Kursk", "Нижегородская область": "Nizhny Novgorod", "Оренбургская область": "Orenburg", "Пензенская область": "Penza", "Пермский край": "Perm",
           "Республика Башкортостан": "Bashkortostan", "Республика Калмыкия": "Kalmykia", "Республика Карелия": "Karelia", "Республика Марий Эл": "Mari El", "Республика Татарстан": "Tatarstan",
           "Самарская область": "Samara", "Саратовская область": "Saratov", "Свердловская область": "Sverdlovsk", "Тюменская область": "Tyumen", "Удмуртская Республика": "Udmurtia",
           "Ульяновская область": "Ulyanovsk", "Челябинская область": "Chelyabinsk", "Чувашская Республика": "Chuvashia"}
def en(s):
    return UNIT_EN.get(s, NAT_EN.get(s, SUBJ_EN.get(s, translit(s))))
def translit(s):
    if s in OVR: return OVR[s]
    for k, v in OVR.items():
        if k in s and len(k) > 3: s = s.replace(k, v)
    out = []
    for ch in s:
        lo = ch.lower()
        if lo in _T:
            t = _T[lo]; out.append(t.capitalize() if ch.isupper() else t)
        else: out.append(ch)
    s = "".join(out)
    return s.replace("iy ", "y ").replace("skiy", "sky").replace("aya ", "aya ")
