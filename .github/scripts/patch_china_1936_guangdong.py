from pathlib import Path
import re

p = Path('history/units/CHI_1936.txt')
s = p.read_text(encoding='utf-8-sig')

# Add Guangdong-specific formation templates before OOB.
marker = '### OOB ###'
assert marker in s

templates = r'''
division_template = {
    name = "Guangdong Shi"
    division_names_group = CHI_INF_01
    # Chen Jitang First Group Army field division, 1932-36 structure.
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
    }
    support = {
        engineer = { x = 0 y = 0 }
        signal_company = { x = 0 y = 1 }
    }
    priority = 1
}

division_template = {
    name = "Guangdong Duli Lu"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
    }
    priority = 0
}

division_template = {
    name = "Guangdong Duli Tuan"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
    }
    priority = 0
}

'''
s = s.replace(marker, templates + marker, 1)

# Insert Chen Jitang's First Group Army before the existing Beiping-Tianjin grouping.
insert_marker = '\t##### Beiping-Tianjin Area (CO: ) #####'
assert insert_marker in s

guangdong = r'''
	##### Guangdong First Group Army (CO: Chen Jitang) #####
	# The establishment created in 1931-32 remained broadly intact until Chen's fall in July 1936.
	# 1st Army (Yu Hanmou)
	division = {
		name = "1 Guangdong Shi"
		location = 1162
		division_template = "Guangdong Shi"
		start_experience_factor = 0.20
		start_equipment_factor = 0.78
	}
	division = {
		name = "2 Guangdong Shi"
		location = 1162
		division_template = "Guangdong Shi"
		start_experience_factor = 0.20
		start_equipment_factor = 0.78
	}

	# 2nd Army (Xiang Hanping)
	division = {
		name = "4 Guangdong Shi"
		location = 1202
		division_template = "Guangdong Shi"
		start_experience_factor = 0.18
		start_equipment_factor = 0.75
	}
	division = {
		name = "5 Guangdong Shi"
		location = 1202
		division_template = "Guangdong Shi"
		start_experience_factor = 0.18
		start_equipment_factor = 0.75
	}

	# 3rd Army (Li Yangjing)
	division = {
		name = "7 Guangdong Shi"
		location = 9938
		division_template = "Guangdong Shi"
		start_experience_factor = 0.18
		start_equipment_factor = 0.75
	}
	division = {
		name = "8 Guangdong Shi"
		location = 9938
		division_template = "Guangdong Shi"
		start_experience_factor = 0.18
		start_equipment_factor = 0.75
	}

	# Independent and training divisions
	division = {
		name = "1 Guangdong Duli Shi"
		location = 1162
		division_template = "Guangdong Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.70
	}
	division = {
		name = "2 Guangdong Duli Shi"
		location = 1202
		division_template = "Guangdong Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.70
	}
	division = {
		name = "Guangdong Peixun Shi"
		location = 1162
		division_template = "Guangdong Shi"
		start_experience_factor = 0.20
		start_equipment_factor = 0.72
	}

	# Independent Guards Brigade and four independent brigades
	division = {
		name = "Guangdong Jingwei Lu"
		location = 1162
		division_template = "Guangdong Duli Lu"
		start_experience_factor = 0.20
		start_equipment_factor = 0.75
	}
	division = {
		name = "1 Guangdong Duli Lu"
		location = 1162
		division_template = "Guangdong Duli Lu"
		start_experience_factor = 0.15
		start_equipment_factor = 0.68
	}
	division = {
		name = "2 Guangdong Duli Lu"
		location = 1202
		division_template = "Guangdong Duli Lu"
		start_experience_factor = 0.15
		start_equipment_factor = 0.68
	}
	division = {
		name = "3 Guangdong Duli Lu"
		location = 9938
		division_template = "Guangdong Duli Lu"
		start_experience_factor = 0.15
		start_equipment_factor = 0.65
	}
	division = {
		name = "4 Guangdong Duli Lu"
		location = 9938
		division_template = "Guangdong Duli Lu"
		start_experience_factor = 0.15
		start_equipment_factor = 0.65
	}

	# Eight independent regiments were part of the permanent establishment.
'''
for i, loc in enumerate([1162,1162,1202,1202,9938,9938,1202,1162], start=1):
    guangdong += f'''\tdivision = {{\n\t\tname = "{i} Guangdong Duli Tuan"\n\t\tlocation = {loc}\n\t\tdivision_template = "Guangdong Duli Tuan"\n\t\tstart_experience_factor = 0.12\n\t\tstart_equipment_factor = 0.62\n\t}}\n'''
guangdong += '\n'

s = s.replace(insert_marker, guangdong + insert_marker, 1)

p.write_text('\ufeff' + s, encoding='utf-8')
clean = re.sub(r'#.*', '', s)
assert clean.count('{') == clean.count('}'), (clean.count('{'), clean.count('}'))
