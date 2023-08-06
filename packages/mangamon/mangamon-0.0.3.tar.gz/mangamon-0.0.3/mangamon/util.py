

class ProgressHook(object):

	def __init__(self):
		pass

	def update(self, iteration: int, total: int) -> None:

		length: int = 20
		filler: str = "="

		prefix: str = f"page {str(iteration)}/{str(total)}"
		suffix: str = f"downloading"

		percent: float = (iteration / float(total))*100
		filled: int = length * iteration // total

		if iteration == total:
			bars = filler * (filled - 1) + ' ' * (length - filled)
			suffix = "Download completed"
			print(f"\r{prefix} : [{bars}] {percent:.2f} % {suffix}")
		else:
			bars = filler * (filled - 1) + '>' + ' ' * (length - filled)
			print(f"\r{prefix} : [{bars}] {percent:.2f} % {suffix}", end='\r')


def wrap_text(p: str, width:int = 80):

	char_count = 0
	words = p.split(" ")
	wrapped_string = ""

	i = 0
	line_width = 0
	while i < len(words):

		if line_width + len(words[i]) < width:
			wrapped_string += words[i] + " "
		else:
			wrapped_string += "\n"
			line_width = 0

		line_width += len(words[i]) + 1

		i += 1

	return wrapped_string