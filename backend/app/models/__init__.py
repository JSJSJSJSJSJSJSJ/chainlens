"""Import every model to populate the shared SQLAlchemy registry."""

from .company import Company
from .dataset import Dataset
from .evidence import Evidence
from .relationship import Relationship, RelationshipEvidence
from .score import Score

__all__ = ["Company", "Dataset", "Evidence", "Relationship", "RelationshipEvidence", "Score"]
