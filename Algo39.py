# Algo ML for SQL injection and request
# creator : R3dB
# ----- ----- -----  Imports ----- ----- ----- #
import pandas as pd
from pytz import unicode
import random


# ----- ----- -----  Fonctions ----- ----- ----- #

def importation_bdd():
    excel_data = pd.read_excel('data2.xlsx')
    data = pd.DataFrame(excel_data, columns=['Sentence', 'Label'])
    # print("Le contenu du fichier est : \n ", data)
    print("-- -- Fin de la recuperation de la base de donnee ! -- --")
    return data


def aleat(data):
    l = list(range(len(data)))
    random.shuffle(l)
    app = int(len(l) * 0.8)
    app_data = l[0:app]
    trv_data = l[app + 1: len(l)]
    print("-- -- Fin du partitionnage aleatoire ! -- --")
    return app_data, trv_data


def choix_bdd(data, app_data, trv_data):
    data_appAlgo = [0] * len(app_data)
    data_appAlgo_bin = [0] * len(app_data)
    data_testAlgo = [0] * len(trv_data)
    data_testAlgo_bin = [0] * len(trv_data)

    for i in range(0, len(app_data)):
        data_appAlgo[i] = data.iloc[app_data[i], 0]
        data_appAlgo_bin[i] = data.iloc[app_data[i], 1]
    for i in range(0, len(trv_data)):
        data_testAlgo[i] = data.iloc[trv_data[i], 0]
        data_testAlgo_bin[i] = data.iloc[trv_data[i], 1]
    print("-- -- Fin de la separation des deux bdd ! -- --")
    return data_appAlgo, data_appAlgo_bin, data_testAlgo, data_testAlgo_bin


def bag_of_word(bdd_blck, bdd_it, inj_mot_list, inj_it_list, rqt_mot_list, rqt_it_list):
    for i in range(0, len(bdd_it)):
        if bdd_it[i] == 1.0:
            li = bdd_blck[i]
            if type(li) is not float:
                l = unicode.split(li)
                for j in range(0, len(l)):
                    if l[j] in inj_mot_list:
                        rang = inj_mot_list.index(l[j])
                        inj_it_list[rang] += 1
                    else:
                        inj_mot_list.append(l[j])
                        inj_it_list.append(int(1))
        elif bdd_it[i] == 0.0:
            li = bdd_blck[i]
            if type(li) is not float:
                l = unicode.split(li)
                for j in range(0, len(l)):
                    if l[j] in rqt_mot_list:
                        rang = rqt_mot_list.index(l[j])
                        rqt_it_list[rang] += 1
                    else:
                        rqt_mot_list.append(l[j])
                        rqt_it_list.append(int(1))
    print("-- -- Fin de la creation du Bag Of Word !-- --")
    return inj_mot_list, inj_it_list, rqt_mot_list, rqt_it_list


def vecteur_bagof(rqetee, inj_mot_list, inj_it_list, rqt_mot_list, rqt_it_list):
    z = unicode.split(rqetee)
    z_int_g = [0] * len(rqt_it_list)
    z_int_i = [0] * len(inj_it_list)
    for i in range(0, len(z)):
        if z[i] in inj_mot_list:
            z_int_i[inj_mot_list.index(z[i])] += 1
        if z[i] in rqt_mot_list:
            z_int_g[rqt_mot_list.index(z[i])] += 1
    return z_int_i, z_int_g


def par_nb_occurence(ph_int_inj, ph_int_sql):
    somme_occ_injection = sum(ph_int_inj)
    somme_occ_requete = sum(ph_int_sql)
    # print("Injection = ", somme_occ_injection, "mots. // requet normal = ", somme_occ_requete, "mots.")
    if somme_occ_injection > somme_occ_requete:
        return 1
    elif somme_occ_injection < somme_occ_requete:
        return 0
    else:
        return 2


def calcul_freq_occurence_bdd(SQL_inj_it, SQL_good_it):  # calcule des frequences des occurences
    fq_SQL_inj_it = [0] * len(SQL_inj_it)
    fq_SQL_good_it = [0] * len(SQL_good_it)
    somme_total_occ_inj = sum(SQL_inj_it)
    somme_total_occ_rqt = sum(SQL_good_it)
    for i in range(0, len(SQL_inj_it)):
        fq_SQL_inj_it[i] = (SQL_inj_it[i] / somme_total_occ_inj)
    for i in range(0, len(SQL_good_it)):
        fq_SQL_good_it[i] = (SQL_good_it[i] / somme_total_occ_rqt)
    print("-- -- Fin Calcul freq des bag of word !-- --")
    return fq_SQL_inj_it, fq_SQL_good_it


def par_freq(SQL_inj_fq, SQL_good_fq, ph_int_inj, ph_int_sql):
    sum_fq_inj = 0
    sum_fq_rqt = 0
    for i in range(0, len(ph_int_inj)):
        sum_fq_inj += ph_int_inj[i] * SQL_inj_fq[i]
    for i in range(0, len(ph_int_sql)):
        sum_fq_rqt += ph_int_sql[i] * SQL_good_fq[i]
    # print("injection  = ", sum_fq_inj, "/ Requet = ", sum_fq_rqt)
    if sum_fq_inj > sum_fq_rqt:
        return 1
    elif sum_fq_inj < sum_fq_rqt:
        return 0
    else:
        return 2


def ajout_dans_bdd(Entree, tipe, SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it):
    if type(Entree) is not float:
        if tipe == 1:
            l = unicode.split(Entree)
            for j in range(0, len(l)):
                if l[j] in SQL_inj_mot:
                    rang = SQL_inj_mot.index(l[j])
                    SQL_inj_it[rang] += 1
                else:
                    SQL_inj_mot.append(l[j])
                    SQL_inj_it.append(int(1))
        if tipe == 0:
            l = unicode.split(Entree)
            for j in range(0, len(l)):
                if l[j] in SQL_good_mot:
                    rang = SQL_good_mot.index(l[j])
                    SQL_good_it[rang] += 1
                else:
                    SQL_good_mot.append(l[j])
                    SQL_good_it.append(int(1))
    else :
        return
    print("-- -- Fin de l ajout dand Bag Of Word !-- --")
    return SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it


def par_mixte(Entree, SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it, SQL_inj_fq, SQL_good_fq):
    if type(Entree) is not float:
        ph_int_inj, ph_int_sql = vecteur_bagof(Entree, SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it)
        retour_occ = par_nb_occurence(ph_int_inj, ph_int_sql)
        retour_freq = par_freq(SQL_inj_fq, SQL_good_fq, ph_int_inj, ph_int_sql)
        print(retour_occ,retour_freq)
        if retour_occ == retour_freq:
            if retour_occ == 1:
                tipe = 1
            elif retour_occ == 0:
                tipe = 0
            else :
                tipe = 2
        elif retour_occ == 2 or retour_freq == 2:
            if retour_occ == 1:
                tipe = 1
            elif retour_occ == 0:
                tipe = 0
            elif retour_freq == 1:
                tipe = 1
            elif retour_freq == 0:
                tipe = 0
        elif retour_occ == 0 and retour_freq == 1:
            tipe = 1
        elif retour_occ == 1 and retour_freq == 0:
            tipe = 0
        else:
            tipe = 2
        print(tipe)
    return tipe


def tout_app(Entree, SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it, SQL_inj_fq, SQL_good_fq):
    print(Entree)
    tipe = par_mixte(Entree,SQL_inj_mot,  SQL_inj_it, SQL_good_mot, SQL_good_it, SQL_inj_fq, SQL_good_fq)
    if tipe != 2 :
        ajout_dans_bdd(Entree, tipe, SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it)
    return SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it


# ----- ----- -----  Appels ----- ----- ----- #

data = importation_bdd()

app_data, trv_data = aleat(data)

data_appAlgo, data_appAlgo_bin, data_testAlgo, data_testAlgo_bin = choix_bdd(data, app_data, trv_data)
SQL_inj_mot = []  # Liste des mots d'injection
SQL_inj_it = []  # Liste des effectifs d'injections
SQL_good_mot = []  # Liste des mots de requete
SQL_good_it = []  # Liste des effectifs d'injections

bag_of_word(data_appAlgo, data_appAlgo_bin, SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it)
print(sum(SQL_inj_it))
print(sum(SQL_good_it))
for k in range (0,3):
    SQL_inj_fq, SQL_good_fq = calcul_freq_occurence_bdd(SQL_inj_it, SQL_good_it)
    Entree = data_testAlgo[k]
    SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it = tout_app(Entree, SQL_inj_mot, SQL_inj_it, SQL_good_mot, SQL_good_it, SQL_inj_fq, SQL_good_fq)
    print(sum(SQL_inj_it))
    print(sum(SQL_good_it))
