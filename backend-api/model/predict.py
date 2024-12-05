from pydantic import BaseModel, Field
from enum import Enum

class RainfallStatus(str, Enum):
    sangat_rendah = "sangat rendah"
    rendah = "rendah"
    normal = "normal"
    tinggi = "tinggi"
    sangat_tinggi = "sangat tinggi"

class DiseaseLevel(str, Enum):
    sangat_rendah = "sangat rendah"
    rendah = "rendah"
    normal = "normal"
    tinggi = "tinggi"
    sangat_tinggi = "sangat tinggi"

class PlantingDistance(str, Enum):
    _20cmx20cm = "20cmx20cm"
    _25cmx25cm = "25cmx25cm"
    _30cmx30cm = "30cmx30cm"

class PredictCropYieldRequest(BaseModel):
    land_area: int = Field(examples=[1000])
    rainfall: RainfallStatus = Field(examples=[RainfallStatus.normal])
    disease_level: DiseaseLevel = Field(examples=[DiseaseLevel.normal])
    temperature: float = Field(examples=[21.8])
    planting_distance: PlantingDistance = Field(examples=[PlantingDistance._20cmx20cm])

class PredictCropYieldAdviceRequest(BaseModel):
    land_area: int = Field(examples=[1000])
    rainfall: RainfallStatus = Field(examples=[RainfallStatus.normal])
    disease_level: DiseaseLevel = Field(examples=[DiseaseLevel.normal])
    temperature: float = Field(examples=[21.8])
    planting_distance: PlantingDistance = Field(examples=[PlantingDistance._20cmx20cm])
    seed_weight: float = Field(examples=[26.35])
    gkp: float = Field(examples=[514.56])
    gkg: float = Field(examples=[360.19])
    rice: float = Field(examples=[234.12])

    def as_redis_key(self):
        return "predict_crop_yield_advice:" + "_".join(map(str, [
            self.land_area,
            self.rainfall,
            self.disease_level,
            self.temperature,
            self.planting_distance,
            self.seed_weight,
            self.gkp,
            self.gkg,
            self.rice
        ]))