from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, Table, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between Article and Tag
article_tag_association = Table('article_tag', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Contenu(Base):
    __tablename__ = 'contenus'
    id = Column(Integer, primary_key=True)
    titre = Column(String, nullable=False)
    contenu = Column(Text, nullable=False)
    date_publication = Column(Date, nullable=False)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'contenu',
        'polymorphic_on': type
    }

class Depeche(Contenu):
    __tablename__ = 'depeches'
    id = Column(Integer, ForeignKey('contenus.id'), primary_key=True)

    articles = relationship("Article", back_populates="depeche", foreign_keys="[Article.depeche_id]")

    __mapper_args__ = {
        'polymorphic_identity': 'depeche',
    }

class Article(Contenu):
    __tablename__ = 'articles'
    id = Column(Integer, ForeignKey('contenus.id'), primary_key=True)
    depeche_id = Column(Integer, ForeignKey('depeches.id'), nullable=False)
    ia_id = Column(Integer, ForeignKey('ias.id'), nullable=False)

    depeche = relationship("Depeche", back_populates="articles", foreign_keys=[depeche_id])
    ia = relationship("IA", back_populates="articles")
    illustrations = relationship("Illustration", back_populates="article")
    tags = relationship("Tag", secondary=article_tag_association, back_populates="articles")

    __mapper_args__ = {
        'polymorphic_identity': 'article',
    }

class Illustration(Base):
    __tablename__ = 'illustrations'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    ia_id = Column(Integer, ForeignKey('ias.id'), nullable=False)

    article = relationship("Article", back_populates="illustrations", foreign_keys=[article_id])
    ia = relationship("IA", back_populates="illustrations", foreign_keys=[ia_id])

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)

    articles = relationship("Article", secondary=article_tag_association, back_populates="tags")

class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    email = Column(String, nullable=False)

class IA(Base):
    __tablename__ = 'ias'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    modele = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date_generation = Column(Date, nullable=False)

    articles = relationship("Article", back_populates="ia", foreign_keys="[Article.ia_id]")
    illustrations = relationship("Illustration", back_populates="ia", foreign_keys="[Illustration.ia_id]")

# Configuration de la base de données
engine = create_engine('sqlite:///BDD_site_ORM.db')
Base.metadata.create_all(engine)

# Vérification des tables
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in the database:")
for table in tables:
    print(table)
