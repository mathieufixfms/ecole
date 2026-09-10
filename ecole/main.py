#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from datetime import date, datetime

from business import school
from business.school import School
from daos.dao import Dao
from daos.address_dao import AddressDao
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
from models.address import Address
from models.course import Course
from models.student import Student
from models.teacher import Teacher


def create_student(school: School) -> None:
	""" 1 : crée un étudiant avec son adresse."""
	create_confirmation = input("Voulez-vous créer un étudiant ? (oui/non) : ").strip().lower()
	if create_confirmation not in ("oui", "o", "y"):
		print("Création de l'étudiant annulée.")
		return
	
	first_name = input("Entrez le prénom de l'étudiant : ").strip()
	last_name = input("Entrez le nom de l'étudiant : ").strip()
	try:
		age = int(input("Entrez l'âge de l'étudiant : "))
		postal_code = int(input("Entrez le code postal : "))
	except ValueError:
		print("L'âge et le code postal doivent être des nombres entiers.")
		return
	
	street = input("Entrez la rue : ").strip()
	city = input("Entrez la ville : ").strip()
	if not first_name or not last_name or not street or not city:
		print("Le prénom, le nom, la rue et la ville sont obligatoires.")
		return
	if age < 0 or postal_code < 0:
		print("L'âge et le code postal doivent être positifs.")
		return
	
	student = Student(first_name, last_name, age)
	student.address = Address(street, city, postal_code)
	StudentDao().create(student)
	school.add_student(student)
	print(f"Étudiant ajouté : {student}")


def create_teacher(school: School) -> None:
	""" 2 : crée un enseignant avec son adresse."""
	create_confirmation = input("Voulez-vous créer un enseignant ? (oui/non) : ").strip().lower()
	if create_confirmation not in ("oui", "o", "y"):
		print("Création de l'enseignant annulée.")
		return
	
	first_name = input("Entrez le prénom de l'enseignant : ").strip()
	last_name = input("Entrez le nom de l'enseignant : ").strip()
	try:
		age = int(input("Entrez l'âge de l'enseignant : "))
		hiring_date = datetime.strptime(
			input("Entrez la date d'embauche (AAAA-MM-JJ) : "),
			"%Y-%m-%d",
		).date()
		postal_code = int(input("Entrez le code postal : "))
	except ValueError:
		print("L'âge, le code postal ou la date d'embauche est invalide.")
		return
	
	street = input("Entrez la rue : ").strip()
	city = input("Entrez la ville : ").strip()
	if not first_name or not last_name or not street or not city:
		print("Le prénom, le nom, la rue et la ville sont obligatoires.")
		return
	if age < 0 or postal_code < 0:
		print("L'âge et le code postal doivent être positifs.")
		return
	
	teacher = Teacher(first_name, last_name, age, hiring_date)
	teacher.address = Address(street, city, postal_code)
	TeacherDao().create(teacher)
	school.add_teacher(teacher)
	school.add_address(teacher.address)
	print(f"Enseignant ajouté : {teacher}")


def delete_student(school: School) -> None:
	""" 3 : supprime un étudiant sélectionné."""
	delete_confirmation = input("Voulez-vous supprimer un étudiant ? (oui/non) : ").strip().lower()
	if delete_confirmation not in ("oui", "o", "y"):
		print("Suppression de l'étudiant annulée.")
		return
	
	try:
		student_nbr = int(input("Entrez le numéro de l'étudiant à supprimer : "))
	except ValueError:
		print("Le numéro de l'étudiant doit être un nombre entier.")
		return
	
	student_to_delete = school.get_student_by_id(student_nbr)
	if student_to_delete is None:
		print(f"Aucun étudiant trouvé avec le numéro {student_nbr}.")
		return
	
	print(
		f"Étudiant sélectionné : prénom = {student_to_delete.first_name}, "
		f"nom = {student_to_delete.last_name}, âge = {student_to_delete.age}, "
		f"adresse = {student_to_delete.address}"
	)
	final_confirmation = input("Confirmez-vous la suppression ? (oui/non) : ").strip().lower()
	if final_confirmation not in ("oui", "o", "y"):
		print("Suppression de l'étudiant annulée.")
		return
	
	deleted = StudentDao().delete(student_to_delete)
	print("L'étudiant a été supprimé avec succès." if deleted else "L'étudiant n'a pas été supprimé.")


def delete_teacher(school: School) -> None:
	""" 4 : demande confirmation puis supprime un enseignant sélectionné."""
	delete_confirmation = input("Voulez-vous supprimer un enseignant ? (oui/non) : ").strip().lower()
	if delete_confirmation not in ("oui", "o", "y"):
		print("Suppression de l'enseignant annulée.")
		return
	
	try:
		teacher_id = int(input("Entrez l'id de l'enseignant à supprimer : "))
	except ValueError:
		print("L'id de l'enseignant doit être un nombre entier.")
		return
	
	teacher_to_delete = school.get_teacher_by_id(teacher_id)
	if teacher_to_delete is None:
		print(f"Aucun enseignant trouvé avec l'id {teacher_id}.")
		return
	
	print(
		f"Enseignant sélectionné : prénom = {teacher_to_delete.first_name}, "
		f"nom = {teacher_to_delete.last_name}, âge = {teacher_to_delete.age}, "
		f"date d'embauche = {teacher_to_delete.hiring_date}, "
		f"adresse = {teacher_to_delete.address}"
	)
	final_confirmation = input("Confirmez-vous la suppression ? (oui/non) : ").strip().lower()
	if final_confirmation not in ("oui", "o", "y"):
		print("Suppression de l'enseignant annulée.")
		return
	
	deleted = TeacherDao().delete(teacher_to_delete)
	print("Enseignant supprimé." if deleted else "L'enseignant n'a pas été supprimé.")


def create_course(school: School) -> None:
	""" 5 : crée un cours associé à un enseignant."""
	create_confirmation = input("Voulez-vous ajouter un cours ? (oui/non) : ").strip().lower()
	if create_confirmation not in ("oui", "o", "y"):
		print("Ajout du cours annulé.")
		return
	
	try:
		teacher_id = int(input("Entrez l'id de l'enseignant du cours : "))
	except ValueError:
		print("L'id de l'enseignant doit être un nombre entier.")
		return
	
	teacher = school.get_teacher_by_id(teacher_id)
	if teacher is None:
		print(f"Aucun enseignant trouvé avec l'id {teacher_id}.")
		return
	
	informatique = Course("Informatique", date(2026, 9, 15), date(2026, 10, 15))
	informatique.set_teacher(teacher)
	informatique.id = CourseDao().create(informatique)
	print(f"Cours ajouté : {informatique}")


def update_address_city(school: School) -> None:
	""" 6 : modifie la ville d'une adresse."""
	update_confirmation = input("Voulez-vous modifier une ville d'une adresse ? (oui/non) : ").strip().lower()
	if update_confirmation not in ("oui", "o", "y"):
		print("Modification de la ville annulée.")
		return
	
	try:
		address_id = int(input("Entrez l'id de l'adresse comprennant la ville à modifier : "))
	except ValueError:
		print("L'id de l'adresse doit être un nombre entier.")
		return
	
	address_to_update = school.get_address_by_id(address_id)
	if address_to_update is None:
		print(f"Aucune adresse trouvée avec l'id {address_id}.")
		return
	
	print(f"Ville actuelle : {address_to_update.city}")
	new_city = input("Entrez la nouvelle ville : ").strip()
	if not new_city:
		print("La ville ne peut pas être vide.")
	else:
		address_to_update.city = new_city
		updated = AddressDao().update(address_to_update)
		print("Ville mise à jour." if updated else "La ville n'a pas été mise à jour.")


def update_address_postal_code(school: School) -> None:
	""" 7 : modifie le code postal d'une adresse."""
	update_confirmation = input("Voulez-vous modifier le code postal d'une adresse ? (oui/non) : ").strip().lower()
	if update_confirmation not in ("oui", "o", "y"):
		print("Modification du code postal annulée.")
		return
	
	try:
		address_id = int(input("Entrez l'id de l'adresse correspondant au code postal à modifier : "))
	except ValueError:
		print("L'id de l'adresse doit être un nombre entier.")
		return
	
	address_to_update = school.get_address_by_id(address_id)
	if address_to_update is None:
		print(f"Aucune adresse trouvée avec l'id {address_id}.")
	else:
		print(f"Code postal actuel : {address_to_update.postal_code}")
		try:
			new_postal_code = int(input("Entrez le nouveau code postal : "))
		except ValueError:
			print("Le code postal doit être un nombre entier.")
			return
		
		address_to_update.postal_code = new_postal_code
		updated = AddressDao().update(address_to_update)
		print(
			"Code postal mis à jour."
			if updated else "Le code postal n'a pas été mis à jour."
		)


def update_student_name(school: School) -> None:
	""" 8 : modifie le prénom et le nom d'un étudiant."""
	modify_student = input("Voulez-vous modifier un étudiant ? (oui/non) : ").strip().lower()
	if modify_student not in ("oui", "o", "y"):
		print("Modification de l'étudiant annulée.")
		return
	
	try:
		student_nbr = int(input("Entrez le numéro de l'étudiant à modifier : "))
	except ValueError:
		print("Le numéro de l'étudiant doit être un nombre entier.")
		return
	
	student_to_update = school.get_student_by_id(student_nbr)
	if student_to_update is None:
		print(f"Aucun étudiant trouvé avec le numéro {student_nbr}.")
		return
	
	print(
		f"Étudiant trouvé : prénom = {student_to_update.first_name}, "
		f"nom = {student_to_update.last_name}"
	)
	new_first_name = input("Entrez le nouveau prénom : ").strip()
	new_last_name = input("Entrez le nouveau nom : ").strip()
	if not new_first_name or not new_last_name:
		print("Le prénom et le nom ne peuvent pas être vides.")
		return
	
	student_to_update.first_name = new_first_name
	student_to_update.last_name = new_last_name
	updated = StudentDao().update(student_to_update)
	print("Nom et prénom ont été mis à jour." if updated else "Le nom et prénom n'ont pas été mis à jour.")


def display_school_data(school: School) -> None:
	""" 9 : Affiche quelques données de l'école."""
	print("cours :")
	print(school.get_course_by_id(1))
	print(school.get_course_by_id(2))
	print(school.get_course_by_id(9))
	print()
	
	print("adresse :")
	print(school.get_address_by_id(1))
	print(school.get_address_by_id(2))
	print(school.get_address_by_id(3))
	print()
	
	print("étudiant :")
	print(school.get_student_by_id(4))
	print()
	
	print("professeur :")
	print(school.get_teacher_by_id(1))
	print(school.get_teacher_by_id(8))


def main() -> None:
	"""Programme principal."""
	print("""\
""")
	school: School = School()
	while True:
		print("""
+------------------------------------------+
|       Bienvenue dans notre école         |
+------------------------------------------+
|                  MENU                    |
+------------------------------------------+
|1 | Créer un étudiant                     |
|2 | Créer un enseignant                   |
|3 | Supprimer un étudiant                 |
|4 | Supprimer un enseignant               |
|5 | Ajouter un cours                      |
|6 | Modifier la ville d'une adresse       |
|7 | Modifier le code postal d'une adresse |
|8 | Modifier le nom d'un étudiant         |
|9 | Afficher des données de l'école       |
|0 | Quitter                               |
+------------------------------------------+
""")
		
		choice = input("Choisissez une action : ").strip()
		if choice == "1":
			create_student(school)
		elif choice == "2":
			create_teacher(school)
		elif choice == "3":
			delete_student(school)
		elif choice == "4":
			delete_teacher(school)
		elif choice == "5":
			create_course(school)
		elif choice == "6":
			update_address_city(school)
		elif choice == "7":
			update_address_postal_code(school)
		elif choice == "8":
			update_student_name(school)
		elif choice == "9":
			display_school_data(school)
		elif choice == "0":
			print("Au revoir merci !")
			break
		else:
			print("Choix invalide. Veuillez sélectionner une option du menu.")


if __name__ == '__main__':
	main()



