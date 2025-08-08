from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    calculations = relationship(
        "Calculation",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)

    # Link each calculation to its owner
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    operation = Column(String, nullable=False)

    operand1 = Column(Float, nullable=False)
    operand2 = Column(Float, nullable=True)

    result = Column(Float, nullable=False)

    # Server-side timestamp (UTC) when the row is inserted
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    # Relationship back to user
    user = relationship("User", back_populates="calculations")
