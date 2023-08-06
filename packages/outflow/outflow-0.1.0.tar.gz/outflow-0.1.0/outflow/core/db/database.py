# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker, scoped_session

from outflow.core.generic.metaclasses import Singleton
from outflow.core.logging import logger


class DeclarativeBases(metaclass=Singleton):
    def __init__(self):
        self._bases = dict()

    def __getitem__(self, item):
        if item not in self._bases:
            self._bases[item] = declarative_base()

        return self._bases[item]


DefaultBase = DeclarativeBases()["MAINDB"]


class DatabaseException(Exception):
    pass


class Database:
    """
    A class to manage the connection to the database
    """

    def __init__(self, login_infos):
        self.login_infos = login_infos
        # self.bound = False
        self.connected = False
        self._engine = None
        self._admin_engine = None
        self._session = None
        self._connection = None
        self._admin_connection = None

    @property
    def admin_connection(self):
        if self._admin_connection is None:
            self.connect_admin()

        return self._admin_connection

    def connect_admin(self):
        """
        Make a connection to the database using SQLAlchemy
        """

        # connected = self.is_available()
        logger.info("Connecting to database as admin")
        self._reflect()
        self._admin_connection = self.admin_engine.connect()

    def connect(self):
        """
        Make a connection to the database using SQLAlchemy
        """

        # connected = self.is_available()
        logger.info("Connecting to database as user")
        self._reflect()
        self._connection = self.engine.connect()
        self.connected = True

    @property
    def session(self):
        if self._session is None:
            if not self.connected:
                self.connect()
            self._session = scoped_session(sessionmaker(bind=self.engine))

        return self._session

    @property
    def admin_engine(self):
        if self._admin_engine is None:
            admin_url = self._generate_url(admin=True)
            self._admin_engine = create_engine(admin_url)
        return self._admin_engine

    @property
    def engine(self):
        if self._engine is None:
            url = self._generate_url()
            self._engine = create_engine(url)
        return self._engine

    def _generate_url(self, admin=False):

        if admin and "admin" not in self.login_infos:
            raise DatabaseException("Admin credentials missing from configuration file")

        vendor = self.login_infos["vendor"]
        address = self.login_infos["address"]

        if vendor == "sqlite":
            return "{vendor}:///{address}".format(vendor=vendor, address=address)
        else:
            return "{vendor}://{user}@{address}/{database}".format(
                vendor=vendor,
                address=address,
                user=self.login_infos["admin"] if admin else self.login_infos["user"],
                database=self.login_infos["database"],
            )

    @property
    def is_connected(self):
        return self.connected

    def _reflect(self):
        try:
            DeferredReflection.prepare(self.engine)
        except NoSuchTableError as e:
            logger.warning(f"The table {e} does not exist")

    def get_configured_sessionmaker(self):
        return

    # @property
    # def admin_connection(self):
