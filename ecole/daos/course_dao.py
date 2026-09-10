# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.course import Course
from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class CourseDao(Dao[Course]):

    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course"""

        if course.teacher is None or course.teacher.id is None:
            raise ValueError("Le cours doit avoir un enseignant enregistré.")

        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                      INSERT INTO course (name, start_date, end_date, id_teacher)
                      VALUES (%s, %s, %s, %s) \
                      """

                cursor.execute(
                    sql,
                    (
                        course.name,
                        course.start_date,
                        course.end_date,
                        course.teacher.id,
                    ),
                )

                course_id = cursor.lastrowid
                course.id = course_id

            Dao.connection.commit()
            return course_id
        except Exception:
            Dao.connection.rollback()
            raise

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoie le cours correspondant à l'id fourni"""

        course: Optional[Course]

        with Dao.connection.cursor() as cursor:
            sql = """
                  SELECT c.id_course,
                         c.name,
                         c.start_date,
                         c.end_date,
                         t.id_teacher,
                         t.hiring_date,
                         p.first_name,
                         p.last_name,
                         p.age
                  FROM course c
                           LEFT JOIN teacher t ON c.id_teacher = t.id_teacher
                           LEFT JOIN person p ON t.id_person = p.id_person
                  WHERE c.id_course = %s \
                  """

            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()

        if record is not None:
            course = Course(
                record['name'], # type: ignore
                record['start_date'], # type: ignore
                record['end_date'] # type: ignore
            )
            course.id = record['id_course'] # type: ignore

            if record['id_teacher'] is not None: # type: ignore
                teacher = Teacher(
                    record['first_name'], # type: ignore
                    record['last_name'], # type: ignore
                    record['age'], # type: ignore
                    record['hiring_date'], # type: ignore
                )
                teacher.id = record['id_teacher'] # type: ignore
                course.teacher = teacher
        else:
            course = None

        return course


    def update(self, course: Course) -> bool:
        """Met à jour un cours en BD"""

        with Dao.connection.cursor() as cursor:
            sql = """
                  UPDATE course
                  SET name = %s,
                      start_date = %s,
                      end_date = %s
                  WHERE id_course = %s \
                  """

            cursor.execute(
                sql,
                (
                    course.name,
                    course.start_date,
                    course.end_date,
                    course.id
                )
            )

            Dao.connection.commit()

            return cursor.rowcount > 0

    def delete(self, course: Course) -> bool:
        """Supprime un cours de la BD"""

        with Dao.connection.cursor() as cursor:
            sql = "DELETE FROM course WHERE id_course = %s"

            cursor.execute(sql, (course.id,))

            Dao.connection.commit()

            return cursor.rowcount > 0