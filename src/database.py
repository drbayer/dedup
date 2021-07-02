#!/usr/bin/env python3


import sqlite3
import os
from src.config import Config
from src.filemetadata import FileMetadata


class Database:

    def __init__(self):
        config = Config()
        datadir = os.path.join(config.config_dir, "data")
        os.makedirs(datadir, exist_ok=True)
        Database.database = os.path.join(datadir, "data.db")
        Database.connect()

    @classmethod
    def connect(self):
        Database.connection = sqlite3.connect(self.database)
        self.__init_db()

    @classmethod
    def __init_db(self):
        schema = """
            CREATE TABLE IF NOT EXISTS metadata (
            shasum TEXT NOT NULL,
            filesize INTEGER
            );

            CREATE UNIQUE INDEX IF NOT EXISTS metadata_index
            on metadata ('shasum');

            CREATE TABLE IF NOT EXISTS files (
            filepath TEXT NOT NULL,
            shasum TEXT NOT NULL,
            FOREIGN KEY(shasum) REFERENCES metadata(shasum)
            );

            CREATE UNIQUE INDEX IF NOT EXISTS files_index
            on files ('filepath');
        """

        with Database.connection as con:
            con.executescript(schema)

    @classmethod
    def write_metadata(self, metadata: FileMetadata):
        if Database.file_recorded(metadata.path):
            return
        sql = """
            INSERT INTO metadata (shasum,filesize) VALUES (?,?);
            INSERT INTO files (filepath,shasum) VALUES (?,?);
            """
        with Database.connection as con:
            con.executescript(sql, (metadata.shasum, metadata.filesize,
                                    metadata.path, metadata.shasum,))

    @classmethod
    def file_recorded(self, filepath):
        sql = """
            SELECT COUNT(filepath)
            FROM files
            WHERE filepath = '{path}'
            """.format(path=filepath)
        for row in Database.connection.execute(sql):
            if row[0] == 0:
                return False
            if row[0] == 1:
                return True
