from pathlib import Path
import re
p=Path('history/units/CHI_1936.txt')
s=p.read_text(encoding='utf-8-sig')

# Add regional templates before OOB.
marker='### OOB ###'
assert marker in s
extra=r'''
division_template = {
    name = "Guangxi Shi"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
        infantry = { x = 1 y = 1 }
        infantry = { x = 2 y = 0 }
        infantry = { x = 2 y = 1 }
        infantry = { x = 3 y = 0 }
        infantry = { x = 3 y = 1 }
    }
    support = { engineer = { x = 0 y = 0 } }
    priority = 1
}

division_template = {
    name = "Shandong Shi"
    division_names_group = CHI_INF_01
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
    name = "Shandong Shouqiang Lu"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
    }
    priority = 0
}

division_template = {
    name = "Chuanjun Shi"
    division_names_group = CHI_INF_01
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
    name = "Chuanjun Lu"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
    }
    priority = 0
}

division_template = {
    name = "Dianjun Lu"
    division_names_group = CHI_INF_01
    regiments = {
        infantry = { x = 0 y = 0 }
        infantry = { x = 0 y = 1 }
        infantry = { x = 1 y = 0 }
    }
    support = { engineer = { x = 0 y = 0 } }
    priority = 0
}

'''
s=s.replace(marker,extra+marker,1)

# Replace the late-war Shandong "Fifth War Area" abstraction with Han Fuju's provincial army.
start=s.index('\t##### Fifth War Area (CO: Li Zongren) #####')
end=s.index('\n}\n\n\n\n\ninstant_effect',start)
shandong=r'''	##### Shandong Provincial Army (CO: Han Fuju) #####
	# Five provincial divisions and Han's pistol brigade; same provincial core later formed his 3rd Army Group.
	division = {
		name = "20 Shandong Bubing Shi"
		location = 4205
		division_template = "Shandong Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.72
	}
	division = {
		name = "22 Shandong Bubing Shi"
		location = 4205
		division_template = "Shandong Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.72
	}
	division = {
		name = "81 Shandong Bubing Shi"
		location = 4205
		division_template = "Shandong Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.70
	}
	division = {
		name = "29 Shandong Bubing Shi"
		location = 10000
		division_template = "Shandong Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.70
	}
	division = {
		name = "74 Shandong Bubing Shi"
		location = 10000
		division_template = "Shandong Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.68
	}
	division = {
		name = "Han Fuju Shouqiang Lu"
		location = 4205
		division_template = "Shandong Shouqiang Lu"
		start_experience_factor = 0.20
		start_equipment_factor = 0.75
	}
	division = {
		name = "Qingdao Jingbei"
		location = 10000
		division_template = "Jingbei Lu"
		start_experience_factor = 0.10
		start_equipment_factor = 0.75
	}
'''
s=s[:start]+shandong+s[end:]

# Add Guangxi, Sichuan and Yunnan forces before Shandong block.
insert=s.index('\t##### Shandong Provincial Army (CO: Han Fuju) #####')
regional=r'''
	##### Guangxi Provincial Army (CO: Li Zongren / Bai Chongxi) #####
	# Pre-October 1936 New Guangxi regular divisions. Their later renumbering confirms the standing formation lineage.
'''
for n,loc,eq in [(19,1047,0.80),(21,1047,0.78),(24,1047,0.80),(43,7137,0.76),(44,7137,0.76),(45,7137,0.76)]:
    regional += f'''\tdivision = {{\n\t\tname = "{n} Guangxi Bubing Shi"\n\t\tlocation = {loc}\n\t\tdivision_template = "Guangxi Shi"\n\t\tstart_experience_factor = 0.22\n\t\tstart_equipment_factor = {eq:.2f}\n\t}}\n'''
regional += r'''

	##### Sichuan Provincial Forces (CO: Liu Xiang) #####
	# Only formations securely traceable through the October 1935 reorganization are instantiated here.
	division = {
		name = "1 Chuanjun Bubing Shi"
		location = 6999
		division_template = "Chuanjun Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.62
	}
	division = {
		name = "2 Chuanjun Bubing Shi"
		location = 6999
		division_template = "Chuanjun Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.62
	}
	division = {
		name = "4 Chuanjun Bubing Shi"
		location = 6999
		division_template = "Chuanjun Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.60
	}
	division = {
		name = "5 Chuanjun Bubing Shi"
		location = 4925
		division_template = "Chuanjun Shi"
		start_experience_factor = 0.15
		start_equipment_factor = 0.60
	}
	division = {
		name = "Chuanjun Jiaodao Shi"
		location = 4925
		division_template = "Chuanjun Shi"
		start_experience_factor = 0.20
		start_equipment_factor = 0.68
	}
	division = {
		name = "2 Chuanbian Lu"
		location = 4925
		division_template = "Chuanjun Lu"
		start_experience_factor = 0.12
		start_equipment_factor = 0.55
	}

	##### Yunnan Provincial Army (CO: Long Yun) #####
	# Long Yun had abolished powerful divisional commands after 1931; brigades were the basic standing formation.
	# Three brigades are documented operating in NE Yunnan in early 1935; six representative standing brigades preserve that brigade-based structure without inventing divisional numbers.
'''
for i,loc in enumerate([1319,1319,1319,1222,1222,1222],1):
    regional += f'''\tdivision = {{\n\t\tname = "Dianjun Duli Lu {i}"\n\t\tlocation = {loc}\n\t\tdivision_template = "Dianjun Lu"\n\t\tstart_experience_factor = 0.18\n\t\tstart_equipment_factor = 0.72\n\t}}\n'''
regional += '\n'
s=s[:insert]+regional+s[insert:]

p.write_text('\ufeff'+s,encoding='utf-8')
clean=re.sub(r'#.*','',s)
assert clean.count('{')==clean.count('}'),(clean.count('{'),clean.count('}'))
