import youtube_dl
import os
import shutil
import requests
import urllib.parse
import json
mp3 = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],}
mp4 = {
		'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
		'videoformat' : "mp4",
			'postprocessors': [{
			'key': 'FFmpegVideoConvertor',
			'preferedformat': 'mkv'     
		}]}
class ytsearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self.search()

    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text
        while 'window["ytInitialData"]' not in response:
            response = requests.get(url).text
        results = self.parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def parse_html(self, response):
        results = []
        start = (
            response.index('window["ytInitialData"]')
            + len('window["ytInitialData"]')
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0) 
                res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                results.append(res)
        return results

    def to_dict(self):
        return self.videos

    def to_json(self):
        return json.dumps({"videos": self.videos})
class youtube_search:
	def search(self, search=None, type='url', result_num=1, max_results=1, raw_data=False, return_more_than_one=False, return_if_https=False):
		returnlist = []
		dicts = {}
		if search is None:
			raise AttributeError('Missing arguement: "search"')
		if isinstance(search, list):
			if type == 'url':
				for sresult in search:
					try:
						results = ytsearch(sresult, max_results=max_results).to_dict()
						convert = int(result_num) - 1
						number = results[convert]
					except IndexError:
						results = ytsearch(sresult, max_results=result_num).to_dict()
						convert = int(result_num) - 1
						number = results[convert]
					for item in results:
						suffix = item['url_suffix']
						url = "https://www.youtube.com" + suffix
						dicts[sresult] = url
				return dicts
			if type == 'title':
				for sresult in search:
					try:
						results = ytsearch(sresult, max_results=max_results).to_dict()
						convert = int(result_num) - 1
						number = results[convert]
					except IndexError:
						results = ytsearch(sresult, max_results=result_num).to_dict()
						convert = int(result_num) - 1
						number = results[convert]
					for item in results:
						title = item['title']
						dicts[sresult] = title
				return dicts
			if type == 'img':
				for sresult in search:
					try:
						results = ytsearch(sresult, max_results=max_results).to_dict()
						convert = int(result_num) - 1
						number = results[convert]
					except IndexError:
						results = ytsearch(sresult, max_results=result_num).to_dict()
						convert = int(result_num) - 1
						number = results[convert]
					for item in results:
						decide = number['thumbnails']
						img = decide[3]
						dicts[sresult] = img
				return dicts
		if return_if_https is False:
			if search.startswith("http://"):
				raise AttributeError(f'Search is not a valid search: "{search}" is already a search. To return the link, set the arguement "return_if_https" to True')
		if return_if_https is True:
			if search.startswith("http://"):
				return search
		try:
			results = ytsearch(search, max_results=max_results).to_dict()
			convert = int(result_num) - 1
			number = results[convert]
		except IndexError:
			results = ytsearch(search, max_results=result_num).to_dict()
			convert = int(result_num) - 1
			number = results[convert]
		if type == 'url':
			if return_more_than_one is False:
				url = "https://www.youtube.com" + number['url_suffix']
				return url
			elif return_more_than_one is True:
				results = ytsearch(search, max_results=max_results).to_dict()
				for item in results:
					suffix = item['url_suffix']
					url = "https://www.youtube.com" + suffix
					returnlist.append(url)
				return returnlist
		if type == 'title':
			if return_more_than_one is False:
				title = number['title']
				return title
			elif return_more_than_one is True:
				results = ytsearch(search, max_results=max_results).to_dict()
				for item in results:
					title = item['title']
					returnlist.append(title)
				return returnlist
		if type == 'img' or type == 'image':
			decide = number['thumbnails']
			img = decide[3]
			return img
		returnlist.clear
	def download(self, search=None, resultnumber=1, url=None, download_format='mp3', path='./'):
		convert = int(resultnumber) - 1
		if search.startswith("https://"):
			url = search
			title = 'song'
		else:
			results = ytsearch(search, max_results=resultnumber).to_dict()
			number = results[convert]
			url = "https://www.youtube.com" + number['url_suffix']
			title = number['title']
		if download_format == 'mp3':
			ydl_opts = mp3
		else:
			ydl_opts = mp4
		if path == './':
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
		else:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
				
		for file in os.listdir('./'):
			if file.endswith('.mp3'):
				try:
					os.rename(file, f"{title}.mp3")
					if path != './' and path.startswith("C:"):
						try:
							shutil.move(f"{title}.mp3", r"{}".format(path))
						except FileExistsError:
							os.remove(f"{title}.mp3")
							shutil.move(f"{title}.mp3", r"{}".format(path))
					elif path != './':
						try:
							shutil.move(f"{title}.mp3", path)
						except FileExistsError:
							os.remove(f"{title}.mp3")
							shutil.move(f"{title}.mp3", path)
				except FileExistsError:
					os.remove(f"{title}.mp3")
					os.rename(file, f"{title}.mp3")
					if path != './' and path.startswith("C:"):
						try:
							shutil.move(f"{title}.mp3", r"{}".format(path))
						except FileExistsError:
							os.remove(f"{title}.mp3")
							shutil.move(f"{title}.mp3", r"{}".format(path))
					elif path != './':
						try:
							shutil.move(f"{title}.mp3", path)
						except FileExistsError:
							os.remove(f"{title}.mp3")
							shutil.move(f"{title}.mp3", path)
			if file.endswith('.mkv'):
				try:
					os.rename(file, f"{title}.mp4")
				except FileExistsError:
					os.remove(f"{title}.mp4")
					os.rename(file, f"{title}.mp4")
				if path != './':
					try:
						shutil.move(f"{title}.mp4", path)
					except FileExistsError:
						os.remove(f"{title}.mp4")
						shutil.move(f"{title}.mp4", path)
