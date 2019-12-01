import json

class fault_injection_stats():
	stats_prefix_dic = {}
	file_ni = ""
	file_wi = ""
	currentCycle = 0
	regEqualCounter = 0
	tempCounter = 0

	def __init__(self, prefix_json, file_ni, file_wi):
		self.json_to_dict(prefix_json)
		self.file_ni = file_ni
		self.file_wi = file_wi

	def json_to_dict(self, prefix_json):
		with open(prefix_json) as json_file: 
			prefix_list = json.load(json_file)
			for item in prefix_list:
				self.stats_prefix_dic[item["prefix"]] = item["info_type"]
			# dict_utils(self.stats_prefix_dic).print_dict() # Debugging print statement

	def main_reg_line_comparator(self):
		f_ni = open(self.file_ni, "r")
		f_wi = open(self.file_wi, "r")
		w1 = open("reg_diff.txt","w+")
		currL_ni = f_ni.readline()
		currL_wi = f_wi.readline()

		# TODO Change Back
		# while currL_ni and currL_wi:
		for i in range(10000):
			self.updateCycleCount(currL_ni)
			if (self.is_reg_lines(currL_ni, currL_wi)):
				self.compare_reg_lines(currL_ni, currL_wi)
			currL_ni = f_ni.readline()
			currL_wi = f_wi.readline()
		print("Number of registers that are equal: ", self.regEqualCounter)
	
	def updateCycleCount(self, line):
		cycleCountPrefix = "THIS IS THE REGISTER FILE FOR WITH INJECTION AT CYCLE "
		if (line.startswith(cycleCountPrefix)):
			self.currentCycle = int(line.lstrip(cycleCountPrefix))

	def compare_reg_lines(self, line_ni, line_wi):
		regLeft_ni, regRight_ni = self.parse_reg_line(line_ni)
		regLeft_wi, regRight_wi = self.parse_reg_line(line_wi)
		if (regLeft_ni[0] != regLeft_wi[0]):
			print("Error: Misaligned register lines. What happened?")
			return;
		if (regLeft_ni[1] != regLeft_wi[1]):
			# TODO: Write to file
			print('Current Cycle: {:>12} {:>12} {:>12} {:>12}  '.format(str(self.currentCycle), regLeft_ni[0], regLeft_ni[1], regLeft_wi[1]))
		if (regRight_ni[1] != regRight_wi[1]):
			# TODO: Write to file
			print('Current Cycle: {:>12} {:>12} {:>12} {:>12}  '.format(str(self.currentCycle), regRight_ni[0], regRight_ni[1], regRight_wi[1]))
		self.tempCounter += 1;
		if (regLeft_ni[1] == regLeft_wi[1] and regRight_ni[1] == regRight_wi[1]):
			self.regEqualCounter += 1

	def is_reg_lines(self, currL_ni, currL_wi):
		if currL_ni[0] in self.stats_prefix_dic.keys():
				lineType_ni = self.stats_prefix_dic[currL_ni[0]]
				lineType_wi = self.stats_prefix_dic[currL_wi[0]]
				return (lineType_wi == lineType_ni and lineType_wi == "reg_data")

	def parse_reg_line(self, line):
		regs = "".join(line.split()).split(",")
		rLeft = regs[0].split("=")
		rRight = regs[1].split("=")
		return rLeft, rRight

class dict_utils():
	d = {}
	def __init__(self, d):
		self.d = d

	def print_dict(self):
		for keys,values in self.d.items():
			print(keys + " " + values)

		
# x = fault_injection_stats("prefix_map.json", "ni.txt", "wi.txt")
x = fault_injection_stats("prefix_map.json", "with_injection_19_01_59.txt", "no_injection_19_01_54.txt")

x.main_reg_line_comparator()

