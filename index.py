# -*- encoding: utf-8 -*-
# 
import os, random
import argparse

# на уровень выше расположения файла
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

import nltk
from nltk.corpus import stopwords
import pymorphy3, data

morph = pymorphy3.MorphAnalyzer()
russian_stopwords = stopwords.words("russian")
from string import punctuation


# функция очистки слов и лемматизации текста
# antispam
def preprocess_text(text):
	words = text.lower().split()
	
	# очистка от прилегающего к слову мусора из пунктуации (слово, -> слово / "или так" -> или так / круто!! -> круто)
	clear_words = []
	for word in words:
		clear_word = ""
		for s in word:
			if not s in punctuation:
				clear_word = clear_word + s
		clear_words.append(clear_word)
	
	# лемматизация, бомбу -> бомба 
	tokens = [morph.parse(token)[0].normal_form for token in clear_words if token not in russian_stopwords\
			and token != " " \
			and token.strip() not in punctuation]

	text = " ".join(tokens)
	
	if len(tokens) > 0:
		token = tokens[0]
	else:
		token = ""
	return token



# символы, которые считаем пунктуацией
split_simbols_list = []
split_simbols = ".,!?;-"
for simbol in split_simbols:
	split_simbols_list.append(simbol)



# https://habr.com/ru/articles/763542/
# python -m spacy download ru_core_news_sm  


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--text', type=str, default='Добрый день, я, Якушенко Павел. Мой адрес - г.Новозыбков, ул.Кубановская, 55', help='Текст для деперсонализации')

	args = parser.parse_args()
	# разбиваем предложение на слова. 
	words = args.text.split()


	out_text = ""
	n = 0
	is_m = False
	for word in words:
		current_word = word
		
		# приводим слово в нормальную форму
		token = preprocess_text(word)
		if len(token) > 0:
			# мужское имя ru
			lower_list = [preprocess_text(i) for i in str(data.ru_names_m).split(" ")]
			# меняем на орка
			change_list = [str(i).replace(",", "" ) for i in str(data.ork_names_m).split(" ")]
			if (token in lower_list):
				current_word = random.choice(change_list)
			
			# женское имя ru
			lower_list = [preprocess_text(i) for i in str(data.ru_names_f).split(" ")]
			# меняем на орка
			change_list = [str(i).replace(",", "" ) for i in str(data.ork_names_f).split(" ")]
			if (token in lower_list):
				current_word = random.choice(change_list)
				is_m = True

			# фамилия ru
			lower_list = [preprocess_text(i) for i in str(data.ru_fam).split(" ")]
			# меняем на орка
			change_list = [str(i).replace(",", "" ) for i in str(data.ork_fam).split(" ")]
			if (token in lower_list):
				current_word = random.choice(change_list)
				if is_m:
					current_word = current_word + "а"


			# мужское имя ukr
			lower_list = [preprocess_text(i) for i in str(data.ukr_names_m).split(" ")]
			# меняем на эльфа
			change_list = [str(i).replace(",", "" ) for i in str(data.elf_names_m).split(" ")]
			if (token in lower_list):
				current_word = random.choice(change_list)

			# женское имя ukr
			lower_list = [preprocess_text(i) for i in str(data.ukr_names_f).split(" ")]
			# меняем на эльфа
			change_list = [str(i).replace(",", "" ) for i in str(data.elf_names_f).split(" ")]
			if (token in lower_list):
				current_word = random.choice(change_list)

			# фамилия ukr
			lower_list = [preprocess_text(i) for i in str(data.ukr_fam).split(" ")]
			# меняем на эльфа
			change_list = [str(i).replace(",", "" ) for i in str(data.elf_fam).split(" ")]
			if (token in lower_list):
				current_word = random.choice(change_list)
				if is_m:
					current_word = current_word + "а"


			# определяем город
			if "г." in word:
				_, word = word.split(".")
				token = preprocess_text(word)
				# является ли он большим
				lower_list = [preprocess_text(i) for i in str(data.big_cities).split(" ")]
				if (token in lower_list):
					# меняем на эльфийский
					change_list = [str(i).replace(",", "" ) for i in str(data.elf_cities).split(" ")]
					current_word = random.choice(change_list)
				else:
					# меняем на орочий
					change_list = [str(i).replace(",", "" ) for i in str(data.ork_cities).split(" ")]
					current_word = random.choice(change_list)
				current_word = f"г.{current_word}"


			# определяем улицу
			if "ул." in word:
				_, word = word.split(".")
				token = preprocess_text(word)
				# центр города
				lower_list = [preprocess_text(i) for i in str(data.good_streets).split(" ")]
				if (token in lower_list):
					# меняем на эльфийскую
					change_list = [str(i).replace(",", "" ) for i in str(data.elf_streets).split(" ")]
					current_word = random.choice(change_list)
				else:
					# меняем на орочий
					change_list = [str(i).replace(",", "" ) for i in str(data.ork_streets).split(" ")]
					current_word = random.choice(change_list)

				current_word = f"ул.{current_word}"


		out_text += current_word + " "
	print(out_text)	
