# -*- coding: utf-8 -*-
from outflow.core.db.database import Database
from outflow.core.logging import logger


class PipelineContext:
    def __init__(self, force_dry_run=False):
        from outflow.core.pipeline import config, settings

        self._force_dry_run = force_dry_run
        self.config = config
        self.settings = settings
        self.args = None
        # self.db = Database(config["pipeline"]["databases"])
        self._db_available = None
        self._db = None

    def __getstate__(self):
        """
        This excludes self._db from the serialization because it is not
        serializable.
        """
        state = self.__dict__.copy()
        state["_db"] = None
        return state

    @property
    def dry_run(self):
        return self._force_dry_run or self.args.dry_run

    @property
    def db_available(self) -> bool:
        from outflow.core.pipeline import settings

        if self._db_available is None:
            if self.dry_run:
                self._db_available = False
                return self._db_available
            try:
                self.db_login_infos = self.config["pipeline"]["databases"][
                    settings.MAIN_DATABASE
                ]["login_info"]
                self._db_available = True
            except KeyError:
                logger.error(
                    "Database login infos not found in configuration file,"
                    " database access will not be available"
                )
                self._db_available = False
        else:
            return self._db_available

    @property
    def db(self) -> Database:
        if not self.db_available:
            logger.error("Database is not available")
            return None

        if self._db is None:
            self._db = Database(self.db_login_infos)
        return self._db

        # return Database(self.db_login_infos)
