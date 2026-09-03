from pathlib import Path
import re

p = Path('history/units/CHI_1936.txt')
s = p.read_text(encoding='utf-8-sig')

# Replace the ambiguous starting templates with formations that map to actual 1936 division strengths.
oob = s.index('### OOB ###')
templates = '''division_template = {
    name = "Juntuán"
    division_names_group = CHI_INF_01
    # Ordinary NRA/provincial field division: nominal four-regiment organisation,
    # usually only about 4,000-6,000 men actually present.
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
        infantry = { x = 1 y = 1 }
        infantry = { x = 2 y = 0 }
        infantry = { x = 2 y = 1 }
    }
    priority = 0
}

division_template = {
    name = "Sanjiao Jun"
    division_names_group = CHI_INF_01
    # 1935 New-Type / German-advised division: 4 regiments x 3 battalions.
    # Artillery is represented by one battalion because actual gun holdings lagged far below TO&E.
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 0 y = 2 }
        infantry = { x = 1 y = 0 }
        infantry = { x = 1 y = 1 }
        infantry = { x = 1 y = 2 }
        infantry = { x = 2 y = 0 }
        infantry = { x = 2 y = 1 }
        infantry = { x = 2 y = 2 }
        infantry = { x = 3 y = 0 }
        infantry = { x = 3 y = 1 }
        infantry = { x = 3 y = 2 }
        artillery_brigade = { x = 4 y = 0 }
    }
    support = {
        engineer = { x = 0 y = 0 }
        signal_company = { x = 0 y = 1 }
        recon = { x = 0 y = 2 }
    }
    priority = 1
}

division_template = {
    name = "29 Jun Zengqiang Shi"
    division_names_group = CHI_INF_01
    # Song Zheyuan's 29th Army divisions were exceptionally large four-brigade formations.
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 0 y = 2 }
        infantry = { x = 1 y = 0 }
        infantry = { x = 1 y = 1 }
        infantry = { x = 1 y = 2 }
        infantry = { x = 2 y = 0 }
        infantry = { x = 2 y = 1 }
        infantry = { x = 2 y = 2 }
        infantry = { x = 3 y = 0 }
        infantry = { x = 3 y = 1 }
        infantry = { x = 3 y = 2 }
        artillery_brigade = { x = 4 y = 0 }
    }
    support = { engineer = { x = 0 y = 0 } }
}

division_template = {
    name = "Jingbei Lu"
    division_names_group = CHI_INF_01
    # Peace-preservation / independent infantry brigade.
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
    }
    priority = 0
}

division_template = {
    name = "Teqin Lu"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
        infantry = { x = 1 y = 1 }
    }
    priority = 0
}

division_template = {
    name = "Qibing Shi"
    division_names_group = CHI_CAV_01
    # Typical cavalry division, roughly 3,000 men in the northern armies.
    regiments = {
        cavalry = { x = 0 y = 0 }
        cavalry = { x = 0 y = 1 }
        cavalry = { x = 1 y = 0 }
    }
}

division_template = {
    name = "Qibing Jun"
    division_names_group = CHI_CAV_01
    # Corps-level cavalry abstraction retained for formations not yet decomposed in this OOB.
    regiments = {
        cavalry = { x = 0 y = 0 }
        cavalry = { x = 0 y = 1 }
        cavalry = { x = 1 y = 0 }
        cavalry = { x = 1 y = 1 }
    }
}

'''
s = templates + s[oob:]

# 29th Army: four oversized infantry divisions were the standing Beiping-Tianjin force.
for name in ['37 Bubing Shi', '38 Bubing Shi', '132 Bubing Shi', '143 Bubing Shi']:
    pat = rf'(name = "{re.escape(name)}".*?division_template = )"Sanjiao Jun"(.*?start_experience_factor = 0\.2)'
    repl = rf'\1"29 Jun Zengqiang Shi"\2\n\t\tstart_equipment_factor = 0.80'
    s, n = re.subn(pat, repl, s, count=1, flags=re.S)
    assert n == 1, name

# Add the other permanent components of Song Zheyuan's 29th Army.
marker = '\n\t##### First War Area (CO: Cheng Qian) #####'
add29 = '''

    # 29th Army additional permanent formations (Beiping-Tianjin-Chahar)
    division = {
        name = "9 Qibing Shi"
        location = 9843 # Nanyuan / Beiping area
        division_template = "Qibing Shi"
        start_experience_factor = 0.20
        start_equipment_factor = 0.75
    }
    division = {
        name = "39 Duli Bubing Lu"
        location = 9843 # Beiyuan
        division_template = "Jingbei Lu"
        start_experience_factor = 0.15
        start_equipment_factor = 0.70
    }
    division = {
        name = "40 Duli Bubing Lu"
        location = 4140 # Zhangjiakou
        division_template = "Jingbei Lu"
        start_experience_factor = 0.15
        start_equipment_factor = 0.70
    }
    division = {
        name = "13 Duli Qibing Lu"
        location = 4140 # Xuanhua / Chahar
        division_template = "Qibing Shi"
        start_experience_factor = 0.15
        start_equipment_factor = 0.65
    }
    division = {
        name = "29 Jun Teqin Lu"
        location = 9843 # Nanyuan
        division_template = "Teqin Lu"
        start_experience_factor = 0.20
        start_equipment_factor = 0.75
    }
'''
assert marker in s
s = s.replace(marker, add29 + marker, 1)

# German-advised/reorganised divisions were the best Chinese infantry, but even these
# had serious shortages of artillery, communications gear and other modern equipment.
s = s.replace('start_equipment_factor = 1.0', 'start_equipment_factor = 0.85')

# Dedicated local garrisons should not consume a six-battalion field-division template.
for garrison in [
    '1 Fujian Jingbei', '2 Fujian Jingbei', '3 Fujian Jingbei', 'Shanghai Jingbei',
    '1 Nanking Jingbei', '2 Nanking Jingbei', '3 Nanking Jingbei', '4 Nanking Jingbei',
    'Qingdao Jingbei', 'Wuhan Jingbei'
]:
    pat = rf'(name = "{re.escape(garrison)}".*?division_template = )"Juntuán"'
    s = re.sub(pat, rf'\1"Jingbei Lu"', s, count=1, flags=re.S)

p.write_text('\ufeff' + s, encoding='utf-8')
clean = re.sub(r'#.*', '', s)
assert clean.count('{') == clean.count('}'), (clean.count('{'), clean.count('}'))
