from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
from clp3 import clp
import re
import locale
locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session handling

possible_words_global = [
    "abstrakcja", "agresja", "akcelerator", "architektura", "balast", "biografia", "błyskawica", "bratnia", "człowiek", "celestyn",
    "cyrkiel", "dyscyplina", "efekt", "ekspedycja", "elektromagnetyzm", "euforia", "faktura", "filozofia", "gargulec", "geometria",
    "horyzont", "ideologia", "instrument", "jaskinia", "kamfora", "kalendarz", "kariera", "klucz", "kolizja", "kometa",
    "komiks", "koncentrat", "konwencja", "kwadratura", "labirynt", "lira", "magma", "malachit", "marazm", "memento",
    "metafora", "neon", "oddech", "oligarchia", "opinia", "patriotyzm", "percepcja", "perswazja", "plaza", "preludium",
    "prognostyk", "proszek", "przywódca", "pułapka", "racja", "rektor", "remedium", "rewolucja", "sekwencja", "sferoid",
    "symfonia", "teatr", "topografia", "tragedia", "transformacja", "ulica", "unikat", "upiór", "węgiel", "widmo",
    "wiedza", "wiza", "wyjątek", "zaburzenie", "zajęcie", "zasięg", "zamieszanie", "zapatrywanie", "zasada", "zatrudnienie",
    "zawód", "zbrodnia", "zdecydowanie", "zjawisko", "złudzenie", "zmysł", "zniekształcenie", "żart", "żółw", "żuraw",
    "abdykacja", "alkoholizm", "animacja", "arbitraż", "aspiracja", "bełkot", "biomasa", "biblioteka", "blizna", "bomba",
    "całun", "czepiec", "czystość", "deklinacja", "delfin", "depresja", "detonacja", "dyktatura", "epoka", "ekspert",
    "ferment", "filantropia", "fluktuacja", "gestykulacja", "głosowanie", "głębokość", "hołd", "hymn", "infuzja", "instrukcja",
    "intencja", "jasność", "kaprys", "katastrofa", "komunikacja", "konsultacja", "korupcja", "krwotok", "król", "kulisy",
    "kwantyzacja", "logika", "marzyciel", "medytacja", "metoda", "moc", "nacisk", "nałóg", "naśladowca", "niezgoda",
    "oszukiwanie", "przestroga", "punkt", "robotnik", "rozbiór", "rozważania", "ruch", "samopoczucie", "spór", "sukces",
    "szablon", "symbol", "tendencja", "teza", "władza", "wybór", "zapał", "zagłada", "zatrzymanie", "zło", "zniszczenie",
]
dictionary_global = []
guessed_words_global = []

def create_bases():
    first_words = []

    with open('odm.txt', 'r') as file:
        for line in file:
            words = line.strip().split(',')
            # print(words)
            if words:
                for word in words:
                    word.strip()
                    # print("S: ", word)
                    word_s = re.split(r'[ .-]+', word)
                    if word_s[0] == '':
                        word_s.pop(0)
                    # print("X: ", word_s)
                    if len(word_s) < 2 and word == word.lower() and len(word) > 2:
                        if (clp(word)):
                            e_id = clp(word)[0]
                            e_l = clp.label(e_id)
                            if e_l[0] == 'A':
                                first_words.append(word)

    # print(len(first_words))
    first_words = set(first_words)
    # print(len(first_words))

    # Create output directory if it doesn't exist
    # output_dir = os.path.join('.', 'my_data')
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    file_name = "all_nouns.txt"
    # print(file_name)
    # output_file = os.path.join(output_dir, file_name)
    output_file = file_name
    # for word in first_words:
    #     if(len() == i):
    #         words.append(eq)
    # # Write words to the file, one per line
    with open(output_file, 'w') as f:
        for word in first_words:
            f.write(word + '\n')

        print(f"Words have been saved to {output_file}")

def pick_the_right_word():
    global possible_words_global
    max = len(possible_words_global)
    import random
    random_index = random.randint(0, max-1)
    right_word = possible_words_global[random_index]

    session['right_word'] = right_word

    return right_word

def read_the_base():
    global dictionary_global
    print("wczytuję bazę")
    with open('all_nouns.txt', 'r') as file:
        for line in file:
            word = line.strip()
            dictionary_global.append(word)

def common_prefix(word1, template):
    part1 = part2 = ''
    min_length = min(len(word1), len(template))
    letter_i = 0

    while (letter_i < min_length and word1[letter_i] == template[letter_i]):
        part1 += word1[letter_i]
        letter_i += 1
    if len(word1) > len(part1):
        part2 += word1[len(part1):len(word1)]

    return part1, part2


def create_hints_list():
    global guessed_words_global
    right_word = session.get('right_word')
    sorted_list = sorted(guessed_words_global, key=lambda x: locale.strxfrm(x))
    guessed_words_global = sorted_list
    right_word_ind = guessed_words_global.index(right_word)
    pre_words = guessed_words_global[:right_word_ind]
    pre_words = [common_prefix(wyraz, right_word) for wyraz in pre_words]
    post_words = guessed_words_global[right_word_ind+1:len(guessed_words_global)]
    post_words = [common_prefix(wyraz, right_word) for wyraz in post_words]
    return pre_words, post_words


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game_start')
def game_start():
    session['right_word'] = None
    global possible_words_global
    global guessed_words_global
    guessed_words_global.clear()
    pick_the_right_word()
    right_word = session.get('right_word')
    guessed_words_global.append(right_word)
    print(right_word)
    global dictionary_global
    read_the_base()

    title = "Podaj pierwsze słowo:"
    return render_template('word_input.html',
                           # words_list=words_list[:20],
                           t = title)


@app.route('/word_input', methods=["GET", "POST"])
def word_input():
    global possible_words_global
    global dictionary_global
    global guessed_words_global
    right_word = session.get('right_word')
    title = "Podaj kolejne słowo"
    pre_words, post_words = create_hints_list()

    if request.method == "POST":
        guess = request.form.get(f'current_word').lower()
        if guess not in dictionary_global:
            title = "Podaj rzeczownik!"
            return render_template('word_input.html', pre_words = pre_words, post_words = post_words, t=title)
        elif guess == right_word:
            title = "ZWYCIĘSTWO!"
            return render_template('word_input.html', pre_words = pre_words, post_words = post_words, t=title)
        elif guess in guessed_words_global and guess != right_word:
            title = "Podaj nowy wyraz!"
            return render_template('word_input.html', pre_words = pre_words, post_words = post_words, t=title)
        else:
            guessed_words_global.append(guess)
            pre_words, post_words = create_hints_list()
            return render_template('word_input.html', pre_words = pre_words, post_words = post_words, t=title)
        # title = "Proponuję te słowa:"
        # feedback.append(request.form.get(f'current_word'))
        # for i in range(word_length):
        #     letter_feedback = request.form.get(f'feedback-{i}')
        #     feedback.append(letter_feedback)
        # # print("User feedback:", feedback)
        #
        # # Here you can add additional processing for feedback if needed
        # if len(feedback[0]) != word_length:
        #     return redirect(url_for('word_input'))
        # else:
        #     words_list = eliminate_words(feedback)
        #     possible_words_global = words_list
        #     if len(words_list) == 1:
        #         title = "To musi być to słowo!"
        #     elif len(words_list) == 0:
        #         title = " Nie mam już pomysłów :c"
        #     return render_template('word_input.html',
        #                            # words_list=words_list,
        #                            t=title)

    return render_template('word_input.html', word_list=possible_words_global)

@app.route('/input_processing/<feedback>')
def input_processing(feedback):
    return render_template('gra.html', feedback=feedback)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=12014)
