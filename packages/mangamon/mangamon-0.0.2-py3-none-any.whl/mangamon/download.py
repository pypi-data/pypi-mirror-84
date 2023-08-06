import sys
import os
import shutil
import errno
from pathlib import Path
from typing import List

from mangamon.constants import CONSTANTS

import bs4
import logging
import img2pdf
import requests

import urllib3
urllib3.disable_warnings()

from mangamon.util import ProgressHook

class MangaDownloader(object):

	def __init__(self, progress_hook = None):
		self.progress_hook = progress_hook

	def update_progress(self, iteration, total):
		""" update progress hook """
		if not self.progress_hook:
			return 

		self.progress_hook.update(iteration, total)


	def get_page_soup(self, url: str) -> bs4.element.NavigableString:
		""" Returns the BeautifulSoup for the page"""

		result = requests.get(url, verify=False, timeout=30)

		if result.status_code == 404:
			raise requests.exceptions.HTTPError		

		doc = result.text
		bs = bs4.BeautifulSoup

		return bs(doc, "html.parser")


	def get_page_count(self, soup: bs4.element.NavigableString) -> int:
		""" Returns total no. of pages in the chapter """

		if not soup:
			raise ValueError("Empty Soup passed to get page count")

		final_option = [ item for item in soup.find_all("option") ][-1]
		return int(final_option.text)


	def save_image(self, soup: bs4.element.NavigableString, chapter: int, page: int, destination: Path) -> Path:
		""" downloads and saves the img to destination and returns the saved path """

		if not soup:
			raise ValueError("Empty Soup passed to save image")

		if chapter <= 0:
			raise ValueError("Invalid Chapter passed as an argument :", chapter)

		if page <= 0:
			raise ValueError("Invalid Page passed as an argument :", page)

		if not destination.exists():
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), destination)

		if not destination.is_dir():
			raise ValueError("Destination is not a directory :", str(destination))

		images = soup.find_all(id="img")

		if len(images) != 1:
			raise Exception("Page contains no or multiple image")

		image_url = images[0].get("src")
		image_path = f"{str(chapter)}__{str(page)}.jpg"

		response = requests.get(image_url, verify=False, timeout=30)

		if response.status_code == 404:
			raise requests.exceptions.HTTPError

		with open(destination/image_path, "wb") as f:
			f.write(response.content)

		return image_path



	def download_chapter(self, manga_name: int, chapter: int, destination: Path) -> List[str]:
		""" 
			downloads the chapter into destination 
			returns list of file paths
		"""

		if type(chapter) != int or chapter <= 0:
			raise ValueError("chapter should be an int > 0")

		if type(manga_name) != str or manga_name.strip() == "":
			raise ValueError("maga_name should be a str")		

		if not destination.exists():
			os.mkdir(destination)

		if not destination.is_dir():
			raise FileNotFoundError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), destination)

		image_names: List[str] = []
		total_pages: int = 0
		page: int = 1

		url = "/".join([CONSTANTS.BASE_URL, manga_name, str(chapter), str(page)])

		soup: bs4.element.NavigableString = self.get_page_soup(url)
		total_pages = self.get_page_count(soup)

		image_name = self.save_image(soup, chapter, page, destination)
		image_names.append(image_name)

		page += 1
		self.update_progress(page, total_pages)

		while page <= total_pages:

			try:

				url = "/".join([CONSTANTS.BASE_URL, manga_name, str(chapter), str(page)])
				soup = self.get_page_soup(url)
				image_name = self.save_image(soup, chapter, page, destination)
				image_names.append(image_name)

			except requests.exceptions.HTTPError as e:
				print(e)
				continue
			except requests.exceptions.ConnectionError as e:
				print(e)
				continue
			except ConnectionResetError as e:
				print(e)
				continue
			except requests.exceptions.ReadTimeout as e:
				print(e)
				continue
			except urllib3.exceptions.ProtocolError as e:
				print(e)
				continue

			self.update_progress(page, total_pages)
			page += 1

		return [ str(destination/image_name) for image_name in image_names ]
