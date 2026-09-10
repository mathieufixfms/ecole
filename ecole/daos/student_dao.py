from dataclasses import dataclass
from typing import Mapping, Optional, cast

from daos.dao import Dao
from models.student import Student
from models.address import Address


@dataclass
class StudentDao(Dao[Student]):
	
	def delete(self, student: Student) -> bool:
		"""Supprime un étudiant de la BD en se basant sur `student_nbr`."""
		
		student_nbr = getattr(student, 'student_nbr', None) or getattr(student, 'id', None)
		
		with Dao.connection.cursor() as cursor:
			sql = "DELETE FROM student WHERE student_nbr = %s"
			
			cursor.execute(sql, (student_nbr,))
			
			Dao.connection.commit()
			
			return cursor.rowcount > 0
	
	def update(self, student: Student) -> bool:
		"""Met à jour le prénom et le nom d'un étudiant."""
		
		with Dao.connection.cursor() as cursor:
			sql = """
				UPDATE person p
				JOIN student s ON s.id_person = p.id_person
				SET p.first_name = %s,
					p.last_name = %s,
					p.age = %s
				WHERE s.student_nbr = %s
			"""
			
			cursor.execute(
				sql,
				(student.first_name, student.last_name, student.age, student.student_nbr),
			)
			
			Dao.connection.commit()
			
			return cursor.rowcount > 0
	
	def create(self, student: Student) -> int:
		"""Crée un étudiant, sa personne et son adresse éventuelle."""
		
		try:
			with Dao.connection.cursor() as cursor:
				address_id = None
				
				if student.address is not None:
					cursor.execute(
						"""
						SELECT id_address
						FROM address
						WHERE street = %s
						  AND city = %s
						  AND postal_code = %s
						LIMIT 1
						""",
						(
							student.address.street,
							student.address.city,
							student.address.postal_code,
						),
					)
					existing_address = cursor.fetchone()
					
					if existing_address is not None:
						address_id = cast(Mapping[str, int], existing_address)["id_address"]
					else:
						cursor.execute(
							"""
							INSERT INTO address (street, city, postal_code)
							VALUES (%s, %s, %s)
							""",
							(
								student.address.street,
								student.address.city,
								student.address.postal_code,
							),
						)
						address_id = cursor.lastrowid
					
					student.address.id = address_id
				
				# Calcule le numéro après l'adresse et avant l'étudiant.
				cursor.execute(
					"SELECT COALESCE(MAX(student_nbr), 0) + 1 AS next_student_nbr "
					"FROM student"
				)
				next_student = cast(Mapping[str, int], cursor.fetchone())
				student.student_nbr = next_student["next_student_nbr"]
				
				cursor.execute(
					"""
					INSERT INTO person (first_name, last_name, age, id_address)
					VALUES (%s, %s, %s, %s)
					""",
					(
						student.first_name,
						student.last_name,
						student.age,
						address_id,
					),
				)
				id_person = cursor.lastrowid
				
				cursor.execute(
					"INSERT INTO student (student_nbr, id_person) VALUES (%s, %s)",
					(student.student_nbr, id_person),
				)
			
			Dao.connection.commit()
			return student.student_nbr
		except Exception:
			Dao.connection.rollback()
			raise
	
	def read(self, student_nbr: int) -> Optional[Student]:
		student: Optional[Student]
		
		with Dao.connection.cursor() as cursor:
			sql = """
				SELECT s.student_nbr,
				       p.first_name,
				       p.last_name,
				       p.age,
				       a.id_address,
				       a.street,
				       a.city,
				       a.postal_code
				FROM student s
				LEFT JOIN person p ON s.id_person = p.id_person
				LEFT JOIN address a ON p.id_address = a.id_address
				WHERE s.student_nbr = %s
			"""
			
			cursor.execute(sql, (student_nbr,))
			record = cursor.fetchone()
		
		if record is None:
			student = None
		else:
			student = Student(
				record['first_name'],  # type: ignore
				record['last_name'],  # type: ignore
				record['age'],  # type: ignore
			)
			# override the auto-generated student number with DB value
			student.student_nbr = record['student_nbr']  # type: ignore
			
			# attach address if present
			if record.get('id_address') is not None:  # type: ignore
				addr = Address(
					record['street'],  # type: ignore
					record['city'],  # type: ignore
					record['postal_code'],  # type: ignore
				)
				addr.id = record['id_address']  # type: ignore
				student.address = addr
		
		return student