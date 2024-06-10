from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from anomaly_detection.models.anomaly import Base


class Database:
    _instance = None

    def __new__(cls, uri: str = None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_db(uri)
        return cls._instance

    def _init_db(self, uri: str):
        self.engine = create_engine(uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()
