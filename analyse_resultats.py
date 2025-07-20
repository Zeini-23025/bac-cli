

import csv
from collections import Counter

def search_student(file_path, identifier):
    """
    Recherche un étudiant par son NNI ou son Num_Bac et affiche ses informations.
    """
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        found = False
        for row in reader:
            if row['NNI'] == identifier or row['Num_Bac'] == identifier:
                print("Informations de l'étudiant :")
                for key, value in row.items():
                    print(f"  {key}: {value}")
                print("-" * 20)
                found = True
    
    if not found:
        print(f"Aucun étudiant trouvé avec l'identifiant : {identifier}")

def check_admission_status(file_path, identifier):
    """
    Vérifie le statut d'admission et la moyenne d'un étudiant par NNI ou Num_Bac.
    """
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        found = False
        for row in reader:
            if row['NNI'] == identifier or row['Num_Bac'] == identifier:
                print(f"Résultat pour l'étudiant {row['Nom_FR']}:")
                print(f"  Décision: {row['Decision']}")
                print(f"  Moyenne: {row['Moy_Bac']}")
                print("-" * 20)
                found = True
                return
    
    if not found:
        print(f"Aucun étudiant trouvé avec l'identifiant : {identifier}")

def calculate_statistics(file_path):
    """
    Calcule et affiche les statistiques sur les résultats du bac.
    """
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        total_students = len(data)

        # 1. Pourcentage des admis, sessionnaires, ajournés, absents
        decision_counts = Counter(row['Decision'] for row in data)
        admis_count = sum(count for dec, count in decision_counts.items() if dec.startswith('Admis'))
        sessionnaire_count = decision_counts['Sessionnaire']
        ajourne_count = sum(count for dec, count in decision_counts.items() if dec.startswith('Ajourné'))
        abscent_count = decision_counts['Abscent']

        print("\n--- Statistiques Générales ---")
        print(f"Nombre total d'étudiants: {total_students}")
        print(f"Pourcentage d'admis: {(admis_count / total_students) * 100:.2f}%")
        print(f"Pourcentage de sessionnaires: {(sessionnaire_count / total_students) * 100:.2f}%")
        print(f"Pourcentage d'ajournés: {(ajourne_count / total_students) * 100:.2f}%")
        print(f"Pourcentage d'absents: {(abscent_count / total_students) * 100:.2f}%")

        # 2. Pourcentage des admis par série
        series = sorted(list(set(row['SERIE'] for row in data)))
        print("\n--- Pourcentage d'admis par série ---")
        for serie in series:
            serie_students = [row for row in data if row['SERIE'] == serie]
            total_serie = len(serie_students)
            if total_serie > 0:
                admis_serie = sum(1 for row in serie_students if row['Decision'].startswith('Admis'))
                print(f"  {serie}: {(admis_serie / total_serie) * 100:.2f}%")

        # 3. Pourcentage des admis par Wilaya
        wilayas = sorted(list(set(row['Wilaya_FR'] for row in data)))
        print("\n--- Pourcentage d'admis par Wilaya ---")
        for wilaya in wilayas:
            wilaya_students = [row for row in data if row['Wilaya_FR'] == wilaya]
            total_wilaya = len(wilaya_students)
            if total_wilaya > 0:
                admis_wilaya = sum(1 for row in wilaya_students if row['Decision'].startswith('Admis'))
                print(f"  {wilaya}: {(admis_wilaya / total_wilaya) * 100:.2f}%")

        # 4. Pourcentage des admis par Noreg
        noregs = sorted(list(set(row['Noreg'] for row in data)))
        print("\n--- Pourcentage d'admis par Noreg ---")
        for noreg in noregs:
            noreg_students = [row for row in data if row['Noreg'] == noreg]
            total_noreg = len(noreg_students)
            if total_noreg > 0:
                admis_noreg = sum(1 for row in noreg_students if row['Decision'].startswith('Admis'))
                print(f"  Noreg {noreg}: {(admis_noreg / total_noreg) * 100:.2f}%")

if __name__ == "__main__":
    FILE_PATH = 'RESULTATS_BAC_2024_SESSION_NORMALE.csv'
    
    while True:
        print("\n--- Menu ---")
        print("1. Rechercher toutes les informations d'un étudiant")
        print("2. Vérifier le statut d'admission d'un étudiant")
        print("3. Afficher les statistiques")
        print("4. Quitter")
        
        choice = input("Entrez votre choix (1-4) : ")
        
        if choice == '1':
            student_id = input("Entrez le NNI ou le Num_Bac de l'étudiant : ")
            search_student(FILE_PATH, student_id)
        elif choice == '2':
            student_id = input("Entrez le NNI ou le Num_Bac de l'étudiant : ")
            check_admission_status(FILE_PATH, student_id)
        elif choice == '3':
            calculate_statistics(FILE_PATH)
        elif choice == '4':
            print("Au revoir !")
            break
        else:
            print("Choix non valide. Veuillez réessayer.")
