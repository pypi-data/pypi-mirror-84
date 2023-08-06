import bs4

from mangamon.download import MangaDownloader
from mangamon.util import ProgressHook
from mangamon.constants import CONSTANTS

from typing import List
from pathlib import Path

import urllib.parse
import requests

class Manga(object):

	@staticmethod
	def search(search_query: str):

		url = "/".join([CONSTANTS.BASE_URL, "actions", "search", "?q="])
		url += search_query.replace(" ", "+")

		response = requests.get(url, verify=False, timeout=30)

		result_lines = [ line.split("|") for line in response.text.split("\n")]

		result = []

		for manga_result in result_lines:

			if len(manga_result) == 6:

				search_result = {}

				search_result["name"] = manga_result[0]
				search_result["sample_url"] = manga_result[1]
				search_result["alt_name"] = manga_result[2]
				search_result["artist"] = manga_result[3]
				search_result["route"] = manga_result[4]
				search_result["id"] = manga_result[5]

				result.append(search_result)
			
		return result

	def __init__(self, manga_name:str):
		
		self.manga_name = manga_name
		self.progress_hook = ProgressHook()
		self.downloder = MangaDownloader(self.progress_hook)


	def get_properties(self, soup: bs4.element.NavigableString):

		if not soup:
			url = "/".join([CONSTANTS.BASE_URL, self.manga_name])
			soup = self.downloder.get_page_soup(url)

		properties = {}
		proterties_table = soup.table

		tr = proterties_table.find_all("tr")

		for row in tr[:-3]:

			key = row.find_next("td")
			val = row.find_next("td").find_next_sibling("td")

			properties[key.text.strip()] = val.text.strip()

		return properties

	def get_latest_chapters(self, soup: bs4.element.NavigableString=None):

		if not soup:
			url = "/".join([CONSTANTS.BASE_URL, self.manga_name])
			soup = self.downloder.get_page_soup(url)

		latest_chapters_soup = soup.find_all(id="latestchapters")

		if len(latest_chapters_soup) == 0:
			raise ValueError("No chapters found")

		li = latest_chapters_soup[0].find_all("li")

		latest_chapters = []
		
		for chapter in li:

			chapter_str = chapter.text.strip()

			latest_chapters.append((
				chapter_str.split(":")[0].strip(),
				chapter_str.split(":")[1].strip()
			))

		return latest_chapters
		
	def get_all_chapters(self, soup: bs4.element.NavigableString=None):

		if not soup:
			url = "/".join([CONSTANTS.BASE_URL, self.manga_name])
			soup = self.downloder.get_page_soup(url)

		try:

			all_chapters = []

			rows = soup.find(id="listing")
			chapters = rows.find_all("td")

			for i in range(0, len(chapters), 2):

				chapter_number = chapters[i].text.split(":")[0].strip()
				chapter_name   = chapters[i].text.split(":")[1].strip()
				release_date   = chapters[i+1].text.strip()

				all_chapters.append((chapter_number, chapter_name, release_date))

			return all_chapters

		except AttributeError:
			raise ValueError("No td or listing found in soup")


	def get_summary(self, soup: bs4.element.NavigableString) -> str:

		if not soup:
			url = "/".join([CONSTANTS.BASE_URL, self.manga_name])
			soup = self.downloder.get_page_soup(url)

		readmangasum = soup.find_all(id='readmangasum')

		if len(readmangasum) == 0:
			return ""

		info = readmangasum[0].p

		return info.text.strip()


	def get_info(self):

		url = CONSTANTS.BASE_URL + "/" + self.manga_name
		soup = self.downloder.get_page_soup(url)

		properties = self.get_properties(soup)
		summary = self.get_summary(soup)
		latest_chapters = self.get_latest_chapters(soup)
		
		return {
			"properties": properties,
			"summary": summary,
			"latest_chapters": latest_chapters
		}


	def download(self, chapter_start: int, chapter_end: int, destination: Path):
		
		downloads = []

		for chapter in range(chapter_start, chapter_end+1):

			downloads.append(self.download_chapter(chapter, destination))

		return downloads


	def download_chapter(self, chapter:int, destination: Path) -> List[Path]:
		return self.downloder.download_chapter(self.manga_name, chapter, destination)
