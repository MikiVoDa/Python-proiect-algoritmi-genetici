import random
from matplotlib import pyplot as plt
import numpy as np

nr_obiecte = 7
iteratia = 0
iteratiaMax = 600
v = [50, 20, 80, 100, 120, 15, 40]
g = [10, 18, 8, 12, 20, 7, 5]
greutate_rucsac_max = 30 # 30 de kg
nr_cromozomi = 60
crom_list = []
penalizare = 20
nr_parinti_selectare_turneu = 4 # Cati cei mai buni cromozomi selectam
nr_participanti_turneu = 3 # numărul de participanți în turneu
pm = 0.1 #probabilitate mutatie

def generare_lista_binara(n):
    lista_binara = [random.choice([0, 1]) for _ in range(n)]
    return lista_binara

def calculare_valoare(temparr):
    sum = 0
    for i in range(len(temparr)):
        sum+= v[i] * temparr[i]
    return sum
def calculare_greutate(temparr):
    sum = 0
    for i in range(len(temparr)):
        sum+= g[i] * temparr[i]
    return sum
def distanta_hamming(crom1, crom2):
    return sum(c1 != c2 for c1, c2 in zip(crom1, crom2))
for i in range(nr_cromozomi):
    crom_list.append(generare_lista_binara(nr_obiecte))
print(v)
print(g)
evolutie_adecvare_medie = []
evolutie_diversitate = []
evolutie_convergenta = []
while iteratia != iteratiaMax:
    lista_valori = []
    lista_greutati = []
    print()
    for i in range(nr_cromozomi):
        fitness_g = calculare_greutate(crom_list[i])
        fitness_v = calculare_valoare(crom_list[i])
        if fitness_g > greutate_rucsac_max:
            fitness_v -= penalizare*(fitness_g - greutate_rucsac_max)
        lista_valori.append(fitness_v)
        lista_greutati.append(fitness_g)
        #print(crom_list[i], fitness_v, fitness_g)
        lista_valori.append(fitness_v)
        lista_greutati.append(fitness_g)

    parinti_alesi = []


    for i in range(nr_parinti_selectare_turneu):
        participanti = random.sample(crom_list, nr_participanti_turneu)
        cel_mai_bun = None
        lista_valori_pt_max = []
        for participant in participanti:
            indexu = crom_list.index(participant)
            lista_valori_pt_max.append(lista_valori[indexu])
        cel_mai_bun = max(lista_valori_pt_max)
        index_cromozom_cel_mai_bun = lista_valori.index(cel_mai_bun)
        parinti_alesi.append(crom_list[index_cromozom_cel_mai_bun])
        #print(participanti)
        #print(lista_valori_pt_max)
        #print(index_cromozom_cel_mai_bun)
        #print(crom_list[index_cromozom_cel_mai_bun])
    #print(parinti_alesi)
    copii = []
    for i in range(0, nr_parinti_selectare_turneu, 2):
        p1 = parinti_alesi[i]
        p2 = parinti_alesi[i+1]

        poz = random.randint(0,nr_obiecte-1)

        c1 = []
        c2 = []
        switch = False
        for j in range(nr_obiecte):
            if j == poz+1:
                switch = True
            if switch == False:
                c1.append(p1[j])
                c2.append(p2[j])
            else:
                c1.append(p2[j])
                c2.append(p1[j])

        nrAleatoare = [round(random.uniform(0, 1), 3) for _ in range(nr_obiecte)]
        for i in range(nr_obiecte):
            if nrAleatoare[i] < pm:
                 if c1[i] == 0:
                     c1[i] = 1
                 else:
                     c1[i] = 0
       # nrAleatoare = [round(random.uniform(0, 1), 3) for _ in range(nr_obiecte)]
       # for i in range(nr_obiecte):
       #     if nrAleatoare[i] < pm:
       #          if c2[i] == 0:
       #              c2[i] = 1
       #          else:
       #              c2[i] = 0
        copii.append(c1)
        copii.append(c2)
    print(copii)
    cromozomi_noua_populatie = nr_cromozomi + nr_parinti_selectare_turneu
    noua_populatie = crom_list + copii

    noua_populatie_alesi = []

    lista_valori_noua_populatie = []
    lista_greutati_noua_populatie = []

    for i in range(cromozomi_noua_populatie):
        fitness_g = calculare_greutate(noua_populatie[i])
        fitness_v = calculare_valoare(noua_populatie[i])
        if fitness_g > greutate_rucsac_max:
            fitness_v -= penalizare*(fitness_g - greutate_rucsac_max)
        lista_valori_noua_populatie.append(fitness_v)
        lista_greutati_noua_populatie.append(fitness_g)
        print(noua_populatie[i], fitness_v, fitness_g)


    for i in range(nr_parinti_selectare_turneu):
        participanti = random.sample(noua_populatie, nr_participanti_turneu)
        cel_mai_slab = None
        lista_valori_pt_max = []
        for participant in participanti:
            indexu = noua_populatie.index(participant)
            lista_valori_pt_max.append(lista_valori_noua_populatie[indexu])
        cel_mai_slab = min(lista_valori_pt_max)
        index_cromozom_cel_mai_slab = lista_valori_noua_populatie.index(cel_mai_slab)
        noua_populatie.pop(index_cromozom_cel_mai_slab)

    suma_adecvare = sum(lista_valori_noua_populatie)
    adecvare_medie = suma_adecvare / cromozomi_noua_populatie
    evolutie_adecvare_medie.append(adecvare_medie)

    crom1, crom2 = random.sample(noua_populatie, 2)
    diversitate_medie = distanta_hamming(crom1, crom2)
    evolutie_diversitate.append(diversitate_medie)

    asemanare_medie = 1 - diversitate_medie
    evolutie_convergenta.append(asemanare_medie)
    print(noua_populatie)
    crom_list = noua_populatie
    iteratia += 1
    if iteratia == iteratiaMax:
        print("Oprire din cauza atingerii numarului maxim de iteratii.")
        break

    # Verificare pentru oprirea daca s-a atins convergenta
    if len(set(map(tuple, crom_list))) == 1:
        print("Oprire din cauza atingerii convergentei.")
        break

plt.plot(range(0, iteratia), evolutie_adecvare_medie, label='Adecvare Medie')
plt.plot(range(0, iteratia), evolutie_diversitate, label='Diversitate (Distanța Hamming Medie)')
plt.plot(range(0, iteratia), evolutie_convergenta, label='Convergenta (1 - Diversitate Medie)')
plt.xlabel('Iteratie')
plt.ylabel('Valoare')
plt.title('Evoluția Adecvării Medii, Diversității și Convergenței Populației')
plt.legend()
plt.show()
