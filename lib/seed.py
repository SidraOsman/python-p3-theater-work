
import random
from faker import Faker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base , Role, Audition, Actor

print ("Seeding starts!!")
if __name__ == '__main__': 

    engine = create_engine('sqlite:///theater.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Role).delete()
    session.query(Actor).delete()
    session.query(Audition).delete()

    fake = Faker()

        
    roles= []
    for _ in range (20):
        role= Role(
            character_name = fake.unique.name()
        )
        session.add(role)
        session.commit()
        roles.append(role)

    actors = []
    for _ in range (20):
        actor= Actor(
            name = fake.unique.name()
        )
        session.add(actor)
        session.commit()
        actors.append(actor)

    auditions = []
    for role in roles:
        for i in range(random.randint(1,5)):
            dev = random.choice(actors)
            if role not in actor.roles:
                actor.roles.append(role)
                session.add(actor)
                session.commit()

            audition = Audition(
                actor = fake.unique.name(),
                location = fake.unique.location(),
                phone = fake.unique.phone_number(),
                role_id = role.id,
                actor_id = actor.id
            )
            auditions.append(audition)

    session.bulk_save_objects(auditions)
    session.commit()
    session.close()
