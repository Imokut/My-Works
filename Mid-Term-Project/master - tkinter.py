# Import the Needed Libraries
# Imokut
import re
import jieba
import unicodedata
import matplotlib.pyplot as plt
import tkinter as tk

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


occurrences = {}
eng_to_chinese = {}
chinese_to_eng = {}
e_t_c_words = {}

# Read word.txt file and create a dictionary of English and Chinese Words
with open("words.txt", 'r', encoding='gb2312') as file:
    for line in file:
      # Split the line into English word, part of speech and Chinese translations
      line_split = line.strip().split(" ")
      english, chinese_definitions = line_split[0], line_split[1:]
      # Split the Chinese translations into a list
      exam = [jieba.lcut(x) for x in chinese_definitions]
      chinese_listset = [extract_chinese_words(x) for x in exam]
      chinese_listwords = [lst[0] for item in chinese_listset for lst in item]

      # Add the English word and its Chinese translations to the dictionary
      eng_to_chinese[english] = chinese_definitions
      e_t_c_words[english] = chinese_listwords

      # Add the Chinese words and their corresponding English words to the dictionary
      for list in chinese_listwords:
          for chinese in list:
              if chinese in chinese_to_eng.keys():
                  chinese_to_eng[chinese].append(english)
              else:
                  chinese_to_eng[chinese] = [english]

def search_words():
    """
    Searches for matching words to a word
    :return: A list of words that match the input word
    """
    # Clear previous results
    listbox.delete(0, tk.END)
    label_count.config(text='')
    
    # Get Search item
    search_term = entry_search.get().strip().lower()

    matched_words = []
    for word in eng_to_chinese.keys():
        if search_term in word.lower():
            matched_words.append(word)

    for word in chinese_to_eng.keys():
        if search_term in word.lower():
            matched_words.extend(chinese_to_eng[word])
        
    if len(matched_words) > 0:
        for word in matched_words:
            listbox.insert(tk.END, word)
        label_count.config(text=f'{len(matched_words)} word(s) matched')
    else:
        listbox.insert(tk.END, 'No matching words found')

def show_definition(event):
    selected_word = listbox.get(listbox.curselection())
    if selected_word in eng_to_chinese:
        definition = eng_to_chinese[selected_word]
    else:
        definition = ', '.join(chinese_to_eng[selected_word])
    label_definition.config(text=f'{selected_word}: {definition}')

window = tk.Tk()
window.title('Dictionary App')

# Create search bar and button
label_search = tk.Label(window, text='Search for a word:')
label_search.grid(row=0, column=0)
entry_search = tk.Entry(window)
entry_search.grid(row=0, column=1)
button_search = tk.Button(window, text='Search', command=search_words)
button_search.grid(row=0, column=2)

# Create dropdown listbox and definition label
listbox = tk.Listbox(window)
listbox.grid(row=1, column=0, columnspan=3)
listbox.bind('<<ListboxSelect>>', show_definition)
label_definition = tk.Label(window, text='')
label_definition.grid(row=2, column=0, columnspan=3)

# Create count label
label_count = tk.Label(window, text='')
label_count.grid(row=3, column=0, columnspan=3)

# Start GUI event loop
window.mainloop()

