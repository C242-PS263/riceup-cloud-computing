import numpy as np

# Fungsi logika fuzzy untuk prediksi hasil panen
def fuzzy_yield_prediction(land_area, rainfall, disease_level, temperature, planting_distance):
    # Definisi fungsi keanggotaan fuzzy untuk curah hujan
    if rainfall == "sangat rendah":
        rainfall_factor = 0.3
    elif rainfall == "rendah":
        rainfall_factor = 0.7
    elif rainfall == "normal":
        rainfall_factor = 1.0
    elif rainfall == "tinggi":
        rainfall_factor = 0.8
    else:
        rainfall_factor = 0.4

    # Definisi fungsi keanggotaan fuzzy untuk tingkat penyakit
    if disease_level == "sangat rendah":
        disease_factor = 1.0
    elif disease_level == "rendah":
        disease_factor = 0.8
    elif disease_level == "normal":
        disease_factor = 0.6
    elif disease_level == "tinggi":
        disease_factor = 0.2
    else:
        disease_factor = 0.05

    # Efek jarak tanam terhadap hasil panen
    if planting_distance == "20cmx20cm":
        planting_factor = 1.2
    elif planting_distance == "25cmx25cm":
        planting_factor = 1.0
    elif planting_distance == "30cmx30cm":
        planting_factor = 0.9


    # Menghitung hasil panen dalam kg berdasarkan faktor fuzzy
    base_yield_per_m2 = 8 * 1000 / 10000  # 8 ton per hektar = 8000 kg per 10,000 m2
    yield_prediction = (
        land_area * base_yield_per_m2 * rainfall_factor * disease_factor * planting_factor * (30 - abs(temperature - 25)) / 30
    )

    return round(yield_prediction, 2)


# Fungsi untuk menghitung jumlah bibit ideal
def seed_amount(land_area, planting_distance):
    if planting_distance == "20cmx20cm":
        seeds_per_m2 = 25
    elif planting_distance == "25cmx25cm":
        seeds_per_m2 = 16
    elif planting_distance == "30cmx30cm":
        seeds_per_m2 = 11

    base_seed_per_m2 = seeds_per_m2 / 1000
    variation = np.random.uniform(0.9, 1.1)
    total_seed = land_area * base_seed_per_m2 * variation
    return round(total_seed, 2)

def gkg_from_gkp(gkp):
    return round(gkp * 0.7, 2) # Gabah Kering Giling = 70% dari GKP

def rice_from_gkg(gkg):
    return round(gkg * 0.65, 2) # Beras = 65% dari GKG
