import csv
import os
from collections import Counter
import matplotlib.pyplot as plt


def search_student(file_path, identifier):
    """
    Recherche un étudiant par son NNI
    ou son Num_Bac et affiche ses informations.
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
    Vérifie le statut d'admission et la moyenne d'un étudiant par
    NNI ou Num_Bac.
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


def plot_decision_stats(decision_counts, total_students):
    labels = [
        'Admis', 'Sessionnaire', 'Ajourné', 'Abscent'
    ]
    admis_count = sum(
        count for dec, count in decision_counts.items() if dec.startswith('Admis')
        )
    sessionnaire_count = decision_counts['Sessionnaire']
    ajourne_count = sum(
        count for dec, count in decision_counts.items() if dec.startswith('Ajourné')
    )
    abscent_count = decision_counts['Abscent']
    sizes = [admis_count, sessionnaire_count, ajourne_count, abscent_count]
    colors = ['#4CAF50', '#FFC107', '#F44336', '#9E9E9E']
    explode = (0.1, 0, 0, 0)  # explode 1st slice

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=140, textprops={'fontsize': 12})
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Répartition des décisions du BAC 2024', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/statistiques_decisions.png')
    print("\nGraphique 'images/statistiques_decisions.png' généré.")


def plot_stats_by_category(data, category_key, title, filename):
    categories = sorted(list(set(row[category_key] for row in data)))
    percentages = []
    for category in categories:
        category_students = [row for row in data if row[category_key] == category]
        total_category = len(category_students)
        if total_category > 0:
            admis_category = sum(1 for row in category_students if row['Decision'].startswith('Admis'))
            percentages.append((admis_category / total_category) * 100)
        else:
            percentages.append(0)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(categories, percentages, color='#4CAF50')
    ax.set_xlabel('Pourcentage d\'admis (%)', fontsize=12)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.2f}%',
                va='center', ha='left', fontsize=10)

    plt.tight_layout()
    plt.savefig(f'images/{filename}')
    print(f"Graphique 'images/{filename}' généré.")


def calculate_and_plot_statistics(file_path):
    """
    Calcule et affiche les statistiques
    sur les résultats du bac, et génère des graphiques.
    """
    if not os.path.exists('images'):
        os.makedirs('images')

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        total_students = len(data)

        decision_counts = Counter(row['Decision'] for row in data)
        plot_decision_stats(decision_counts, total_students)
        plot_stats_by_category(
            data, 'SERIE',
            'Pourcentage d\'admis par série',
            'statistiques_series.png'
        )
        plot_stats_by_category(
            data, 'Wilaya_FR',
            'Pourcentage d\'admis par Wilaya',
            'statistiques_wilayas.png'
        )
        plot_stats_by_category(
            data, 'Noreg',
            'Pourcentage d\'admis par Noreg',
            'statistiques_noregs.png'
        )


if __name__ == "__main__":
    FILE_PATH = 'RESULTATS_BAC_2024_SESSION_NORMALE.csv'

    while True:
        print("\n--- Menu ---")
        print("1. Rechercher toutes les informations d'un étudiant")
        print("2. Vérifier le statut d'admission d'un étudiant")
        print("3. Afficher les statistiques et générer les graphiques")
        print("4. Quitter")

        choice = input("Entrez votre choix (1-4) : ")

        if choice == '1':
            student_id = input("Entrez le NNI ou le Num_Bac de l'étudiant : ")
            search_student(FILE_PATH, student_id)
        elif choice == '2':
            student_id = input("Entrez le NNI ou le Num_Bac de l'étudiant : ")
            check_admission_status(FILE_PATH, student_id)
        elif choice == '3':
            calculate_and_plot_statistics(FILE_PATH)
        elif choice == '4':
            print("Au revoir !")
            break
        else:
            print("Choix non valide. Veuillez réessayer.")
