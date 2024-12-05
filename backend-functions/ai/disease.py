from ai import prompt

def advice_disease_generate(disease: str):
    response = prompt.generate_by_prompt(
        f"""Kamu adalah seorang petani padi yang handal. Seorang pengguna memiliki tanaman padi yang diprediksi memiliki penyakit. Berikan saran kepada pengguna tersebut.

        Penyakit yang dihadapi: {disease}

        Berikan saran SINGKAT untuk mengatasi penyakit tersebut. Jelaskan langkah-langkah yang perlu diambil pengguna secara singkat dan padat. **Sertakan contoh merk obat yang bisa digunakan untuk mengatasi penyakit tersebut dan jelaskan cara pemakaiannya. Selain itu, berikan juga contoh merk pupuk yang sebaiknya diberikan untuk mengatasi penyakit tersebut atau untuk menjaga kesehatan tanaman padi secara umum, dan jelaskan cara pemakaian pupuk tersebut.** 

        **Jika diperlukan, berikan saran tentang sanitasi dan drainase sawah yang baik untuk membantu mengatasi penyakit tersebut atau mencegah penyakit datang kembali.**

        Pastikan untuk hanya merekomendasikan merk obat dan pupuk yang tersedia di Indonesia.

        Jika penyakit yang diinput tidak diketahui, berikan saran umum untuk menjaga kesehatan tanaman padi. Pastikan saran yang diberikan mudah dipahami dan dipraktikkan oleh pengguna."""
    )

    return response