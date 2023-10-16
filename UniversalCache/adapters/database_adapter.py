import json
import datetime
from typing import Any, Type

from sqlalchemy import create_engine, BigInteger, Column, Text, DateTime
from sqlalchemy.orm import declarative_base, Session

from UniversalCache.abstract_adapter import AbstractAdapter

Base = declarative_base()


class CacheRecord(Base):
    __tablename__ = 'universal_cache'

    key = Column(Text, primary_key=True, unique=True, nullable=False)
    value = Column(Text, nullable=False)
    expiration_time = Column(DateTime, nullable=True)


class DatabaseAdapter(AbstractAdapter):
    def __init__(self, db_url: str):
        self.__engine = create_engine(db_url)

        Base.metadata.create_all(self.__engine)

    @classmethod
    def __make_key(cls, function, *args, **kwargs) -> str:
        return f'{function.__name__}:{function.__module__}:{str(args)}{str(kwargs)}'

    def __key_exists(self, key: str) -> bool:
        with Session(bind=self.__engine) as session:
            record_exists = session.query(CacheRecord).filter_by(key=key).scalar()

            return record_exists

    def get(self, function, params: dict, *args, **kwargs) -> Any:
        key = self.__make_key(function, *args, **kwargs)

        with Session(bind=self.__engine) as session:
            record: Type[CacheRecord] = session.query(CacheRecord).filter_by(key=key).one()

            json_decoder = params['json_decoder'] if 'json_decoder' in params else None

            if json_decoder:
                json_decoded_value = json.loads(str(record.value), cls=json_decoder)
            else:
                json_decoded_value = json.loads(str(record.value))

            return json_decoded_value

    def set(self, function, value: Any, params: dict, *args, **kwargs) -> None:
        key = self.__make_key(function, *args, **kwargs)

        with Session(bind=self.__engine) as session:
            json_encoder = params['json_encoder'] if 'json_encoder' in params else None

            ttl = params['ttl'] if 'ttl' in params else None

            if ttl is not None:
                expiration_time = datetime.datetime.now() + ttl
            else:
                expiration_time = None

            if json_encoder:
                json_encoded_value = json.dumps(value, cls=json_encoder)
            else:
                json_encoded_value = json.dumps(value)

            if self.__key_exists(key):
                session.query(CacheRecord).filter_by(key=key).update({
                    'value': json_encoded_value,
                    'expiration_time': expiration_time
                })
            else:
                record = CacheRecord(key=key, value=json_encoded_value, expiration_time=expiration_time)

                session.add(record)

            session.commit()

    def contains(self, function, params: dict, *args, **kwargs) -> bool:
        key = self.__make_key(function, *args, **kwargs)

        session = Session(bind=self.__engine)

        cache_record: Type[CacheRecord] = session.query(CacheRecord).filter_by(key=key).first()

        if cache_record is None:
            return False

        expiration_time = cache_record.expiration_time

        if expiration_time is None:
            return True

        if datetime.datetime.now() > expiration_time:
            return False
        else:
            return True
