import random
import collections

# Pravila: šta pobjeđuje šta
PRAVILA = {
    "kamen": ["skare"],
    "skare": ["papir"],
    "papir": ["kamen", "dijamant"],
    "dijamant": ["kamen", "skare"]
}

# Rezultat meča (igra se do 3 pobjede)
moje_pobjede = 0
bot_pobjede = 0

# Svaki igrač ima samo jedan dijamant za cijeli meč
ja_imam_dijamant = True
bot_imam_dijamant = True

# Ovdje bot pamti tvoje prošle poteze da bi te skenirao!
istorija_poteza_igraca = []

print("=============================================")
print("🏆 DOBRODOŠLI U KAMEN - ŠKARE - PAPIR - DIJAMANT 🏆")
print("=============================================")
print("📌 Pravila: Tradicionalna + Dijamant lomi kamen/škare, ali gubi od papira!")
print("📌 Dijamant možeš iskoristiti samo JEDNOM u cijelom meču.")
print("📌 Igra se do 3 pobjede. Sretno!\n")

# Glavna petlja: igra se dok neko ne skupi 3 boda
while moje_pobjede < 3 and bot_pobjede < 3:
    print(f"📊 TRENUTNI REZULTAT -> Ti: {moje_pobjede} | Bot: {bot_pobjede}")
    
    # 1. Unos igrača
    moj_potez = input("Izaberi (kamen, skare, papir, dijamant): ").lower().strip()
    
    if moj_potez not in ["kamen", "skare", "papir", "dijamant"]:
        print("❌ Ne postoji taj potez! Gubiš ovu rundu zbog varanja.\n")
        bot_pobjede += 1
        continue
        
    if moj_potez == "dijamant" and not ja_imam_dijamant:
        print("⚠️ Već si potrošio svoj dijamant! Kazna: automatski biraš KAMEN.")
        moj_potez = "kamen"

    # 2. "Mind-Reading" AI - Bot razmišlja!
    moguci_potezi_bota = ["kamen", "skare", "papir"]
    if bot_imam_dijamant:
        moguci_potezi_bota.append("dijamant")
        
    # Ako je igrač odigrao više od 2 runde, bot ga analizira
    if len(istorija_poteza_igraca) >= 2:
        # Tražimo koji potez igrač najčešće bira
        najcesci_potez = collections.Counter(istorija_poteza_igraca).most_common(1)[0][0]
        
        # Bot bira ono što pobjeđuje taj najčešći potez
        if najcesci_potez == "kamen":
            bot_potez = "papir"
        elif najcesci_potez == "skare":
            bot_potez = "kamen"
        elif najcesci_potez == "papir":
            bot_potez = "skare"
        else: # Ako je igrač često birao dijamant
            bot_potez = "papir"
            
        # Ako bot izabere dijamant (nasumično 20% šanse za iznenađenje)
        if bot_imam_dijamant and random.random() < 0.2:
            bot_potez = "dijamant"
    else:
        # Na početku meča bot bira nasumično
        bot_potez = random.choice(moguci_potezi_bota)

    # Zapamti ovaj potez igrača za iduću rundu
    istorija_poteza_igraca.append(moj_potez)

    # Potroši dijamante ako su iskorišteni
    if moj_potez == "dijamant": ja_imam_dijamant = False
    if bot_potez == "dijamant": bot_imam_dijamant = False

    print(f"🤖 Bot je izabrao: {bot_potez.upper()}")

    # 3. Ko je pobijedio u rundi?
    if moj_potez == bot_potez:
        print("🤝 Neriješeno je u ovoj rundi!\n")
    elif bot_potez in PRAVILA[moj_potez]:
        print("🎉 Bravo! Osvajaš bod!\n")
        moje_pobjede += 1
    else:
        print("😢 Bot uzima bod! (Zadirkivanje: Jesi li to pošao po drva? 🪓)\n")
        bot_pobjede += 1

# KRAJ MEČA
print("=============================================")
if moje_pobjede == 3:
    print("🏆 KRAJ MEČA: POBIJEDIO SI! Ti si kralj Dijamanata! 👑")
else:
    print("💀 KRAJ MEČA: BOT TE JE RAZBIO! Više sreće drugi put. 💀")
print("=============================================")