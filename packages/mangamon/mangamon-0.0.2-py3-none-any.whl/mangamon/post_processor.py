import os
from pathlib import Path

class PostProcessor():

	@staticmethod
	def getFormatter(format:str):

		if format.upper() == "PDF":
			return PDF


class PDF():

	@staticmethod
	def convert(paths, destination_path, clean=True):

		import img2pdf

		print("")

		with open(str(destination_path) + ".pdf", "wb") as output_file:
			output_file.write(img2pdf.convert(paths))

		print("successfully converted to pdf")

		if clean:

			for file in paths:
				os.remove(file)
