from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship

from api.databases import Base


class User(Base):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True)
    mail = Column(String(200), unique=True)
    pwd = Column(String(200))
    nombre = Column(String(100))
    apellido = Column(String(100))
    rol = Column(String(50))
    obra = Column(String(50))
    enlinea = Column(String(5))
    lastlog = Column(String(20))
    pwdR = Column(String(5))
    # def __repr__(self):
    #         return f"User(id={self.id}, username='{self.mail}')"
    



# class ET(Base):
#     __tablename__ = "PLANTILLA" 

#     id = Column(Integer, primary_key=True)
#     codigo = Column(String(200))
#     numero = Column(String(200))
#     descripcion = Column(String(100))
#     revision = Column(String(100))
#     estado = Column(String(50))
#     fecha_ingreso = Column(String(50))
#     fecha_egreso= Column(String(5))
#     N_informe = Column(String(20))
#     NP = Column(String(5))
#     file_url=Column(String(200))
#     inf_url= Column(String(200))
#     os = Column(String(20))
#     OS_url = Column(String(200))
