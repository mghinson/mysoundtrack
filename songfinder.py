import rake
from gensim import models


temp = open("english_words.txt", 'r')
english_words = set(temp.read().split('\n'))
temp.close()


# texts: list, where each element is a full song/full fb post

def get_keywords(text, stop_words_path):
	rake_obj = rake.Rake(stop_words_path, 4, 1, 1)
	keyword_first_version = rake_obj.run(text)
	return [keyword for keyword in keyword_first_version if keyword in english_words]

class SongFinder(object):

	word2vec_model = None

	def __init__(self, stop_words_path, model, songs):

		self.model = model
		self.songs = songs
		word2vec_model = models.Word2Vec.load(model)
		self.stop_words_path = stop_words_path
		self.keywords_per_song = []

		for song in songs:
			song_file = open(song, 'r')
			self.keywords_per_song.append(get_keywords(song_file.read(), stop_words_path))
			song_file.close()

	def find_representative_song(self, fb_posts):

		# currently assuming fb_post text is sanitized. Should include some kind of sanitization code later

		fb_post_keywords = [get_keywords(fb_post, english_words) for fb_post in fb_posts]
		winner = -1
		max_score = -1
		index = 0

		for song_keywords in self.keywords_per_song:
			score = 0
			if len(song_keywords) == 0:
				continue
			try:
				for post_keywords in fb_post_keywords:
					if len(post_keywords) == 0:
						continue
					score += word2vec_model.n_similarity(song_keywords, post_keywords)
				if score > max_score:
					max_score = score
					winner = index
			except KeyError:
				print("d'oh!")
			index += 1

		if winner == -1:
			return None
		return songs[winner]

print("testing all imports are working")

posts = ["I love my friends", "I need someone to love", "Where is the party?"]

songs = ["song_lyrics/radioactive", "song_lyrics/hello", "song_lyrics/lean_on"]
sf = SongFinder("english_words.txt", "brown_word2vec_model", songs)
print(sf.find_representative_song(posts))



