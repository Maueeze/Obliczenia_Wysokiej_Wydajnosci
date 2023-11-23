import csv
import numpy as np
import random

partie = [1 ,2 ,3, 4, 5]
historia_wynikow = []
populacja_dane_opisowe = []
populacja_dane_liczbowe = []
populacja_dane_spoleczne = []
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
populacja_dane_poparcie = []
event_list = [ ]
bad_event_list = [ ]
historia_eventow = []
macierz_jednostkowa = np.identity(5)
#nr_glosowania = 1


def shuffle_array(arr):  #funkcja do tasowania tablicy indeksów
    random.shuffle(arr)
    return arr

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

def normalizuj (arr):   # normalizacja poparcia tak by suma poparć nie była większa od 100 punktów
    suma = arr[0]+arr[1]+arr[2]+arr[3]+arr[4]

    for i in range(0,5):
        arr[i] = round(100*arr[i]/suma,2)

    return arr



def glosowanie (arr): # głosowanie na partie
    global nr_glosowania
    wynik1 = 0
    wynik2 = 0
    wynik3 = 0
    wynik4 = 0
    wynik5 = 0

    for i in range(0, populacja):


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
    temp_wyniki = normalizuj(temp_wyniki)
    #temp_wyniki1 = [nr_glosowania, temp_wyniki[0], temp_wyniki[1], temp_wyniki[2], temp_wyniki[3], temp_wyniki[4]]
    historia_wynikow.append(temp_wyniki)
    #nr_glosowania += 1
    #print(temp_wyniki)



def create_file(name, arr):   #funkcja do tworzenia pliku .csv
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)

        for i in range(len(arr)):
            writer.writerow(arr[i])
    file.close()

def rozmowa(wsp_og, wsp1, wsp2, poparcie1, poparcie2):


    par = losuj([1, -1], [0.5, 0.5])
    wsp_og = wsp_og*par
    wsp1 = wsp1 * wsp_og
    wsp2 = wsp2 * wsp_og

    temp_poparcie1 = poparcie1
    temp_poparcie2 = poparcie2

    for i in range (0,5):
        poparcie1[i] = temp_poparcie1[i] + temp_poparcie2[i] * wsp2
        poparcie2[i] = temp_poparcie2[i] + temp_poparcie1[i] * wsp1

    poparcie1 = normalizuj(poparcie1)
    poparcie2 = normalizuj(poparcie2)
    return poparcie1, poparcie2

def dekoduj_partia(i):

    if i == 0:
        temp_partia = "Prawica"
        return temp_partia
    elif i == 1:
        temp_partia = "Studencka Partia Przyjaciół Piwa"
        return temp_partia
    elif i == 2:
        temp_partia = "Obóz Liberalny"
        return temp_partia
    elif i == 3:
        temp_partia = "Przyszłość dla Wszystkich"
        return temp_partia
    elif i == 4:
        temp_partia = "Harmonia Społeczna"
        return temp_partia



def event(n,arr):

    #czy event się wydarzy?
    los = losuj([0, 1], [0.95, 0.05])
    temp_arr = np.array(arr)
    if los == 1:
        #event bedzie negatywny czy pozytywny?
        los2 = losuj([0,1], [0.5,0.5])
        if los2 == 1:
            temp_wyniki = [1/historia_wynikow[n][0], 1/historia_wynikow[n][1], 1/historia_wynikow[n][2], 1/historia_wynikow[n][3], 1/historia_wynikow[n][4]]
            losuj_partie = int(losuj([0, 1, 2, 3, 4], temp_wyniki))
            shuffle_array(event_list)
            temp_event1 = event_list[0][0]
            temp_event2 = event_list[0][1]
        elif los2 == 0:
            losuj_partie = int(losuj([0, 1, 2, 3, 4], historia_wynikow[n]))
            shuffle_array(event_list)
            temp_event1 = bad_event_list[0][0]
            temp_event2 = bad_event_list[0][1]



        partia = dekoduj_partia(losuj_partie)
        temp_event = [n, temp_event1 + partia + temp_event2]
        historia_eventow.append(temp_event)


        zmiana_wspolczynnika = losuj_z_rozkladu_normalnego(0, 10, 3, 5)
        if los2 == 0:
            temp_arr[:,losuj_partie] *= 1 - zmiana_wspolczynnika / 100
        elif los2 == 1:
            temp_arr[:,losuj_partie] *= 1 + zmiana_wspolczynnika / 100
        #print(n, zmiana_wspolczynnika)
        for i in range(0,1000):
           temp_arr[i] = normalizuj(temp_arr[i])
        return temp_arr
    elif los == 0:
        return arr


with open('populacja_dane_opisowe.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if len(row) > 0:
            tempdata = [str(row[0]),str(row[1])]
            populacja_dane_opisowe.append(tempdata)


with open('populacja_dane_liczbowe.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if len(row) > 0:
            tempdata = [float(row[0]), float(row[1])]
            populacja_dane_liczbowe.append(tempdata)

with open('populacja_dane_spoleczne.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if len(row) > 0:
            tempdata = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11])]
            populacja_dane_spoleczne.append(tempdata)

with open('populacja_dane_poparcie.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if len(row) > 0:
            tempdata = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4])]
            populacja_dane_poparcie.append(tempdata)


with open('eventy.csv') as f:
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        if len(row) > 0:
            tempdata = [str(row[0]),str(row[1])]
            event_list.append(tempdata)

with open('eventy_zle.csv') as f:
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        if len(row) > 0:
            tempdata = [str(row[0]),str(row[1])]
            bad_event_list.append(tempdata)




populacja = len(populacja_dane_liczbowe)
nr_wyborcow = list(range(0, populacja))   #lista z indeksami wyborców


glosowanie(populacja_dane_poparcie) # głosowanie pierwotne

    #wybory
n = 400 #liczba tur
rozmowy = 0
for i in range(0,n): #czas na interakcje
    shuffle_array(nr_wyborcow) #tasowanie listy z numerami
    #print(nr_wyborcow)


    for j in range(0, int(populacja/2)):

        #bierzemy dwa pierwsze numery z potasowanej listy i określamy szansę na rozmowę
        szansa1 = populacja_dane_liczbowe[nr_wyborcow[2*j]][0]
        szansa2 = populacja_dane_liczbowe[nr_wyborcow[2*j+1]][0]

        szansa_na_rozmowe = min(szansa1,szansa2)
        czy_do_rozmowy_dojdzie = losuj([0, 1], [1-szansa_na_rozmowe, szansa_na_rozmowe]) #liczymy szanse na rozmowę

        if czy_do_rozmowy_dojdzie == 1: # jeżeli do rozmowy dojdzie to wtedy następuje wymiana poparcia

            populacja_dane_poparcie[2*j], populacja_dane_poparcie[2*j+1] = rozmowa(0.001, populacja_dane_liczbowe[nr_wyborcow[2*j]][1], populacja_dane_liczbowe[nr_wyborcow[2*j+1]][1], populacja_dane_poparcie[nr_wyborcow[2*j]], populacja_dane_poparcie[nr_wyborcow[2*j+1]])

            rozmowy += 1

    #print(i)
    populacja_dane_poparcie = event(i, populacja_dane_poparcie)
    glosowanie(populacja_dane_poparcie)



print("------------------------")
#for i in range(1,populacja):

    #print(populacja_dane_opisowe[i][0], " ", populacja_dane_opisowe[i][1], " ", populacja_dane_liczbowe[i][0], " ", populacja_dane_liczbowe[i][1], " ", populacja_dane_liczbowe[i][2], " ", populacja_dane_liczbowe[i][3], " ",populacja_dane_liczbowe[i][4])

print(rozmowy)
glosowanie(populacja_dane_poparcie)

historia_wynikow_zmiana = []
for i in range(0,len(historia_wynikow)):

    A = historia_wynikow[i][0]
    B = historia_wynikow[i][1]
    C = historia_wynikow[i][2]
    D = historia_wynikow[i][3]
    E = historia_wynikow[i][4]


    tempwynik = [i+1,A, B, C, D, E ]
    historia_wynikow_zmiana.append(tempwynik)

create_file("wyniki.csv",historia_wynikow_zmiana)
create_file("historia_eventow.csv", historia_eventow)