from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table , Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


role_actor = Table(
    'role_actor',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('actor_id', ForeignKey('actors.id'),primary_key=True),
    extend_existing=True
)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    character_name = Column(String())
    
    actors = relationship('Actor', secondary=role_actor, back_populates='roles')
    auditions = relationship('Audition' , backref=backref('role'))

    def get_auditions(self,session):
        return session.query(Audition).filter(Audition.role_id== self.id).all() 
    
    def __repr__(self):
        return f'<Role {self.name}>'
     

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer(), primary_key=True)
    name= Column(String())


    roles = relationship('Company' , secondary=role_actor, back_populates="actors")
    auditions = relationship('Audition' , backref=backref('actor'))

        
    def get_auditions(self,session):
        return (session.query(Audition) .filter(Audition.actor_id == self.id).all())
    
        
    def get_roles(self,session): 
        return (
            session.query(Roles)
            .join(role_actor)
            .filter(role_actor.c.actor_id == self.id)
            .all()
        )

    def __repr__(self):
        return f'<Actor {self.name}>'
    

    
class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer() , primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())


    role_id= Column(Integer, ForeignKey('roles.id'))
    actor_id = Column(Integer , ForeignKey('actors.id'))


    def get_audition_for_actor(self,session): 
        return session.query(Actor).filter(Actor.id == self.actor_id).first()
    
    def get_audition_for_role(self,session):
        return session.query(Role).filter(Role.id == self.role_id).first()
    
    def audition_order(self,session): 
        return (f"Freebie for  {self.get_audition_for_role(session).actor} by {self.get_audition_for_actor(session).actor}: Actor:{self.actor} location:{self.location} phone:{self.phone}")
    

    def __repr__(self):
        return f'<Audition {self.actor}>'
