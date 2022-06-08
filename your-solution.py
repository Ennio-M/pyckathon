'''
REPO: pyckathon

PREMESSA:
L’esercizio serve ad allontanare le paure che ci possono affliggere all’idea di dover imparare da zero un nuovo linguaggio.
Se non ve ne siete accorti, negli ultimi mesi ne abbiamo imparati già due. Oggi però farete tutto da soli.

SCOPO DEL GIOCO:
Sicuramente avrete già giocato al gioco dell’impiccato sui banchi di scuola, nei momenti morti di alcune lezioni con il vostro vicino.
Uno dei giocatori pensa una parola e aggiunge su un foglio un numero di trattini pari al numero di lettere che la compongono.
L’altro giocatore dovrà indovinare la parola tentando di indovinare le lettere che la compongono.
Ogni tentativo sbagliato verrà contato come errore.

TECNOLOGIE:
Oggi si lavora con Python, per questo motivo dovete concentrarvi solo sul file YOUR_SOLUTION.py, non curatevi degli altri file.
Se volete poi dopo le 18.00 potrete sbirciare il resto del codice.
Ma l’escamotage che abbiamo usato per farvi lavorare tranquilli è solo un modo semplice e comodo per permettervi di lavorare senza distrazioni

CONSEGNA:
I giocatori sono l'utente e il computer.
Il computer sceglie casualmente una parola e l'utente la dovrà indovinare.
Ha a disposizione 5 tentativi.

L'utente potrà provare ad indovinare una sola lettera per volta.
Ad ogni inserimento (sia che avvenga tramite tasto INVIO oppure tramite CLICK su apposito pulsante) il computer deve controllare
se quella lettera è presente nella parola da indovinare.

Se la lettera è presente, deve apparire al posto giusto, sostituendo il trattino (o i trattini) corrispondente.
Se la lettera non è presente, l'utente deve essere avvisato dell'errore con un messaggio che mostra anche quanti tentativi sono rimasti.
Se la lettera è già stata usata, l'utente deve essere avvisato con un messaggio, ma i tentativi a disposizione non devono diminuire.

Nella parte sottostante il campo di input saranno mostrate tutte le lettere già utilizzate dall'utente (sia quelle corrette che quelle errate).

Il gioco termina quando l'utente esaurisce i tentativi a disposizione oppure se indovina la parola.
In entrambi i casi si deve mostrare un messaggio adatto alla situazione.
'''

# CONSIGLI:
# - occhio alla indentazione

#------------------------------------------LIBRERIE-------------------------------------------------------

import random   #libreria per usare un valore casuale
import pyodide  #libreria per pyscript
import js       #libreria per javascript
from utils import Utils #libreria per utilizzare funzioni JS

custom_utils = Utils(pyodide, js) #istanza della libreria - ripensate all'esercizio di PHP con Movie ;)

#---------------------------------------ELEMENTI DAL DOM------------------------------------------------------

# questi elementi sono già stati catturati per te, 
# ti serviranno per prendere il valore inserito e catturare l'evento di invio

user_letter = custom_utils.getHtmlElement("user-letter")
add_letter_btn = custom_utils.getHtmlElement("add-letter-btn")
used_letters = custom_utils.getHtmlElement("used-letters")
result = custom_utils.getHtmlElement("result")
solution = custom_utils.getHtmlElement('solution')


# questo elemento conterrà il testo segnaposto per la parola da indovinare
word_html_container = custom_utils.getHtmlElement('word')

#----------------------------------------------------------------------------------------------------


def main():

    #le variabili sono definite come esempi, non siete obbligati ad utilizzarle tutte o solo queste

    global words
    global count
    global errors
    global length
    global word
    global display
    global already_guessed
    global limit
    global user_letters
    global user_value

    count = 5
    errors = 0
    display = ""
    already_guessed = []
    user_letters = []

    
    words = ['matto', 'gatto', 'pazzo'] # array con le parole da indovinare

    word = random.choice(words) #selezione casuale della parola

    letters = list(word) #divido la parola in una lista di lettere

    for letter in letters: #aggiungo un _ per ogni lettera della parola
        display += "_"

    custom_utils.writeToHtmlElement(word_html_container, '%s' % (display)) #output degli underscore

    def checkLetters(e): #funzione per controllare le lettere
        global count
        global display
        user_value = getattr(user_letter, "value").lower() #salvo la lettera inserita dall'utente
        user_letters.append(user_value) #la salvo in una lista
        if(user_value in letters): #controllo che la lettera inserita sia nella lista
            display = ""
            already_guessed.append(user_value)
            for letter in letters:
                if(letter in already_guessed):
                    display += letter
                else:
                    display += "_"
        else:
            count -= 1
            custom_utils.writeToHtmlElement(result, "Lettera sbagliata! Hai altri %d tentativi!" % (count))

        custom_utils.writeToHtmlElement(word_html_container, '%s' % (display)) #ristampo la parola con gli underscore e le lettere indovinate

        if(all(item in already_guessed for item in letters)): #controllo se le lettere indovinate contengono tutte le lettere della parola
            custom_utils.writeToHtmlElement(result, "Hai Vinto!")
            custom_utils.writeToHtmlElement(solution, "<span>Ricarica per rigiocare</span>")
            custom_utils.disableInputElement(user_letter)
            custom_utils.removeOnClickEventFromHtmlElement(add_letter_btn)
        if(count == 0): #controllo che i tentativi non siano esauriti
            custom_utils.writeToHtmlElement(result, "Hai Perso :(")
            custom_utils.writeToHtmlElement(solution, "La parola da indovinare era: <span>%s</span> <br> Ricarica per rigiocare" % (word))
            custom_utils.disableInputElement(user_letter)
            custom_utils.removeOnClickEventFromHtmlElement(add_letter_btn)

        custom_utils.writeToHtmlElement(used_letters, 'Lettere usate: <span>%s</span>' % (user_letters)) #stampo quali lettere sono state inserite

        custom_utils.emptyInputElement(user_letter) #svuoto il campo di input


        custom_utils.writeToConsole(e)

    def checkEnter(e): #funzione per controllare che il tasto premuto sia ENTER
        custom_utils.writeToConsole(e)
        if custom_utils.checkIfEventIsEnterKey(e):
            checkLetters(e) #se il tasto premuto è ENTER chiamo la funzione di controllo lettere
    
    custom_utils.addOnClickEventToHtmlElement(add_letter_btn, checkLetters) #richiamo la funzione di controllo lettere al click del bottone
    custom_utils.addKeyupEventToHtmlElement(user_letter, checkEnter) #alla pressione di un tasto chiamo la funzione per controllare che sia ENTER

    # inserisco la stringa segnaposto dentro il contenitore HTML
    # display = "___" # da modificare
    # custom_utils.writeToHtmlElement(word_html_container, '%s' % (display))


main()