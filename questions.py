"""
IQ Test savollari to'plami.
Har bir savol:
- id: savol raqami
- question: savol matni
- options: 4 ta variant ro'yxati
- correct: to'g'ri variant indeksi (0, 1, 2, 3)
- explanation: to'g'ri javobning batafsil tushuntirilishi
- category: Mantiq, Ketma-ketlik, Fazoviy, Matematik, Analitika
"""

QUESTIONS = [
    {
        "id": 1,
        "category": "🔢 Ketma-ketlik",
        "question": "Quyidagi sonlar qatorida so'roq belgisi o'rnidagi sonni toping:\n\n2, 4, 8, 16, 32, ?",
        "options": ["48", "64", "54", "72"],
        "correct": 1,
        "explanation": "Har bir keyingi son avvalgisini 2 ga ko'paytirish orqali hosil bo'ladi (2 × 2 = 4, 4 × 2 = 8... 32 × 2 = 64)."
    },
    {
        "id": 2,
        "category": "🧩 Analitika",
        "question": "Daryo so'zining Suv bilan qanday bog'liqligi bo'lsa, O'rmon so'zining nima bilan shunday bog'liqligi bor?",
        "options": ["Hayvon", "Daraxt", "Barg", "Yer"],
        "correct": 1,
        "explanation": "Daryo suvdan tashkil topadi, xuddi shuningdek o'rmon daraxtlardan tashkil topadi."
    },
    {
        "id": 3,
        "category": "🔢 Ketma-ketlik",
        "question": "Mantiqiy qatorni davom ettiring:\n\n1, 1, 2, 3, 5, 8, 13, ?",
        "options": ["18", "20", "21", "24"],
        "correct": 2,
        "explanation": "Bu Fibonachchi ketma-ketligi: har bir son o'zidan oldingi ikkita sonning yig'indisiga teng (8 + 13 = 21)."
    },
    {
        "id": 4,
        "category": "💡 Mantiq",
        "question": "Agar hamma A'lar B bo'lsa, va ba'zi B'lar C bo'lsa, unda quyidagilardan qaysi biri QAT'IY haqiqat?",
        "options": [
            "Hamma A'lar C dir",
            "Ba'zi A'lar C bo'lishi mumkin",
            "Hech bir A C emas",
            "Barcha C'lar A dir"
        ],
        "correct": 1,
        "explanation": "Ba'zi B'lar C bo'lgani sababli, A'lar ham C bo'lishi ehtimoli bor, ammo qat'iy ravishda 'bo'lishi mumkin' degan xulosa to'g'ri."
    },
    {
        "id": 5,
        "category": "🔢 Matematik mantiq",
        "question": "Quyidagi qonuniyat bo'yicha ? belgisini toping:\n\n3 -> 9\n4 -> 16\n5 -> 25\n7 -> ?",
        "options": ["35", "42", "49", "56"],
        "correct": 2,
        "explanation": "Har bir son o'zining kvadratiga mos keladi (7² = 49)."
    },
    {
        "id": 6,
        "category": "🧩 Fazoviy mantiq",
        "question": "Agar soat 03:15 ni ko'rsatayotgan bo'lsa, soat millari (soat va daqiqa) orasidagi burchak necha gradus?",
        "options": ["0°", "7.5°", "15°", "22.5°"],
        "correct": 1,
        "explanation": "Daqiqa mili 3 da turganda, soat mili 3 dan bir oz oldinga siljiydi. 1 daqiqada soat mili 0.5° yuradi. 15 × 0.5° = 7.5°."
    },
    {
        "id": 7,
        "category": "🔢 Ketma-ketlik",
        "question": "Ketma-ketlikdagi tushirib qoldirilgan sonni toping:\n\n100, 96, 88, 72, ?",
        "options": ["40", "56", "48", "64"],
        "correct": 0,
        "explanation": "Farqlar 2 barobardan oshib bormoqda: -4, -8, -16, demak keyingisi -32 bo'ladi. 72 - 32 = 40."
    },
    {
        "id": 8,
        "category": "💡 Mantiq",
        "question": "Bir kishi 8 dollar evaziga ot sotib oldi, uni 9 dollarga sotdi. Keyin yana 10 dollarga qaytarib sotib olib, 11 dollarga sotdi. U jami necha dollar foyda qildi?",
        "options": ["1 dollar", "2 dollar", "0 dollar", "3 dollar"],
        "correct": 1,
        "explanation": "1-savdodan 1 dollar (9-8=1), 2-savdodan yana 1 dollar (11-10=1) foyda ko'rdi. Jami foyda = 2 dollar."
    },
    {
        "id": 9,
        "category": "🧩 So'z mantig'i",
        "question": "Ortiqcha so'zni toping:",
        "options": ["Olma", "Shaftoli", "Sabzi", "Nok"],
        "correct": 2,
        "explanation": "Sabzi — ildizmevali sabzavot, qolganlari esa daraxtda pishadigan mevalardir."
    },
    {
        "id": 10,
        "category": "🔢 Matematik mantiq",
        "question": "Agar 5 ta mashina 5 daqiqada 5 ta detal yasasa, 100 ta mashina 100 ta detalni necha daqiqada yasaydi?",
        "options": ["100 daqiqada", "5 daqiqada", "20 daqiqada", "1 daqiqada"],
        "correct": 1,
        "explanation": "1 ta mashina 1 ta detalni yasashi uchun 5 daqiqa ketadi. Shuning uchun 100 ta mashina ham 100 ta detalni 5 daqiqada yasaydi."
    },
    {
        "id": 11,
        "category": "🧩 Fazoviy mantiq",
        "question": "Kubning 6 ta tomoni bor. Agar har bir tomoni turli rangga bo'yalsa, qarama-qarshi tomonlar necha juft bo'ladi?",
        "options": ["2 juft", "3 juft", "4 juft", "6 juft"],
        "correct": 1,
        "explanation": "Kubda 6 ta tomon bo'lib, ular 3 ta qarama-qarshi juftlikni hosil qiladi."
    },
    {
        "id": 12,
        "category": "🔢 Ketma-ketlik",
        "question": "Qatorni to'ldiring:\n\n3, 5, 9, 17, 33, ?",
        "options": ["65", "49", "66", "55"],
        "correct": 0,
        "explanation": "Har safar qo'shilayotgan son 2 barobar ortmoqda: +2, +4, +8, +16, demak keyingisi +32 bo'ladi (33 + 32 = 65)."
    },
    {
        "id": 13,
        "category": "💡 Mantiq",
        "question": "Maryamning otasining 5 ta qizi bor: Chacha, Cheche, Chichi, Chocho. 5-qizining ismi nima?",
        "options": ["Chuchu", "Maryam", "Charos", "Mohira"],
        "correct": 1,
        "explanation": "Savolning boshida aytilgan: 'Maryamning otasining 5 ta qizi bor...', demak 5-qiz Maryamdir!"
    },
    {
        "id": 14,
        "category": "🔢 Matematik mantiq",
        "question": "Bir hovuzga suv quyuvchi jo'mrak uni 2 soatda to'ldiradi, pastki jo'mrak esa 3 soatda bo'shatadi. Ikkala jo'mrak bir vaqtda ochilsa, hovuz necha soatda to'ladi?",
        "options": ["4 soatda", "5 soatda", "6 soatda", "1 soatda"],
        "correct": 2,
        "explanation": "1 soatda: 1/2 - 1/3 = 1/6 qismi to'ladi. Demak butun hovuz 6 soatda to'ladi."
    },
    {
        "id": 15,
        "category": "🧩 Analitika",
        "question": "Qaysi so'z 'KITOBLAR' so'zining harflaridan tuzilishi MUMKIN EMAS?",
        "options": ["BORLIK", "ORTIQ", "ROBIYA", "TOBLAR"],
        "correct": 1,
        "explanation": "'ORTIQ' so'zida 'Q' harfi bor, 'KITOBLAR' so'zida esa 'Q' harfi yo'q."
    }
]


def calculate_iq(score: int, total: int = len(QUESTIONS)) -> dict:
    """
    To'plangan ball bo'yicha IQ va uning darajasini hisoblab beradi.
    Standartlashtirilgan IQ shkalasi (70 - 145+).
    """
    percentage = (score / total) * 100

    if score == 15:
        iq = 145
        title = "Daho (Genius) 🌟"
        desc = "Ajoyib natija! Sizning mantiqiy va analitik fikrlashingiz dunyo aholisining 1% dan yuqori darajada."
    elif score >= 13:
        iq = 130 + (score - 13) * 5
        title = "Juda yuqori intellekt 🧠⚡️"
        desc = "Mantiqiy qonuniyatlar, fazoviy tasavvur va tahlil qobiliyatingiz juda kuchli."
    elif score >= 11:
        iq = 115 + (score - 11) * 7
        title = "O'rtachadan yuqori intellekt 💡"
        desc = "Yaxshi natija! Siz tez va mantiqiy to'g'ri qarorlar qabul qila olasiz."
    elif score >= 8:
        iq = 100 + (score - 8) * 5
        title = "O'rtacha intellekt darajasi 🎯"
        desc = "Ko'pchilik odamlar uchun me'yoriy natija. Yana ozgina diqqat va mashq bilan yuqori natijaga erishishingiz mumkin."
    elif score >= 5:
        iq = 85 + (score - 5) * 5
        title = "O'rtachadan pastroq daraja 📚"
        desc = "Mantiqiy masalalarda biroz ko'proq mashq qilish tavsiya etiladi."
    else:
        iq = 70 + score * 3
        title = "Boshlang'ich daraja 🔄"
        desc = "E'tibor va diqqatni jamlash ustida ishlash tavsiya etiladi. Testni qayta topshirib ko'ring!"

    return {
        "score": score,
        "total": total,
        "percentage": round(percentage, 1),
        "iq": iq,
        "title": title,
        "desc": desc
    }
