#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from datetime import date

from business import school
from business.school import School
from daos.dao import Dao
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
from models.address import Address
from models.course import Course
from models.student import Student
from models.teacher import Teacher



def main() -> None:
	"""Programme principal."""
	print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

	school: School = School()

	# Création de Bob avec son adresse, puis enregistrement en base.
	#bob = Student("Bob", "Marley", 14)
	#bob.address = Address("1 rue des Ecoles", "Toulouse", 31000)
	#school.add_student(bob)
	#StudentDao().create(bob)
	#print(f"Etudiant ajoute : {bob}")

	# Création d'un teacher avec sa personne et son adresse.
	#jeanne = Teacher("jeanne", "D'arc", 40, date(2026, 9, 9))
	#jeanne.address = Address("2 rue du buchet", "Toulouse", 31000)
	#school.add_teacher(jeanne)
	#school.add_address(jeanne.address)
	#school.persons.append(jeanne)
	#TeacherDao().create(jeanne)
	#print(f"Teacher ajoute : {jeanne}")

	## Suppression d'un student de la BD
	#print("suppression de l'étudiant :")
	#student_to_delete = school.get_student_by_id(5)
	#if student_to_delete is None:
	#print("Aucun étudiant trouvé avec l'id 5.")
	#else:
	#deleted = StudentDao().delete(student_to_delete)
	#print("Étudiant 5 supprimé." if deleted else "L'étudiant 5 n'a pas été supprimé.")

	# Suppression d'un teacher de la BD
	#print("suppression de l'enseignant :")
	#teacher_to_delete = school.get_teacher_by_id(7)
	#if teacher_to_delete is None:
	#print("Aucun enseignant trouvé avec l'id 7.")
	#else:
	#print("Enseignant 7 supprimé.")

	# Demande d'ajout d'un cours
	#try:
	#id_teacher = int(input("Entrez l'id de l'enseignant du cours : "))
	#except ValueError:
	#print("L'id de l'enseignant doit être un nombre entier.")
	#else:
	#teacher = school.get_teacher_by_id(id_teacher)
	#if teacher is None:
	#print(f"Aucun enseignant trouvé avec l'id {id_teacher}.")
	#else:
	#informatique = Course("Informatique", date(2026, 9, 15), date(2026, 10, 15))
	#informatique.set_teacher(teacher)
	#informatique.id = CourseDao().create(informatique)
	#print(f"Cours ajouté : {informatique}")



	# initialisation d'un ensemble de cours, enseignants et élèves composant l'école
	#school.init_static()

	# affichage de la liste des cours, leur enseignant et leurs élèves
	#school.display_courses_list()

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



