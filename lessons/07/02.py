from sqlalchemy import String, create_engine, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    mapped_column, 
    relationship, 
    Session)


BD_URL = "sqlite:///vehicle.db"

# BD_URL = "postgresql://postgres:postgres@localhost/postgres"

class Base(DeclarativeBase):
    pass


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(30))
    models: Mapped[list["Model"]] = relationship(
        back_populates="vehicle",
        cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"Vehicle({self.id}, {self.brand}, {self.color})"


class Model(Base):
    __tablename__ = "vehicle_models"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(50))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    
    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="models")
    
    def __repr__(self) -> str:
        return self.model_name
    

if __name__ == '__main__':
    engine = create_engine(BD_URL)

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        
        bmw_5 = Vehicle(
            brand = "Ford",
            models = [Model(model_name = "5 series")]
        )
        
        mercedeses = Vehicle(
            brand = "Mazda",
            models = [
                Model(model_name = "W221-clk"),
                Model(model_name = "V601")
            ]
        )
        
        session.add_all([bmw_5, mercedeses])
        
        session.commit()