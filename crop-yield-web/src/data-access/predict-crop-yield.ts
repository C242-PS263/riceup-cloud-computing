import { PredictCropYieldRequest, PredictCropYieldResponse } from "../data/predict-crop-yield";
import { apiUrl } from "../lib/utils";

export async function predictCropYield(request: PredictCropYieldRequest): Promise<PredictCropYieldResponse> {
  const response = await fetch(apiUrl("/predict-crop-yield"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Failed to predict crop yield");
  }

  return await response.json();
}
