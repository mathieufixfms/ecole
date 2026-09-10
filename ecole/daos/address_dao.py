# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from dataclasses import dataclass
from typing import Optional
from daos.dao import Dao
from models.address import Address


@dataclass
class AddressDao(Dao[Address]):

	def delete(self, address: Address) -> bool:
		"""Supprime une adresse de la BD"""

		with Dao.connection.cursor() as cursor:
			sql = "DELETE FROM address WHERE id_address = %s"

			cursor.execute(sql, (address.id,))

			Dao.connection.commit()

			return cursor.rowcount > 0

	def update(self, address: Address) -> bool:
		"""Met à jour une adresse en BD."""

		with Dao.connection.cursor() as cursor:
			sql = """
				  UPDATE address
				  SET street = %s,
					  city = %s,
					  postal_code = %s
				  WHERE id_address = %s \
				  """

			cursor.execute(
				sql,
				(
					address.street,
					address.city,
					address.postal_code,
					address.id,
				),
			)

			Dao.connection.commit()

			return cursor.rowcount > 0

	def create(self, address: Address) -> int:
		"""Crée une adresse en BD et retourne son id"""

		with Dao.connection.cursor() as cursor:
			sql = "INSERT INTO address (street, city, postal_code) VALUES (%s, %s, %s)"

			cursor.execute(
				sql,
				(
					address.street,
					address.city,
					address.postal_code,
				)
			)

			Dao.connection.commit()

			address.id = cursor.lastrowid

			return cursor.lastrowid

	def read (self, id_address: int) -> Optional[Address]:

		address: Optional[Address]

		with Dao.connection.cursor() as cursor:
			sql = "SELECT * FROM address WHERE id_address = %s"

			cursor.execute(sql, (id_address,))
			record = cursor.fetchone()

		if record is not None:
			address = Address(
				record['street'], # type: ignore
				record['city'], # type: ignore
				record['postal_code'], # type: ignore
			)
			address.id = record['id_address'] # type: ignore
		else:
			address = None

		return address
