from pathlib import Path
import re

p = Path('history/units/ITA_1936_nsb.txt')
s = p.read_text(encoding='utf-8-sig')

start = s.index('division_template = { #Blackshirts')
end = s.index('division_template = { \n\tname = "Divisione Celere"', start)
blackshirts = '''division_template = { # Blackshirts: standard Ethiopia division, 3 legions x 2 battalions
\tname = "Camicie Nere"
\tdivision_names_group = ITA_INF_02
\tregiments = {
\t\tmilitia = { x = 0 y = 0 }
\t\tmilitia = { x = 0 y = 1 }
\t\tmilitia = { x = 1 y = 0 }
\t\tmilitia = { x = 1 y = 1 }
\t\tmilitia = { x = 2 y = 0 }
\t\tmilitia = { x = 2 y = 1 }
\t\tartillery_brigade = { x = 4 y = 0 }
\t}
\tregimental_support = {
\t\tartillery = { x = 0 y = 0 }
\t\tartillery = { x = 1 y = 0 }
\t\tartillery = { x = 2 y = 0 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t\tsignal_company = { x = 0 y = 1 }
\t}
}

division_template = { # 6th CC.NN. Division: four legions
\tname = "Camicie Nere Tevere"
\tdivision_names_group = ITA_INF_02
\tregiments = {
\t\tmilitia = { x = 0 y = 0 }
\t\tmilitia = { x = 0 y = 1 }
\t\tmilitia = { x = 1 y = 0 }
\t\tmilitia = { x = 1 y = 1 }
\t\tmilitia = { x = 2 y = 0 }
\t\tmilitia = { x = 2 y = 1 }
\t\tmilitia = { x = 3 y = 0 }
\t\tmilitia = { x = 3 y = 1 }
\t\tartillery_brigade = { x = 4 y = 0 }
\t}
\tregimental_support = {
\t\tartillery = { x = 0 y = 0 }
\t\tartillery = { x = 1 y = 0 }
\t\tartillery = { x = 2 y = 0 }
\t\tartillery = { x = 3 y = 0 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t\tsignal_company = { x = 0 y = 1 }
\t\tlogistics_company = { x = 0 y = 2 }
\t}
}

division_template = { # 7th CC.NN. Division: eight legions, reserve in Libya
\tname = "Camicie Nere Cirene"
\tdivision_names_group = ITA_INF_02
\tregiments = {
\t\tmilitia = { x = 0 y = 0 }
\t\tmilitia = { x = 0 y = 1 }
\t\tmilitia = { x = 0 y = 2 }
\t\tmilitia = { x = 0 y = 3 }
\t\tmilitia = { x = 1 y = 0 }
\t\tmilitia = { x = 1 y = 1 }
\t\tmilitia = { x = 1 y = 2 }
\t\tmilitia = { x = 1 y = 3 }
\t\tmilitia = { x = 2 y = 0 }
\t\tmilitia = { x = 2 y = 1 }
\t\tmilitia = { x = 2 y = 2 }
\t\tmilitia = { x = 2 y = 3 }
\t\tmilitia = { x = 3 y = 0 }
\t\tmilitia = { x = 3 y = 1 }
\t\tmilitia = { x = 3 y = 2 }
\t\tmilitia = { x = 3 y = 3 }
\t\tartillery_brigade = { x = 4 y = 0 }
\t\tartillery_brigade = { x = 4 y = 1 }
\t}
\tregimental_support = {
\t\tartillery = { x = 0 y = 0 }
\t\tartillery = { x = 1 y = 0 }
\t\tartillery = { x = 2 y = 0 }
\t\tartillery = { x = 3 y = 0 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t\tsignal_company = { x = 0 y = 1 }
\t}
}

'''
s = s[:start] + blackshirts + s[end:]

cstart = s.index('#############################\n###### ASCARI INFANTRY ######')
cend = s.index('###################\n#### IRREGULARS ###', cstart)
colonial = '''#############################
###### ASCARI INFANTRY ######
#############################

division_template = {
\tname = "Divisione Coloniale"
\tdivision_names_group = ITA_COL_01
\toverride_model = ITA_infantry_alt_1_entity
\ttemplate_counter = 67
\tregiments = {
\t\tinfantry = { x = 0 y = 0 }
\t\tinfantry = { x = 0 y = 1 }
\t\tinfantry = { x = 1 y = 0 }
\t\tinfantry = { x = 1 y = 1 }
\t}
\tpriority = 0
}

# 1st/2nd Eritrean divisions: ten native battalions and two mountain-artillery battalions.
division_template = {
\tname = "Divisione Ascari Eritrea"
\tdivision_names_group = ITA_COL_01
\toverride_model = ITA_infantry_alt_1_entity
\tregiments = {
\t\tinfantry = { x = 0 y = 0 }
\t\tinfantry = { x = 0 y = 1 }
\t\tinfantry = { x = 0 y = 2 }
\t\tinfantry = { x = 1 y = 0 }
\t\tinfantry = { x = 1 y = 1 }
\t\tinfantry = { x = 2 y = 0 }
\t\tinfantry = { x = 2 y = 1 }
\t\tinfantry = { x = 3 y = 0 }
\t\tinfantry = { x = 3 y = 1 }
\t\tinfantry = { x = 3 y = 2 }
\t\tartillery_brigade = { x = 4 y = 0 }
\t\tartillery_brigade = { x = 4 y = 1 }
\t}
\tsupport = { engineer = { x = 0 y = 0 } }
\tpriority = 1
}

# Divisione Libia: 3 x two-battalion Libyan regiments + X battalion + artillery regiment.
division_template = {
\tname = "Divisione Ascari Libica"
\tdivision_names_group = ITA_COL_01
\toverride_model = ITA_infantry_alt_2_entity
\tregiments = {
\t\tinfantry = { x = 0 y = 0 }
\t\tinfantry = { x = 0 y = 1 }
\t\tinfantry = { x = 1 y = 0 }
\t\tinfantry = { x = 1 y = 1 }
\t\tinfantry = { x = 2 y = 0 }
\t\tinfantry = { x = 2 y = 1 }
\t\tinfantry = { x = 3 y = 0 }
\t\tartillery_brigade = { x = 4 y = 0 }
\t\tartillery_brigade = { x = 4 y = 1 }
\t}
\tsupport = { engineer = { x = 0 y = 0 } }
\tpriority = 1
}

# Corpo Indigeni Somali: six regular Arab-Somali battalions and corps artillery.
division_template = {
\tname = "Corpo Indigeni Somali"
\tdivision_names_group = ITA_COL_01
\toverride_model = ITA_infantry_alt_3_entity
\tregiments = {
\t\tinfantry = { x = 0 y = 0 }
\t\tinfantry = { x = 0 y = 1 }
\t\tinfantry = { x = 0 y = 2 }
\t\tinfantry = { x = 1 y = 0 }
\t\tinfantry = { x = 1 y = 1 }
\t\tinfantry = { x = 1 y = 2 }
\t\tartillery_brigade = { x = 4 y = 0 }
\t}
\tsupport = { engineer = { x = 0 y = 0 } }
\tpriority = 0
}

'''
s = s[:cstart] + colonial + s[cend:]

irr_start = s.index('###################\n#### IRREGULARS ###')
irr_end = s.index('####### OOB #######', irr_start)
irregular = '''###################
#### IRREGULARS ###
###################

division_template = {
\tname = "Banda Indigena Irregolare"
\tdivision_names_group = ITA_COL_02
\toverride_model = ITA_irregular_infantry_alt_1_entity
\tregiments = { irregular_infantry = { x = 0 y = 0 } }
\tpriority = 0
}

division_template = {
\tname = "Truppe Irregolari a Cavallo"
\tdivision_names_group = ITA_CAV_05
\toverride_model = ITA_cavalry_alt_3_entity
\tregiments = { cavalry = { x = 0 y = 0 } }
\tpriority = 0
}

division_template = {
\tname = "Banda Irregolare Libica"
\tdivision_names_group = ITA_COL_02
\toverride_model = ITA_irregular_infantry_alt_0_entity
\tregiments = { irregular_infantry = { x = 0 y = 0 } }
\tpriority = 0
}

division_template = {
\tname = "Banda Irregolare Eritrea"
\tdivision_names_group = ITA_COL_02
\toverride_model = ITA_irregular_infantry_alt_1_entity
\tregiments = { irregular_infantry = { x = 0 y = 0 } }
\tpriority = 0
}

division_template = {
\tname = "Banda Irregolare Somala"
\tdivision_names_group = ITA_COL_03
\toverride_model = ITA_irregular_infantry_alt_3_entity
\tregiments = {
\t\tirregular_infantry = { x = 0 y = 0 }
\t\tirregular_infantry = { x = 0 y = 1 }
\t}
\tpriority = 0
}

'''
s = s[:irr_start] + irregular + s[irr_end:]

s = s.replace('division_template = "Camicie Nere"\t# CC.NN. militia, lower training and equipment \n\t\tstart_equipment_factor = 0.2',
              'division_template = "Camicie Nere Cirene"\t# Eight-legion reserve division\n\t\tstart_experience_factor = 0.15\n\t\tstart_equipment_factor = 0.55', 1)

s = re.sub(r'\n\tdivision = \{ # \n\t\tdivision_name = \{\n\t\t\tis_name_ordered = yes\n\t\t\tname_order = 2\n\t\t\}#  "2a Divisione Fanteria Coloniale Libica".*?\n\t\}', '', s, count=1, flags=re.S)

s = s.replace('division_template = "Divisione Ascari Eritrea" # Colonial militia, lower training and equipment\n\t\tforce_equipment_variants = { infantry_equipment_0 = { owner = "ITA" }}',
              'division_template = "Divisione Ascari Eritrea" # Regular Eritrean askari formation\n\t\tstart_experience_factor = 0.30\n\t\tstart_equipment_factor = 0.90\n\t\tforce_equipment_variants = { infantry_equipment_0 = { owner = "ITA" }}')

s = s.replace('}#  "1a Divisione Fanteria Coloniale Libica" \n\t\tlocation = 8164 \n\t\tdivision_template = "Divisione Ascari Libica" # Colonial militia, lower training and equipment\n\t\tforce_equipment_variants = { infantry_equipment_0 = { owner = "ITA" }}',
              '}#  "Divisione Fanteria Libia"\n\t\tlocation = 8164\n\t\tdivision_template = "Divisione Ascari Libica" # Nasi\'s Libyan Division on the Somali front\n\t\tstart_experience_factor = 0.25\n\t\tstart_equipment_factor = 0.85\n\t\tforce_equipment_variants = { infantry_equipment_0 = { owner = "ITA" }}')

s = s.replace('name = "Divisione F. Coloniale Arabo-Somala"', 'name = "Corpo Indigeni Somali"')
s = s.replace('division_template = "Divisione Ascari Somala" # Colonial militia, lower training and equipment\n\t\tforce_equipment_variants = { infantry_equipment_0 = { owner = "ITA" }}',
              'division_template = "Corpo Indigeni Somali" # Six regular Arab-Somali battalions\n\t\tstart_experience_factor = 0.25\n\t\tstart_equipment_factor = 0.80\n\t\tforce_equipment_variants = { infantry_equipment_0 = { owner = "ITA" }}')

s = s.replace('division_template = "Camicie Nere"\t# CC.NN. militia, lower training and equipment\n\t\tstart_experience_factor = 0.10',
              'division_template = "Camicie Nere Tevere"\t# Four-legion mixed volunteer division\n\t\tstart_experience_factor = 0.10\n\t\tstart_equipment_factor = 0.75', 1)

dubat = re.compile(r'(\n\tdivision = \{ #Somlia Dubats \(Somali Irregular Infantry\).*?\n\t\})\n\n\tdivision = \{ #Somlia Dubats \(Somali Irregular Infantry\).*?\n\t\}', re.S)
s, n = dubat.subn(r'\1', s, count=1)
assert n == 1, 'duplicate Somali Dubat block not found'

clean = re.sub(r'#.*', '', s)
assert clean.count('{') == clean.count('}'), (clean.count('{'), clean.count('}'))
p.write_text('\ufeff' + s, encoding='utf-8')
