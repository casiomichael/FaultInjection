import json
import xlrd

# class folder_manager():



class fault_injection_stats_utils():
	def is_data_line(self, line):
		return
	def is_other_line(self, line):
		return

	def get_data_objects_from_line(self, line):
		return

	def is_reg_lines(self, currL_ni, currL_wi):
		return currL_ni[0] == "r" and currL_wi[0] == "r"

	def parse_reg_line(self, line):
		regs = "".join(line.split()).split(",")
		rLeft = regs[0].split("=")
		rRight = regs[1].split("=")
		return rLeft, rRight

	def json_to_dict(self, prefix_json):
		with open(prefix_json) as json_file: 
			prefix_list = json.load(json_file)
			for item in prefix_list:
				self.stats_prefix_dic[item["prefix"]] = item["info_type"]

class regDiffer():
	regEqualCounter = 0
	regNEqualCounter = 0
	file_wi = ""
	file_ni = ""
	fi_stats_utils = None

	def __init__(self, with_injection_fp, no_injection_fp, fi_stats_utils):
		# Filepath for no injection data.
		self.file_ni = no_injection_fp
		# Filepath for with injection data
		self.file_wi = with_injection_fp
		# Instance of utils object that analyzes lines from the test files that we run. 
		self.fi_stats_utils = fi_stats_utils

	# Main Function that counts that number of registers that are different between the no injection file and the injection file. 
	def count_register_diff_number(self):
		f_ni = open(self.file_ni, "r")
		f_wi = open(self.file_wi, "r")
		w1 = open("reg_diff.txt","w+")
		currL_ni = f_ni.readline()
		currL_wi = f_wi.readline()

		while currL_ni and currL_wi:
			if (self.fi_stats_utils.is_reg_lines(currL_ni, currL_wi)):
				self.regEqualCounter += self.compare_reg_lines(currL_ni, currL_wi)
				self.regNEqualCounter += 2 - self.compare_reg_lines(currL_ni, currL_wi)
			currL_ni = f_ni.readline()
			currL_wi = f_wi.readline()
		print("Number of registers that are equal: ", self.regEqualCounter)
		print("Number of registers that are not equal: ", self.regNEqualCounter)

	def compare_reg_lines(self, line_ni, line_wi):
		regLeft_ni, regRight_ni = self.fi_stats_utils.parse_reg_line(line_ni)
		regLeft_wi, regRight_wi = self.fi_stats_utils.parse_reg_line(line_wi)
		regEqualCounter = 0
		if (regLeft_ni[0] != regLeft_wi[0]):
			print("Error: Misaligned register lines. What happened?")
			return;
		if (regLeft_ni[1] == regLeft_wi[1]):
			regEqualCounter += 1

		if (regRight_ni[1] == regRight_wi[1]):
			regEqualCounter += 1

		return regEqualCounter

fi_stats_utils_inst = fault_injection_stats_utils()
regDiffer_inst = regDiffer(with_injection_fp="inorder/flip_percentage_tests/05-000000100with_injection_19_15_43.txt", no_injection_fp="inorder/no_injection.txt", fi_stats_utils=fi_stats_utils_inst)
regDiffer_inst.count_register_diff_number()

