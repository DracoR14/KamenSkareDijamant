from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Pravila igre: šta pobjeđuje šta
PRAVILA = {
    "kamen": ["skare"],
    "skare": ["papir"],
    "papir": ["kamen", "dijamant"],
    "dijamant": ["kamen", "skare"]
}

# Model poruke koju nam telefon šalje (šta igrač bira)
class PotezIgraca(BaseModel):
    potez: str
    korisnik_ima_dijamant: bool
    bot_ima_dijamant: bool

@app.get("/")
def pocetna_stranica():
    return {"poruka": "Dobrodošli na server igre Kamen-Škare-Papir-Dijamant!"}

@app.post("/odigraj-rundu")
def odigraj_rundu(podaci: PotezIgraca):
    moj_potez = podaci.potez.lower().strip()
    ja_imam_dijamant = podaci.korisnik_ima_dijamant
    bot_imam_dijamant = podaci.bot_ima_dijamant

    # Provjera za dijamant (kazna ako igrač vara i bira ga opet)
    if moj_potez == "dijamant" and not ja_imam_dijamant:
        moj_potez = "kamen" 

    # Bot bira potez
    moguci_potezi_bota = ["kamen", "skare", "papir"]
    if bot_imam_dijamant:
        moguci_potezi_bota.append("dijamant")
        
    bot_potez = random.choice(moguci_potezi_bota)

    # Određivanje pobjednika runde
    if moj_potez == bot_potez:
        rezultat = "nerijeseno"
        poruka = "🤝 Neriješeno je!"
    elif bot_potez in PRAVILA[moj_potez]:
        rezultat = "igrac"
        poruka = "🎉 Pobijedio si u ovoj rundi!"
    else:
        rezultat = "bot"
        poruka = "😢 Bot uzima bod! (Zadirkivanje: Jesi li to pošao po drva? 🪓)"

    # Server u sekundi vraća ove podatke nazad telefonu preko interneta
    return {
        "tvoj_potez": moj_potez,
        "bot_potez": bot_potez,
        "pobjednik_runde": rezultat,
        "poruka": poruka
    }