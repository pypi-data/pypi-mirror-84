""" Dowload manga endlessly """

import sys
import argparse
import requests
import logging
from pathlib import Path

from tabulate import tabulate

from .manga import Manga
from .post_processor import PostProcessor
from .util import wrap_text

logging.basicConfig(level=logging.INFO)

def main():

	argv = sys.argv

	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--name", help="manga name")
	parser.add_argument("-i", "--info", action="store_true", help="get information")
	parser.add_argument("-lt", "--latest", action="store_true", help="list latest chapters")
	parser.add_argument("-ll", "--longlist", action="store_true", help="list all chapters")

	parser.add_argument("-d", "--download", action="store_true", help="download manga")
	parser.add_argument("-c", "--chapter", type=int, help="chapters")
	parser.add_argument("--chapterstart", type=int, help="chapter start")
	parser.add_argument("--chapterend", type=int, help="chapter end")

	parser.add_argument("--format", type=str, help="convert to format [pdf]")

	parser.add_argument("-s", "--search", help="search manga")

	args = parser.parse_args(argv[1:])

	if len(sys.argv) == 1:
		parser.print_help(sys.stdout)
		exit()


	if args.name:

		manga = Manga(args.name)

		if args.latest:

			latest_chapters = manga.get_latest_chapters()
			print(tabulate(latest_chapters, headers=["Chapter", "Name"]))
			exit()

		if args.longlist:

			chapter_list = manga.get_all_chapters()
			print(tabulate(chapter_list, headers=["Chapter", "Name", "Date"]))
			exit()

		if args.info:
			info = manga.get_info()

			print()
			properties = [[key, info["properties"][key]] for key in info["properties"].keys() ]
			print(tabulate(properties, tablefmt="plain"))
			print()
			print("Summary:")
			print(wrap_text(info["summary"]))
			print()
			print("Latest Chapters")
			print(tabulate(info["latest_chapters"], tablefmt="plain"))
			exit()

		if args.download and ( args.chapter or (args.chapterstart and args.chapterend)):

			destination = Path(".")/args.name
			logging.info(destination)

			if args.chapter:
				downloads = manga.download_chapter(args.chapter, destination)
			else:
				downloads = manga.download(args.chapterstart, args.chapterend, destination)


			if args.format:

				if args.chapter or (args.chapterstart and args.chapterend):

					formatter = PostProcessor.getFormatter(args.format)
					save_as = str(args.chapter) if args.chapter else str(args.chapterstart) + "-" + str(args.chapterend)
					print("post processing started")

					if isinstance(downloads, list) and  isinstance(downloads[0], list):
						temp = []
						for sub_arr in downloads:
							temp += sub_arr

						downloads = temp

					formatter.convert(downloads, destination/save_as)

				else:
					parser.print_help(sys.stdout)

	if args.search:

		search_result = Manga.search(args.search)
		table = [(result["name"], result["artist"], result["route"][1:]) for result in search_result]
		print(tabulate(table, headers=["Title", "Artist", "Manga Name"]))
		
