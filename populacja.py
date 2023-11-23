
import csv
import numpy as np
import random


plec = ["Mężczyzna", "Kobieta"]
plec_praw = [0.5, 0.5] #współczynniki do wyznaczenia płci wyborcy
wyksztalcenie = ["podstawowe", "gimnazjalne", "zawodowe", "średnie", "wyższe"]
wyksztalcenie_praw = [0.117, 0.031, 0.196, 0.324, 0.231] # współczynniki do określenia wykształcenia
partie = [1 ,2 ,3, 4, 5] #Prawica, Studencka Partia Przyjaciół Piwa, Obóz Liberalny, Przyszłość dla Wszystkich, Harmonia Społeczna
partie_dane_spoleczne = [
[ 1,  0,  1,  1,  1], # 1. Bezpieczeństwo
[ 1,  1,  1, -1, -1], # 2. Dostęp do broni
[ 0,  0,  1,  1, -1], # 3. Energia Atomowa
[-1,  1,  1,  0,  0], # 4. Integracja Europejska
[ 0,  1,  0, -1,  1], # 5. Legalizacja miękkich narkotyków
[ 1,  1,  0,  1,  1], # 6. Ochrona Zdrowia
[ 0,  0,  0,  0,  1], # 7. Pomoc Uchodźcom
[-1,  1,  0,  1,  1], # 8. Programy socjalne
[ 1,  1,  0, -1, -1], # 9. Religijność
[ 1, -1, -1,  1,  0], # 10. Rozliczenie Historii
[-1,  1,  1,  0,  1], # 11. Swobody obywatelskie
[ 0,  0,  1,  1,  0], # 12. Wolność
]

populacja = 10000
populacja_dane_opisowe = np.empty((populacja,2), dtype=object)  #tablica cech opisowych - płeć, wykształcenie
populacja_dane_liczbowe = np.zeros((populacja,2), dtype=float)  #tablica cech liczbowych, współczynnik interakcji, zdolność przekonywania
populacja_dane_spoleczne = np.zeros((populacja,12), dtype=float) #tablica zainteresowań społecznych:
# 1. Bezpieczeństwo
# 2. Dostęp do broni
# 3. Energia Atomowa
# 4. Integracja Europejska
# 5. Legalizacja miękkich narkotyków
# 6. Ochrona Zdrowia
# 7. Pomoc Uchodźcom
# 8. Programy socjalne
# 9. Religijność
# 10. Rozliczenie Historii
# 11. Swobody obywatelskie
# 12. Wolność
populacja_dane_poparcie = np.zeros((populacja,5), dtype=float) #tablica poparcia



def losuj(opcje, prawdopodobienstwa): # losowanie opcji z zadanego rozkładu prawdopodobieństwa
    if len(opcje) != len(prawdopodobienstwa):
        raise ValueError("Liczba opcji musi być taka sama jak liczba prawdopodobieństw.")

    wybrana_opcja = random.choices(opcje, prawdopodobienstwa, k=1)[0]
    return wybrana_opcja


def losuj_z_rozkladu_normalnego(min_value, max_value, odchylenie_standardowe, srednia): #Losowanie wartości z zadanego zakresu z zadaną średnią i odchyleniem standardowym
    while True:
        liczba = np.random.normal(srednia, odchylenie_standardowe)
        if min_value <= liczba <= max_value:
            return round(liczba,4)


def glosowanie (arr): # głosowanie na partie

    wynik1 = 0
    wynik2 = 0
    wynik3 = 0
    wynik4 = 0
    wynik5 = 0

    for i in range(0,populacja):

        temp_arr = [arr[i][0], arr[i][1], arr[i][2], arr[i][3], arr[i][4]]
        #glos = losuj(partie, [arr[i][2], arr[i][3], arr[i][4]])
        najwiekszy_wynik = max(temp_arr)

        glos = temp_arr.index(najwiekszy_wynik)+1


        if glos == 1:
            wynik1 += 1
        elif glos == 2:
            wynik2 += 1
        elif glos == 3:
            wynik3 += 1
        elif glos == 4:
            wynik4 += 1
        elif glos == 5:
            wynik5 += 1

    temp_wyniki = [wynik1, wynik2, wynik3, wynik4, wynik5]

    print(temp_wyniki)


def create_file(name, arr):   #funkcja do tworzenia pliku .csv
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)

        for i in range(len(arr)):
            writer.writerow(arr[i])
    file.close()

def min_max_scaling(data, new_min, new_max):
    # Znajdź min i max w danych
    min_val = np.min(data)
    max_val = np.max(data)

    # Skalowanie do nowego zakresu
    scaled_data = new_min + (data - min_val) * (new_max - new_min) / (max_val - min_val)

    return scaled_data

def normalizuj (arr):   # normalizacja poparcia tak by suma poparć nie była większa od 100 punktów
    suma = arr[0]+arr[1]+arr[2]+arr[3]+arr[4]

    for i in range(0,5):
        arr[i] = round(100*arr[i]/suma,2)

    return arr

for i in range(0,populacja): #pętla dystrybucji cech

        populacja_dane_opisowe[i][0] = losuj(plec, plec_praw)  #określenie płci
        populacja_dane_opisowe[i][1] = losuj(wyksztalcenie,wyksztalcenie_praw) #określenie wykształcenia
        populacja_dane_liczbowe[i][0] = losuj_z_rozkladu_normalnego(0, 1, 0.4, 0.4) #określenie współczynnika interakcji
        populacja_dane_liczbowe[i][1] = losuj_z_rozkladu_normalnego(0, 1, 0.4, 0.4) #określenie współczynnika zdolności przekonywania

        #dane_spoleczne

        # 1. Bezpieczeństwo
        populacja_dane_spoleczne[i][0] = losuj_z_rozkladu_normalnego(0, 1, 0.4, 0.6)
        # 2. Dostęp do broni
        populacja_dane_spoleczne[i][1] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.0)
        # 3. Energia Atomowa
        populacja_dane_spoleczne[i][2] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.5)
        # 4. Integracja Europejska
        populacja_dane_spoleczne[i][3] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.2)
        # 5. Legalizacja miękkich narkotyków
        populacja_dane_spoleczne[i][4] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, -0.1)
        # 6. Ochrona Zdrowia
        populacja_dane_spoleczne[i][5] = losuj_z_rozkladu_normalnego(0, 1, 0.4, 0.6)
        # 7. Pomoc Uchodźcom
        populacja_dane_spoleczne[i][6] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.6)
        # 8. Programy socjalne
        populacja_dane_spoleczne[i][7] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.3)
        # 9. Religijność
        populacja_dane_spoleczne[i][8] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.3)
        # 10. Rozliczenie Historii
        populacja_dane_spoleczne[i][9] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0)
        # 11. Swobody obywatelskie
        populacja_dane_spoleczne[i][10] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.3)
        # 12. Wolność
        populacja_dane_spoleczne[i][11] = losuj_z_rozkladu_normalnego(-1, 1, 0.4, 0.8)




populacja_dane_poparcie = np.dot(populacja_dane_spoleczne, partie_dane_spoleczne)
populacja_dane_poparcie = [[round(value, 2) for value in row] for row in populacja_dane_poparcie]

for i in range(0, populacja):
    populacja_dane_poparcie[i] = min_max_scaling(populacja_dane_poparcie[i], 20, 100)
    populacja_dane_poparcie[i] = normalizuj(populacja_dane_poparcie[i])

glosowanie(populacja_dane_poparcie)

create_file("populacja_dane_opisowe.csv", populacja_dane_opisowe)
create_file("populacja_dane_liczbowe.csv", populacja_dane_liczbowe)
create_file("populacja_dane_spoleczne.csv", populacja_dane_spoleczne)
create_file("populacja_dane_poparcie.csv", populacja_dane_poparcie)





