import re
import sys

group = int(sys.argv[1])
data = input()

pattern = r'Temp:\s+(\d+\.\d+),\s+RH:\s+(\d+\.\d+)%'
regx = re.compile(pattern)
match = regx.search(data)

print(match.group(group))
