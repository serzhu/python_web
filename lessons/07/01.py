from sqlalchemy.orm import (DeclarativeBase, 
                            Mapped, 
                            mapped_column, 
                            relationship, 
                            Session)
from sqlalchemy import String, create_engine, ForeignKey

class Base(DeclarativeBase):
    pass

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(30))
    models: Mapped[list['Model']] = relationship(back_populates='vehicle')
    

class Model(Base):
    __tablename__ = 'vehicle_models'
    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(50))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicles.id'))
    vehicle: Mapped['Vehicle'] = relationship(back_populates="models")
    
    def __repr__(self) -> str:
        return self.model_name

if __name__ == '__main__':
    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(bind = engine)

    with Session(engine) as session:
        ford = Vehicle(
            brand='Ford', 
            models=[Model(model_name='Fokus'), Model(model_name='Mustang')]
        )
        
        toyota = Vehicle(
            brand='Toyota', 
            models=[
                Model(model_name='Corolla'), 
                Model(model_name='Camry')
            ]
        )
        
        session.add_all([ford, toyota])
        session.commit()
