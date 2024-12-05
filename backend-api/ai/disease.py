import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting


def advice_generate(disease: str):
    vertexai.init(project="riceup-441906", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    responses = model.generate_content(
        [
            f"""Kamu adalah seorang petani padi yang handal. Seorang pengguna memiliki tanaman padi yang diprediksi memiliki penyakit. Berikan saran kepada pengguna tersebut.

            Penyakit yang dihadapi: {disease}

            Berikan saran SINGKAT untuk mengatasi penyakit tersebut. Jelaskan langkah-langkah yang perlu diambil pengguna secara singkat dan padat. **Sertakan contoh merk obat yang bisa digunakan untuk mengatasi penyakit tersebut dan jelaskan cara pemakaiannya. Selain itu, berikan juga contoh merk pupuk yang sebaiknya diberikan untuk mengatasi penyakit tersebut atau untuk menjaga kesehatan tanaman padi secara umum, dan jelaskan cara pemakaian pupuk tersebut.** 

            **Jika diperlukan, berikan saran tentang sanitasi dan drainase sawah yang baik untuk membantu mengatasi penyakit tersebut atau mencegah penyakit datang kembali.**

            Pastikan untuk hanya merekomendasikan merk obat dan pupuk yang tersedia di Indonesia.

            Jika penyakit yang diinput tidak diketahui, berikan saran umum untuk menjaga kesehatan tanaman padi. Pastikan saran yang diberikan mudah dipahami dan dipraktikkan oleh pengguna."""
        ],
        stream=False,
        generation_config={
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        },
        safety_settings=[
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
        ],
    )

    return responses.text