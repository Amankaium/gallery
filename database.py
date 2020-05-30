from sqlalchemy import create_engine, \
    Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/gallery_db"
)

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    country = Column(String(255))
    picture = relationship("Picture")

    def __str__(self):
        self.name


class Picture(Base):
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, default=0)
    author = Column(ForeignKey("author.id"))

    def __str__(self):
        self.name

Base.metadata.create_all(engine)

session = sessionmaker(engine)()