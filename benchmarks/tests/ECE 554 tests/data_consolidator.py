import json
import xlrd
from os import listdir
from os.path import isfile, join
import copy

class folder_manager():
	is_ruu = False
	folder_fp = ""
	file_groups = {}
	file_split_substring = "with_injection"
	def __init__(self, folder_fp):
		self.folder_fp = folder_fp if folder_fp[-1] == "/" else folder_fp + "/"
		if ("ruu" in folder_fp):
			self.is_ruu = True
		self.group_files_by_type()

	def group_files_by_type(self):
		onlyfiles = [f for f in listdir(self.folder_fp) if isfile(join(self.folder_fp, f))]
		for file in onlyfiles: 
			prefix = file.split(self.file_split_substring)[0]
			suffix = self.file_split_substring + file.split(self.file_split_substring)[1]
			if (self.is_ruu):
				prefix = prefix + suffix[-10:-4]
			l = []
			if prefix in self.file_groups.keys():
				l = self.file_groups[prefix]
			l.append(suffix)
			self.file_groups[prefix] = l

	def avg_all_stats(self):

		for index, prefix in enumerate(self.file_groups.keys()):
			if index == 0:
				# Initialize Excel Sheet
			else:
				# Add Values to it. 
			avged_stats = self.avg_stats_in_group(prefix)



	def avg_stats_in_group(self, prefix):
		total_stats = {}
		count = 0
		currGroup = self.file_groups[prefix]
		for file_suffix in currGroup:
			currFileStats = self.getFileStats(prefix, file_suffix)
			if (count == 0):
				total_stats = copy.deepcopy(currFileStats)
			else:
				for key in currFileStats.keys():
					total_stats[key] = currFileStats[key] + total_stats[key]
			count+=1
		for key in total_stats.keys():
			total_stats[key] = round(total_stats[key]/count,2)
		# print("")
		# print("###################")
		# print(prefix)
		# dict_utils(total_stats).print_dict() # Debugging print statement
		# print("###################")
		return total_stats

	def reconstruct_filepath(self, prefix, suffix, is_ruu):
		return self.folder_fp + prefix[:-6] + suffix if is_ruu else self.folder_fp + prefix + suffix

	def getFileStats(self, prefix, file_suffix):
		wi_fp = self.reconstruct_filepath(prefix, file_suffix, self.is_ruu)
		ni_fp = self.folder_fp.split("/")[0] + "/no_injection.txt"
		fi_stats_utils_inst = fault_injection_stats_utils()
		fault_injection_stats_inst = fault_injection_stats(with_injection_fp=wi_fp, no_injection_fp=ni_fp, fi_stats_utils=fi_stats_utils_inst)
		res = fault_injection_stats_inst.get_stats()
		return res	



class fault_injection_stats_utils():
	def is_data_line(self, line):
		return ":" in line

	def get_data_objects_from_line(self, line):
		data_obj = line.split(":")
		key = data_obj[0]
		value = round(float("".join(data_obj[1].split())),2)
		return key, value

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

class fault_injection_stats():
	regEqualCounter = 0
	regNEqualCounter = 0
	file_wi = ""
	file_ni = ""
	fi_stats_utils = None
	stats = {}

	def __init__(self, with_injection_fp, no_injection_fp, fi_stats_utils):
		# Filepath for no injection data.
		self.file_ni = no_injection_fp
		# Filepath for with injection data
		self.file_wi = with_injection_fp
		# Instance of utils object that analyzes lines from the test files that we run. 
		self.fi_stats_utils = fi_stats_utils

	# Main Function that counts that number of registers that are different between the no injection file and the injection file. 
	def get_stats(self):
		f_ni = open(self.file_ni, "r")
		f_wi = open(self.file_wi, "r")
		currL_ni = f_ni.readline()
		currL_wi = f_wi.readline()
		while currL_ni and currL_wi:
			if (self.fi_stats_utils.is_data_line(currL_wi)):
				key, value = self.fi_stats_utils.get_data_objects_from_line(currL_wi)
				self.stats[key] = value

			if (self.fi_stats_utils.is_reg_lines(currL_ni, currL_wi)):
				self.regEqualCounter += self.compare_reg_lines(currL_ni, currL_wi)
				self.regNEqualCounter += 2 - self.compare_reg_lines(currL_ni, currL_wi)
			currL_ni = f_ni.readline()
			currL_wi = f_wi.readline()
		self.stats["# Equal Registers"] = round(float(self.regEqualCounter),2)
		self.stats["# UnEqual Registers"] = round(float(self.regNEqualCounter),2)
		return self.stats

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

class dict_utils():
	d = {}
	def __init__(self, d):
		self.d = d

	def print_dict(self):
		for keys,values in self.d.items():
			print(keys + " " + str(values))

fm = folder_manager("inorder/flip_percentage_tests")
fm.avg_all_stats()




