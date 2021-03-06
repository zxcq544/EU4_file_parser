import glob
import json
from pprint import pprint

import EU4FileParser

gfx_file_list = []
for file in glob.glob("./gfx files/*.gfx"):
    gfx_file_list.append(file)

print(gfx_file_list)

with open('achievements.gfx') as f:
    file_data = f.read()

# file_data = '''
# 	progressbartype = {
# 		name = "achievement_progress"
# 		color = { 0.0 0.5 0.0 }
# 		colortwo = { 1.0 0.0 0.0 }
# 		textureFile1 = "gfx//interface//modifier_progress_w72_h18_green.dds"
# 		textureFile2 = "gfx//interface//modifier_progress_w72_h18_red.dds"
# 		size = { x = 72 y = 18 }
# 		effectFile = "gfx//FX//progress.lua"
# 	}
# '''
example_string_to_tokenize = file_data
# tokens = EU4FileParser.tokenize(example_string_to_tokenize)
# for i in tokens:
#     print(i)
parser = EU4FileParser.EU4Parser()
result = parser.parse(example_string_to_tokenize)
pprint(result)

# now write output to a file
# out = open("achievements.json", "w")
# magic happens here to make it pretty-printed
# out.write(json.dumps(result, indent=4, sort_keys=True))
# out.close()
