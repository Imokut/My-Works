# Import the Needed Libraries
# Imokut
import re
import jieba
import unicodedata
import matplotlib.pyplot as plt

def extract_chinese_words(lst):
    """
    This function takes in a list of individual words from a Chinese definition for an English Word and extracts the
    individual Chinese Words in them and its context part of speech.
    Example:
    extract_chinese_words(['vt', '.', '丢弃', '；', '放弃', '，', '抛弃'])
    returns:
    [('丢弃', 'vt'), ('放弃', 'vt'), ('抛弃', 'vt')]

    :param lst: A list of characters from a definition of an English Word
    :return: A list of only the Chinese Characters in a definition and the pos in context
    """
    chinese_words = []
    pos = None

    for i, item in enumerate(lst):
        # Remove symbols
        if item in [".", ",", ', ', '; ', ';', '. ', '...']:
            continue

        # Extract part-of-speech
        if item.isalpha() and not all('\u4e00' <= char <= '\u9fff' for char in item) and pos is None:
            pos = item
        elif item.isalpha() and pos is not None and not all('\u4e00' <= char <= '\u9fff' for char in item):
            pos = item

        # Extract Chinese word
        if all('\u4e00' <= char <= '\u9fff' for char in item):
            chinese_words.append((item.strip(), pos))

    return chinese_words
class DictionaryTool:
    def __init__(self):
        self.occurrences = {}
        self.english_dict = {}
        self.chinese_dic = {}
        self.e_t_c_words = {}

    def load_words(self):
        """
        This function reads the word.txt file
        :return: Appends words to the dictionaries in the attributes of the class
        """
        with open("words.txt", 'r', encoding='gb2312') as file:
          #
            for line in file:
              # Split the line into English word, part of speech and Chinese translations
              line_split = line.strip().split(" ")
              english, chinese_definitions = line_split[0], line_split[1:]
              # Split the Chinese translations into a list
              exam = [jieba.lcut(x) for x in chinese_definitions]
              chinese_listset = [extract_chinese_words(x) for x in exam]
              chinese_listwords = [lst[0] for item in chinese_listset for lst in item]

              # Add the English word and its Chinese translations to the dictionary
              self.english_dict[english] = chinese_definitions
              self.e_t_c_words[english] = chinese_listwords

              # Add the Chinese words and their corresponding English words to the dictionary
              for list in chinese_listwords:
                  for chinese in list:
                      if chinese in self.chinese_dic.keys():
                          self.chinese_dic[chinese].append(english)
                      else:
                          self.chinese_dic[chinese] = [english]

    def search_words(self, word):
        """
        Searches for matching words to a word
        :param word: An English Word
        :return: A list of words that match the input word
        """
        found_words = []
        for w in self.english_dict.keys():
            if word.lower() in w.lower():
                found_words.append(w)
        return found_words

    def count_letter_occurrences(self):
        """
         Counts the occurences of each letter of the alphabet in our glossary
         It stores this count in self.occurences
        """
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for w in self.english_dict.keys():
            for char in w:
                if char.isalpha() and char.lower() in alphabet:
                    char = char.lower()
                    if char in self.occurrences:
                        self.occurrences[char] += 1
                    else:
                        self.occurrences[char] = 1

    def display_search_results(self, results):
        """
        Displays the matched words in a search
        """

        if results:
            print("Search Results: ")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result}")
        else:
            print("No result found")

    def display_letter_occurrences(self):
        """
        Prints the count of the occurence of each letter of the alphabet
        :return:
        """
        print("Letter Occurrences:")
        for char, count in self.occurrences.items():
            print(f"{char}, {count}")

    def draw_letter_occurrences_bar_chart(self):
        """
        Draws a Bar Chart that show the Occurrence of each letter in the dictionary

        """
        x = list(self.occurrences.keys())
        y = list(self.occurrences.values())
        plt.bar(x, y)
        plt.xlabel('Letter')
        plt.ylabel('Occurrences')
        plt.title('Letter Occurrences Bar Chart')
        plt.show()

    def define_english_word(self, word):
        """
        Returns the Chinese definition for an English Word
        :param word: The input English word
        :return: Chinese Definition for the English Word
        """
        return self.english_dict[word]

    def search_chinese_word(self, word):
        """
        Searches the dictionary for matched Chinese words
        :param word: The input Chinese Word
        :return: A List of words that match the Chinese word
        """
        found_words = []
        for w in self.chinese_dic.keys():
            if word in w:
                found_words.append(w)
        return found_words


    def return_chinese_def(self, word):
        """
        Prints English words that share a context with the input Chinese word
        :param word: The input Chinese word
        """
        for word in self.chinese_dic[word]:
            print(word)

    def run(self):
        """
        Loads the word.txt file then sets up the Dictionary to be used in the console

        """
        self.load_words()
        while True:
            print("\nDictionary Tool")
            print("1. Search English words")
            print("2. Search Chinese word and show all possible matched English words list")
            print("3. Count letter occurrences")
            print("4. Draw letter occurrences bar graph")
            print("5. Exit")
            choice = input("Enter your choice (1/2/3/4/5): ")
            if choice == '1':
                search_input = input("Enter a word to search: ")
                results = self.search_words(search_input)
                self.display_search_results(results)
                print(f"Total matched words: {len(results)}")  # Display total matched words
                if results:
                    selected_word = input("Select a word from the matched words: ")
                    # Add code to display translation for the selected word
                    definition = self.define_english_word(selected_word)
                    print(definition)
                else:
                    print("No results to select.")
            elif choice == '2':
                search_input = input("Enter a Chinese word to search: ")
                results = self.search_chinese_word(search_input)
                self.display_search_results(results)
                print(f"Total matched words: {len(results)}")  # Display total matched words
                if results:
                    selected_word = input("Select a word from the matched words: ")
                    # Add code to display translation for the selected word
                    self.return_chinese_def(selected_word)
                else:
                    print("No results to select.")
            elif choice == '3':
                self.count_letter_occurrences()
                self.display_letter_occurrences()
            elif choice == '4':
                self.count_letter_occurrences()
                self.draw_letter_occurrences_bar_chart()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")



dt = DictionaryTool()
dt.run()