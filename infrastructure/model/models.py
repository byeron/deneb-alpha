from sqlalchemy import Column, String

from infrastructure.model.base import Base


class FeatureData(Base):
    __tablename__ = "feature_files"
    id = Column(String, unique=True, primary_key=True)
    file_name = Column(String, nullable=False)
    hash = Column(String, nullable=False, unique=True)
    created_at = Column(String, nullable=False)
