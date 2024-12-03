export interface PredictCropYieldRequest {
    land_area: string;
    rainfall: string;
    disease_level: string;
    temperature: string;
    planting_distance: string;
}

export interface PredictCropYieldResponse {
    land_area: number;
    rainfall: string;
    disease_level: string;
    temperature: number;
    planting_distance: string;
    seed_weight: number;
    gkp: number;
    gkg: number;
    rice: number;
}