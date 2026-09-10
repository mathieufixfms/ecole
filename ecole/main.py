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


def update_student_name(school: School) -> None:
	"""Demande confirmation puis modifie le prénom et le nom d'un étudiant."""
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


def create_student(school: School) -> None:
	"""Demande confirmation puis crée un étudiant avec son adresse."""
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
	"""Demande confirmation puis crée un enseignant avec son adresse."""
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
	"""Demande confirmation puis supprime un étudiant sélectionné."""
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
	"""Demande confirmation puis supprime un enseignant sélectionné."""
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


def main() -> None:
	"""Programme principal."""
	print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")
	
	school: School = School()
	
	# Demande de création d'un étudiant
	create_student(school)
	
	# Demande de création d'un enseignant
	create_teacher(school)
	
	# Demande de suppression d'un étudiant
	delete_student(school)
	
	# Demande de suppression d'un enseignant
	delete_teacher(school)
	
	# Demande d'ajout d'un cours
	# try:
	# id_teacher = int(input("Entrez l'id de l'enseignant du cours : "))
	# except ValueError:
	# print("L'id de l'enseignant doit être un nombre entier.")
	# else:
	# teacher = school.get_teacher_by_id(id_teacher)
	# if teacher is None:
	# print(f"Aucun enseignant trouvé avec l'id {id_teacher}.")
	# else:
	# informatique = Course("Informatique", date(2026, 9, 15), date(2026, 10, 15))
	# informatique.set_teacher(teacher)
	# informatique.id = CourseDao().create(informatique)
	# print(f"Cours ajouté : {informatique}")
	
	# Demande de modification de la ville d'une adresse
	# try:
	# 	id_address = int(input("Entrez l'id de l'adresse à modifier : "))
	# 	new_city = input("Entrez la nouvelle ville : ").strip()
	# except ValueError:
	# 	print("L'id de l'adresse doit être un nombre entier.")
	# else:
	# 	address_to_update = school.get_address_by_id(id_address)
	# 	if address_to_update is None:
	# 		print(f"Aucune adresse trouvée avec l'id {id_address}.")
	# 	elif not new_city:
	# 		print("La ville ne peut pas être vide.")
	# 	else:
	# 		address_to_update.city = new_city
	# 		updated = AddressDao().update(address_to_update)
	# 		print("Ville mise à jour." if updated else "La ville n'a pas été mise à jour.")
	
	# Demande de modification du code postal d'une adresse
	# try:
	# 	id_address = int(input("Entrez l'id de l'adresse à modifier : "))
	# 	new_postal_code = int(input("Entrez le nouveau code postal : "))
	# except ValueError:
	# 	print("L'id et le code postal doivent être des nombres entiers.")
	# else:
	# 	address_to_update = school.get_address_by_id(id_address)
	# 	if address_to_update is None:
	# 		print(f"Aucune adresse trouvée avec l'id {id_address}.")
	# 	else:
	# 		address_to_update.postal_code = new_postal_code
	# 		updated = AddressDao().update(address_to_update)
	# 		print(
	# 			"Code postal mis à jour."
	# 			if updated else "Le code postal n'a pas été mis à jour."
	#		)
	
	# Demande de modification du nom d'un étudiant
	update_student_name(school)
	
	# initialisation d'un ensemble de cours, enseignants et élèves composant l'école
	# school.init_static()
	
	# affichage de la liste des cours, leur enseignant et leurs élèves
	# school.display_courses_list()
	
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


if __name__ == '__main__':
	main()



