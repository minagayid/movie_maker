"""Rights-aware movie production orchestration."""

from .models import ProjectSpec, ProductionPackage, Scene, SourceMaterial
from .pipeline import MovieMaker

__all__ = ["MovieMaker", "ProjectSpec", "ProductionPackage", "Scene", "SourceMaterial"]

__version__ = "0.1.0"
