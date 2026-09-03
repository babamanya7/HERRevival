from pathlib import Path
import re

p = Path('history/units/CHI_1936.txt')
s = p.read_text(encoding='utf-8-sig')

# Add Shanxi/Suiyuan brigade templates.
marker = '### OOB ###'
assert marker in s
extra = r'''
division_template = {
    name = "Jinsui Duli Lu"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
    }
    priority = 0
}

division_template = {
    name = "Jinsui Qibing Lu"
    division_names_group = CHI_CAV_01
    regiments = {
        cavalry = { x = 0 y = 0 }
        cavalry = { x = 0 y = 1 }
    }
    priority = 0
}

'''
s = s.replace(marker, extra + marker, 1)

start = s.index('\t##### Second War Area (CO: Yan Xishan) #####')
end = s.index('\t##### Third War Area (CO: Gu Zhutong) #####', start)

block = r'''	##### Shanxi-Suiyuan Pacification Command (CO: Yan Xishan) #####
	# Pre-war Jinsui Army establishment, 1 Jan 1936. Later 1937 War Area labels removed.

	# 33rd Army Corps - western/northern Shanxi
	division = {
		name = "71 Bubing Shi"
		location = 1069
		division_template = "Juntuán"
		start_experience_factor = 0.15
		start_equipment_factor = 0.72
	}
	division = {
		name = "68 Bubing Shi"
		location = 1069
		division_template = "Juntuán"
		start_experience_factor = 0.15
		start_equipment_factor = 0.72
	}

	# 34th Army Corps - southeast/south Shanxi and western Suiyuan
	division = {
		name = "66 Bubing Shi"
		location = 1069
		division_template = "Juntuán"
		start_experience_factor = 0.15
		start_equipment_factor = 0.72
	}
	division = {
		name = "69 Bubing Shi"
		location = 1069
		division_template = "Juntuán"
		start_experience_factor = 0.15
		start_equipment_factor = 0.70
	}
	division = {
		name = "70 Bubing Shi"
		location = 4114
		division_template = "Juntuán"
		start_experience_factor = 0.15
		start_equipment_factor = 0.70
	}

	# Fu Zuoyi's Suiyuan force / 35th Army
	division = {
		name = "72 Bubing Shi"
		location = 9958
		division_template = "Juntuán"
		start_experience_factor = 0.20
		start_equipment_factor = 0.78
	}
	division = {
		name = "73 Bubing Shi"
		location = 9958
		division_template = "Juntuán"
		start_experience_factor = 0.20
		start_equipment_factor = 0.80
	}

	# Former Zheng-Tai railway guard, redesignated 101st Division in 1934
	division = {
		name = "101 Bubing Shi"
		location = 1069
		division_template = "Juntuán"
		start_experience_factor = 0.15
		start_equipment_factor = 0.70
	}

	# Independent infantry brigades
	division = {
		name = "1 Jinsui Duli Lu"
		location = 1069
		division_template = "Jinsui Duli Lu"
		start_experience_factor = 0.12
		start_equipment_factor = 0.65
	}
	division = {
		name = "2 Jinsui Duli Lu"
		location = 4114
		division_template = "Jinsui Duli Lu"
		start_experience_factor = 0.12
		start_equipment_factor = 0.65
	}
	division = {
		name = "3 Jinsui Duli Lu"
		location = 1069
		division_template = "Jinsui Duli Lu"
		start_experience_factor = 0.12
		start_equipment_factor = 0.65
	}

	# Cavalry Command - three brigades; the 1st/2nd cavalry divisions were only formed later in 1936.
	division = {
		name = "1 Jinsui Qibing Lu"
		location = 4114
		division_template = "Jinsui Qibing Lu"
		start_experience_factor = 0.15
		start_equipment_factor = 0.68
	}
	division = {
		name = "2 Jinsui Qibing Lu"
		location = 9958
		division_template = "Jinsui Qibing Lu"
		start_experience_factor = 0.15
		start_equipment_factor = 0.68
	}
	division = {
		name = "3 Jinsui Qibing Lu"
		location = 9958
		division_template = "Jinsui Qibing Lu"
		start_experience_factor = 0.15
		start_equipment_factor = 0.65
	}

'''

s = s[:start] + block + s[end:]
p.write_text('\ufeff' + s, encoding='utf-8')
clean = re.sub(r'#.*', '', s)
assert clean.count('{') == clean.count('}'), (clean.count('{'), clean.count('}'))
