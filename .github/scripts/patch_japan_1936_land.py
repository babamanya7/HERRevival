from pathlib import Path
import re

p = Path('history/units/JAP_1936_nsb.txt')
s = p.read_text(encoding='utf-8-sig')

# Rebuild starting land templates around the actual 1 Jan 1936 organisation.
oob_mark = '##### OOB #####'
assert oob_mark in s
_, rest = s.split(oob_mark, 1)

templates = r'''division_template = {
    name = "Hohei Shidan"
    division_names_group = JAP_INF_01
    # Old standing square division: 2 infantry brigades x 2 regiments x 3 battalions.
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
        heavy_infantry = { x = 0 y = 2 }
        heavy_infantry = { x = 1 y = 0 }
        heavy_infantry = { x = 1 y = 1 }
        heavy_infantry = { x = 1 y = 2 }
        heavy_infantry = { x = 2 y = 0 }
        heavy_infantry = { x = 2 y = 1 }
        heavy_infantry = { x = 2 y = 2 }
        heavy_infantry = { x = 3 y = 0 }
        heavy_infantry = { x = 3 y = 1 }
        heavy_infantry = { x = 3 y = 2 }
        artillery_brigade = { x = 4 y = 0 }
        artillery_brigade = { x = 4 y = 1 }
        artillery_brigade = { x = 4 y = 2 }
    }
    regimental_support = {
        artillery = { x = 0 y = 0 }
        artillery = { x = 1 y = 0 }
        artillery = { x = 2 y = 0 }
        artillery = { x = 3 y = 0 }
    }
    support = {
        engineer = { x = 0 y = 0 }
        field_hospital = { x = 0 y = 1 }
        signal_company = { x = 0 y = 2 }
        recon = { x = 0 y = 3 }
        logistics_company = { x = 0 y = 4 }
    }
}

division_template = {
    name = "Konoe Shidan"
    division_names_group = JAP_INF_01
    # Imperial Guard was a foot infantry division, not a motorized formation.
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
        heavy_infantry = { x = 0 y = 2 }
        heavy_infantry = { x = 1 y = 0 }
        heavy_infantry = { x = 1 y = 1 }
        heavy_infantry = { x = 1 y = 2 }
        heavy_infantry = { x = 2 y = 0 }
        heavy_infantry = { x = 2 y = 1 }
        heavy_infantry = { x = 2 y = 2 }
        heavy_infantry = { x = 3 y = 0 }
        heavy_infantry = { x = 3 y = 1 }
        heavy_infantry = { x = 3 y = 2 }
        artillery_brigade = { x = 4 y = 0 }
        artillery_brigade = { x = 4 y = 1 }
        artillery_brigade = { x = 4 y = 2 }
    }
    regimental_support = {
        artillery = { x = 0 y = 0 }
        artillery = { x = 1 y = 0 }
        artillery = { x = 2 y = 0 }
        artillery = { x = 3 y = 0 }
    }
    support = {
        engineer = { x = 0 y = 0 }
        field_hospital = { x = 0 y = 1 }
        signal_company = { x = 0 y = 2 }
        recon = { x = 0 y = 3 }
        logistics_company = { x = 0 y = 4 }
    }
    priority = 2
}

division_template = {
    name = "Dai-1 Dokuritsu Konsei Ryodan"
    division_names_group = JAP_IMB_01
    # 1st Mixed Brigade: one independent infantry regiment, two tank battalions, field artillery.
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
        heavy_infantry = { x = 0 y = 2 }
        light_armor = { x = 1 y = 0 }
        light_armor = { x = 1 y = 1 }
        artillery_brigade = { x = 2 y = 0 }
    }
    support = { engineer = { x = 0 y = 0 } }
}

division_template = {
    name = "Dai-11 Dokuritsu Konsei Ryodan"
    division_names_group = JAP_IMB_01
    # 11th Mixed Brigade: two independent infantry regiments and strong field artillery; no tank battalions.
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
        heavy_infantry = { x = 0 y = 2 }
        heavy_infantry = { x = 1 y = 0 }
        heavy_infantry = { x = 1 y = 1 }
        heavy_infantry = { x = 1 y = 2 }
        artillery_brigade = { x = 2 y = 0 }
        artillery_brigade = { x = 2 y = 1 }
    }
    support = { engineer = { x = 0 y = 0 } }
}

division_template = {
    name = "Karafuto Konsei Ryodan"
    division_names_group = JAP_IMB_01
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
        heavy_infantry = { x = 1 y = 0 }
        heavy_infantry = { x = 1 y = 1 }
        artillery_brigade = { x = 2 y = 0 }
    }
    support = { engineer = { x = 0 y = 0 } }
}

division_template = {
    name = "Kihei Ryodan"
    division_names_group = JAP_CAV_01
    # Cavalry brigade: two cavalry regiments plus brigade fire support.
    regiments = {
        cavalry = { x = 0 y = 0 }
        cavalry = { x = 0 y = 1 }
        cavalry = { x = 1 y = 0 }
        cavalry = { x = 1 y = 1 }
    }
    regimental_support = { artillery = { x = 0 y = 0 } }
}

division_template = {
    name = "Shina Chuton Rentai"
    division_names_group = JAP_GAR_01
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
    }
    priority = 0
}

division_template = {
    name = "Taiwan Chuton Rentai"
    division_names_group = JAP_GAR_01
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
        heavy_infantry = { x = 0 y = 2 }
    }
    priority = 0
}

division_template = {
    name = "Kantogun Dokuritsu Shubitai"
    division_names_group = JAP_GAR_01
    # Independent Garrison Unit: six independent guard battalions.
    regiments = {
        heavy_infantry = { x = 0 y = 0 }
        heavy_infantry = { x = 0 y = 1 }
        heavy_infantry = { x = 0 y = 2 }
        heavy_infantry = { x = 1 y = 0 }
        heavy_infantry = { x = 1 y = 1 }
        heavy_infantry = { x = 1 y = 2 }
    }
    priority = 0
}

division_template = {
    name = "Kichi Shubitai"
    division_names_group = JAP_GAR_01
    # Small home naval-base/security detachment; not a pseudo-division.
    regiments = { heavy_infantry = { x = 0 y = 0 } }
    priority = 0
}

division_template = {
    name = "Rikusentai"
    division_names_group = JAP_MAR_01
    # SNLF were battalion/regimental-sized in this period, not six-battalion divisions.
    regiments = {
        marine = { x = 0 y = 0 }
        marine = { x = 0 y = 1 }
        marine = { x = 0 y = 2 }
    }
    support = { engineer = { x = 0 y = 0 } }
    priority = 2
}

'''

# Build a clean 1 Jan 1936 OOB instead of retaining later-1936/1937 field-army groupings.
oob = r'''##### OOB #####
units = {
    ##### HOME ISLANDS #####
    division = { # Imperial Guards Division, Tokyo
        division_name = { is_name_ordered = yes name_order = 168 }
        location = 1182
        division_template = "Konoe Shidan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.90
    }
    division = { # 1st Division - still Tokyo on 1 Jan; ordered to Manchuria only before Feb 26 Incident
        division_name = { is_name_ordered = yes name_order = 1 }
        location = 1182
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.85
    }
    division = { # 2nd Division - Sendai
        division_name = { is_name_ordered = yes name_order = 2 }
        location = 7169
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.82
    }
    division = { # 4th Division - Osaka
        division_name = { is_name_ordered = yes name_order = 4 }
        location = 7072
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.82
    }
    division = { # 5th Division - Hiroshima; not North China until 1937
        division_name = { is_name_ordered = yes name_order = 5 }
        location = 1092
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.82
    }
    division = { # 6th Division - Kumamoto
        division_name = { is_name_ordered = yes name_order = 6 }
        location = 11925
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.82
    }
    division = { # 7th Division - Asahikawa
        division_name = { is_name_ordered = yes name_order = 7 }
        location = 12421
        division_template = "Hohei Shidan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.85
    }
    division = { # 8th Division - Hirosaki/Aomori; earlier Manchurian rotation already ended
        division_name = { is_name_ordered = yes name_order = 8 }
        location = 6994
        division_template = "Hohei Shidan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.84
    }
    division = { # 10th Division - Himeji district (Osaka-area map proxy)
        division_name = { is_name_ordered = yes name_order = 10 }
        location = 7072
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.82
    }
    division = { # 11th Division - Zentsuji/Shikoku (Kochi map proxy)
        division_name = { is_name_ordered = yes name_order = 11 }
        location = 7197
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.82
    }
    division = { # 12th Division - Kurume district on 1 Jan; rotating elements move to Manchuria later in 1936
        division_name = { is_name_ordered = yes name_order = 12 }
        location = 1025
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.85
    }
    division = { # 14th Division - Utsunomiya/Kanto; returned from Manchuria in 1934
        division_name = { is_name_ordered = yes name_order = 14 }
        location = 1182
        division_template = "Hohei Shidan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.84
    }
    division = { # 16th Division - Kyoto
        division_name = { is_name_ordered = yes name_order = 16 }
        location = 11960
        division_template = "Hohei Shidan"
        start_experience_factor = 0.25
        start_equipment_factor = 0.82
    }

    # Karafuto permanent brigade
    division = {
        name = "Karafuto Dokuritsu Konsei Ryodan"
        location = 12446
        division_template = "Karafuto Konsei Ryodan"
        start_experience_factor = 0.20
        start_equipment_factor = 0.80
    }

    # Small home naval/base security detachments retained only at major bases.
    division = { name = "Ominato Kichi Kaiheidan" location = 9859 division_template = "Kichi Shubitai" start_experience_factor = 0.10 start_equipment_factor = 0.70 }
    division = { name = "Yokosuka Kichi Shubitai" location = 9998 division_template = "Kichi Shubitai" start_experience_factor = 0.10 start_equipment_factor = 0.70 }
    division = { name = "Kure Kichi Kaiheidan" location = 1092 division_template = "Kichi Shubitai" start_experience_factor = 0.10 start_equipment_factor = 0.70 }
    division = { name = "Sasebo Kichi Kaiheidan" location = 9950 division_template = "Kichi Shubitai" start_experience_factor = 0.10 start_equipment_factor = 0.70 }
    division = { name = "Yokosuka Tokubetsu Rikusentai" location = 9998 division_template = "Rikusentai" start_experience_factor = 0.25 start_equipment_factor = 0.80 }

    ##### TAIWAN ARMY #####
    # No metropolitan infantry divisions were stationed on Taiwan on 1 Jan 1936.
    division = {
        name = "Taiwan Hohei Dai-1 Rentai"
        location = 7186
        division_template = "Taiwan Chuton Rentai"
        start_experience_factor = 0.20
        start_equipment_factor = 0.82
    }
    division = {
        name = "Taiwan Hohei Dai-2 Rentai"
        location = 12068
        division_template = "Taiwan Chuton Rentai"
        start_experience_factor = 0.20
        start_equipment_factor = 0.82
    }

    ##### KOREA ARMY #####
    division = { # 19th Division - Ranam / northern Korea
        division_name = { is_name_ordered = yes name_order = 19 }
        location = 4052
        division_template = "Hohei Shidan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.88
    }
    division = { # 20th Division - Yongsan/Seoul
        division_name = { is_name_ordered = yes name_order = 20 }
        location = 7125
        division_template = "Hohei Shidan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.88
    }
    division = { name = "Chinkai Kichi Kaiheidan" location = 4056 division_template = "Kichi Shubitai" start_experience_factor = 0.10 start_equipment_factor = 0.70 }

    ##### KWANTUNG ARMY - MANCHURIA #####
    # 3rd Division: on rotating Manchurian station since 1934; returns to Japan in March 1936.
    division = {
        division_name = { is_name_ordered = yes name_order = 3 }
        location = 3843
        division_template = "Hohei Shidan"
        start_experience_factor = 0.32
        start_equipment_factor = 0.92
    }
    # 9th Division: Manchukuo garrison 1935-February 1937.
    division = {
        division_name = { is_name_ordered = yes name_order = 9 }
        location = 3944
        division_template = "Hohei Shidan"
        start_experience_factor = 0.32
        start_equipment_factor = 0.92
    }

    # Cavalry Group: 1st and 4th Cavalry Brigades permanently in Manchuria since 1934.
    division = { name = "Kihei Dai-1 Ryodan" location = 7697 division_template = "Kihei Ryodan" start_experience_factor = 0.30 start_equipment_factor = 0.88 }
    division = { name = "Kihei Dai-4 Ryodan" location = 7697 division_template = "Kihei Ryodan" start_experience_factor = 0.30 start_equipment_factor = 0.88 }

    # The two mixed brigades had very different organizations.
    division = {
        name = "Dai-1 Dokuritsu Konsei Ryodan"
        location = 10612 # Gongzhuling area
        division_template = "Dai-1 Dokuritsu Konsei Ryodan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.90
    }
    division = {
        name = "Dai-11 Dokuritsu Konsei Ryodan"
        location = 11822 # Chengde
        division_template = "Dai-11 Dokuritsu Konsei Ryodan"
        start_experience_factor = 0.30
        start_equipment_factor = 0.88
    }

    # Four independent garrison units existed by 1934; the 5th was only created during 1936.
    division = { name = "Dai-1 Dokuritsu Shubitai" location = 11771 division_template = "Kantogun Dokuritsu Shubitai" start_experience_factor = 0.20 start_equipment_factor = 0.82 }
    division = { name = "Dai-2 Dokuritsu Shubitai" location = 4572 division_template = "Kantogun Dokuritsu Shubitai" start_experience_factor = 0.20 start_equipment_factor = 0.82 }
    division = { name = "Dai-3 Dokuritsu Shubitai" location = 7697 division_template = "Kantogun Dokuritsu Shubitai" start_experience_factor = 0.20 start_equipment_factor = 0.80 }
    division = { name = "Dai-4 Dokuritsu Shubitai" location = 3843 division_template = "Kantogun Dokuritsu Shubitai" start_experience_factor = 0.20 start_equipment_factor = 0.80 }

    ##### CHINA GARRISON ARMY #####
    # Before the May 1936 reinforcement the Tientsin garrison was only about 2,000 men.
    division = {
        name = "Shina Chuton Hohei Rentai"
        location = 10068 # Tianjin
        division_template = "Shina Chuton Rentai"
        start_experience_factor = 0.25
        start_equipment_factor = 0.85
    }

    # No Mengjiang/Mongol cavalry divisions: their large Japanese-sponsored expansion occurs later in 1936.
    # No visible Pacific-island pseudo-divisions: militarisation was still infrastructure/base preparation, not later-war mass garrisons.
}

'''

# Preserve production block only.
prod_marker = '#########################\n## STARTING PRODUCTION ##'
assert prod_marker in rest
prod = prod_marker + rest.split(prod_marker, 1)[1]
new = templates + oob + '\n\n' + prod

p.write_text('\ufeff' + new, encoding='utf-8')
clean = re.sub(r'#.*', '', new)
assert clean.count('{') == clean.count('}'), (clean.count('{'), clean.count('}'))

# Sanity checks for core historical corrections.
for token in ['Konoe Shidan', 'Dai-1 Dokuritsu Konsei Ryodan', 'Dai-11 Dokuritsu Konsei Ryodan', 'Kihei Dai-4 Ryodan', 'Taiwan Hohei Dai-2 Rentai']:
    assert token in new
assert 'Mouko Kiheishidan' not in new
assert 'Jidousha Shidan' not in new
