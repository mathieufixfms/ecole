from dataclasses import dataclass
from typing import Optional

from daos.dao import Dao
from models.address import Address
from models.teacher import Teacher


@dataclass
class TeacherDao(Dao[Teacher]):

	def create(self, teacher: Teacher) -> int:
		"""Crée un enseignant en BD et renvoie son id."""
		try:
			with Dao.connection.cursor() as cursor:
				address_id = None

				if teacher.address is not None:
					cursor.execute(
						"""
						INSERT INTO address (street, city, postal_code)
						VALUES (%s, %s, %s)
						""",
						(
							teacher.address.street,
							teacher.address.city,
							teacher.address.postal_code,
						),
					)
					address_id = cursor.lastrowid
					teacher.address.id = address_id

				cursor.execute(
					"""
					INSERT INTO person (first_name, last_name, age, id_address)
					VALUES (%s, %s, %s, %s)
					""",
					(
						teacher.first_name,
						teacher.last_name,
						teacher.age,
						address_id,
					),
				)
				id_person = cursor.lastrowid

				cursor.execute(
					"""
					INSERT INTO teacher (hiring_date, id_person)
					VALUES (%s, %s)
					""",
					(teacher.hiring_date, id_person),
				)
				teacher.id = cursor.lastrowid

			Dao.connection.commit()
			return teacher.id
		except Exception:
			Dao.connection.rollback()
			raise

	def read(self, id_teacher: int) -> Optional[Teacher]:
		"""Renvoie un enseignant avec sa personne et son adresse."""

		with Dao.connection.cursor() as cursor:
			sql = """
				  SELECT t.id_teacher,
						 t.hiring_date,
						 p.first_name,
						 p.last_name,
						 p.age,
						 a.id_address,
						 a.street,
						 a.city,
						 a.postal_code
				  FROM teacher t
						   LEFT JOIN person p ON t.id_person = p.id_person
						   LEFT JOIN address a ON p.id_address = a.id_address
				  WHERE t.id_teacher = %s \
				  """

			cursor.execute(sql, (id_teacher,))
			record = cursor.fetchone()

		if record is None:
			return None

		teacher = Teacher(
			record['first_name'], # type: ignore
			record['last_name'], # type: ignore
			record['age'], # type: ignore
			record['hiring_date'], # type: ignore
		)
		teacher.id = record['id_teacher'] # type: ignore

		if record.get('id_address') is not None: # type: ignore
			address = Address(
				record['street'], # type: ignore
				record['city'], # type: ignore
				record['postal_code'], # type: ignore
			)
			address.id = record['id_address'] # type: ignore
			teacher.address = address

		return teacher




	def update(self, teacher: Teacher) -> bool:
		"""Met à jour un enseignant en BD."""

		with Dao.connection.cursor() as cursor:
			sql = """
				  UPDATE teacher
				  SET first_name = %s,
					  last_name = %s,
					  age = %s,
					  hiring_date = %s
				  WHERE id_teacher = %s \
				  """

			cursor.execute(
				sql,
				(
					teacher.first_name,
					teacher.last_name,
					teacher.age,
					teacher.hiring_date,
					teacher.id,
				),
			)

			Dao.connection.commit()

			return cursor.rowcount > 0

	def delete(self, teacher: Teacher) -> bool:
		"""Supprime un enseignant de la BD."""

		with Dao.connection.cursor() as cursor:
			sql = "DELETE FROM teacher WHERE id_teacher = %s"

			cursor.execute(sql, (teacher.id,))

			Dao.connection.commit()

			return cursor.rowcount > 0