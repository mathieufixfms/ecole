from dataclasses import dataclass
from typing import Mapping, Optional, cast

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
						SELECT id_address
						FROM address
						WHERE street = %s
						  AND city = %s
						  AND postal_code = %s
						LIMIT 1
						""",
						(
							teacher.address.street,
							teacher.address.city,
							teacher.address.postal_code,
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
                WHERE t.id_teacher = %s
            """
			
			cursor.execute(sql, (id_teacher,))
			record = cursor.fetchone()
		
		if record is None:
			return None
		
		teacher = Teacher(
			record['first_name'],  # type: ignore
			record['last_name'],  # type: ignore
			record['age'],  # type: ignore
			record['hiring_date'],  # type: ignore
		)
		teacher.id = record['id_teacher']  # type: ignore
		
		if record.get('id_address') is not None:  # type: ignore
			address = Address(
				record['street'],  # type: ignore
				record['city'],  # type: ignore
				record['postal_code'],  # type: ignore
			)
			address.id = record['id_address']  # type: ignore
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
                WHERE id_teacher = %s
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
		"""Supprime l'enseignant, sa personne et son adresse si inutilisée."""
		
		try:
			with Dao.connection.cursor() as cursor:
				cursor.execute(
					"""
					SELECT t.id_person, p.id_address
					FROM teacher t
					JOIN person p ON t.id_person = p.id_person
					WHERE t.id_teacher = %s
					""",
					(teacher.id,),
				)
				teacher_record = cursor.fetchone()
				if teacher_record is None:
					return False
				
				relations = cast(Mapping[str, Optional[int]], teacher_record)
				id_person = relations["id_person"]
				id_address = relations["id_address"]
				
				cursor.execute(
					"DELETE FROM teacher WHERE id_teacher = %s",
					(teacher.id,),
				)
				teacher_deleted = cursor.rowcount > 0
				
				if id_person is not None:
					cursor.execute("DELETE FROM person WHERE id_person = %s", (id_person,))
				
				if id_address is not None:
					cursor.execute(
						"SELECT COUNT(*) AS references_count FROM person WHERE id_address = %s",
						(id_address,),
					)
					references = cast(Mapping[str, int], cursor.fetchone())
					if references["references_count"] == 0:
						cursor.execute(
							"DELETE FROM address WHERE id_address = %s",
							(id_address,),
						)
			
			Dao.connection.commit()
			return teacher_deleted
		except Exception:
			Dao.connection.rollback()
			raise