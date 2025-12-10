from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sympy import symbols, Eq, solve, parse_expr, latex, lambdify
import numpy as np
from typing import List, Optional
import traceback
from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()
app = FastAPI(title="Calcolatore di funzione inversa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FunctionInput(BaseModel):
    function: str 

class FunctionResult(BaseModel):
    funzione_di_partenza: str
    funzione_inversa: str
    punti_x: List[float]
    punti_y: List[Optional[float]]
    studio_della_funzione: dict

@app.get("/")
def read_root():
    """Endpoint di test per verificare che il server funzioni"""
    return {"message": "Backend funzionante!"}

def calcola_punti_grafico(expr, variabile, start=-20, end=21):
    """
    Genera i punti x, y per il grafico di un'espressione simbolica.
    Gestisce parametri liberi sostituendoli con default (2).
    Restituisce due liste: punti_x e punti_y.
    """
    try:
        # Generiamo punti interi
        valori_x = np.arange(start, end)
        
        # TRUCCO PER GRAFICI GENERICI:
        # Se ci sono parametri extra (es. 'a' in 'a^x'), li sostituiamo con 2
        simboli_liberi = expr.free_symbols - {variabile}
        if simboli_liberi:
            sostituzioni = {simbolo: 2 for simbolo in simboli_liberi}
            expr_per_grafico = expr.subs(sostituzioni)
        else:
            expr_per_grafico = expr
        
        # Convertiamo in funzione Python veloce
        f_grafico = lambdify(variabile, expr_per_grafico, modules=['numpy'])
        
        # Calcoliamo i valori
        valori_y_numpy = f_grafico(valori_x)
        
        # Se il risultato è un numero singolo (funzione costante), lo replichiamo
        if np.isscalar(valori_y_numpy):
            valori_y_numpy = np.full_like(valori_x, valori_y_numpy)
        
        # Convertiamo in lista Python pulita (gestendo infiniti e NaN)
        punti_y = [float(val) if np.isfinite(val) else None for val in valori_y_numpy]
        
        return valori_x.tolist(), punti_y
    
    except Exception:
        return ValueError("Impossibile calcolare i punti del grafico")

def calcola_inversa(function_str: str):
    """
    Calcola la funzione inversa di una funzione data come stringa.
    Restituisce l'espressione originale e l'espressione inversa.
    """
    # definisci i simboli
    x, y = symbols('x y')
    
    # convertire la stringa in espressione matematica
    espressione = parse_expr(function_str)
    
    # creiamo l'equazione y = f(x)
    funzione_originale = Eq(y, espressione)
    
    # troviamo la funzione inversa risolvendo l'equazione per x
    soluzioni = solve(funzione_originale, x)
    
    if not soluzioni:
        raise ValueError("Impossibile trovare l'inversa")
    
    expr_inversa = soluzioni[0]
    
    return espressione, expr_inversa, y

def studio_della_funzione(funzione_di_partenza: str, funzione_inversa: str):
    """
    Funzione che prende una funzione in argomento e ne fa lo studio tramite l'AI
    """
        # Token GitHub (mettilo in variabile d'ambiente)
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        raise ValueError("GITHUB_TOKEN non trovato nelle variabili d'ambiente")
    
    endpoint = "https://models.inference.ai.azure.com/chat/completions"
    
    prompt = f"""
    Sei un professore di matematica esperto. Analizza questa funzione inversa:

    Funzione originale: f(x) = {funzione_di_partenza}
    Funzione inversa: f⁻¹(x) = {funzione_inversa}

   Fornisci uno studio COMPLETO della funzione inversa in formato JSON:

    {{
    "nome_funzione": "nome della funzione in italiano scritto in lettere",
    "dominio": "descrizione del dominio in notazione matematica",
    "codominio": "descrizione del codominio",
    "iniettivita": "spiegazione se è iniettiva",
    "suriettivita": "spiegazione se è suriettiva",
    "biettivita": "spiegazione se è biettiva",
    "monotonia": "crescente/decrescente/non monotona con spiegazione",
    "limiti": {{
    "x_meno_infinito": "valore del limite",
    "x_piu_infinito": "valore del limite",
    "limiti_notevoli": ["altri limiti importanti"]
  }},
  "asintoti": {{
    "verticali": ["lista"],
    "orizzontali": ["lista"],
    "obliqui": ["lista"]
  }},
  "punti_notevoli": {{
    "intersezione_assi": {{"x": null, "y": null}},
  }},
  "grafico_qualitativo": "descrizione del comportamento grafico",
  "spiegazione_completa": "spiegazione dettagliata in italiano per studenti"
    }}
    Rispondi SOLO con il JSON valido, senza markdown o altro testo.
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}"
    }
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Sei un professore di matematica che aiuta studenti con analisi matematica. Rispondi sempre in JSON valido."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "gpt-4o",
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Pulisci eventuali markdown
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
        
        studio = json.loads(content)
        return studio
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Errore nella chiamata API: {str(e)}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Errore nel parsing JSON: {str(e)}")

@app.post("/calcolo-analisi")
def calcola_funzione_inversa(input: FunctionInput):
    try:
        # Calcola la funzione inversa
        espressione, expr_inversa, y = calcola_inversa(input.function)
        
        # --- CALCOLO DEI PUNTI PER IL GRAFICO --- 
        # Passiamo 'y' perché l'inversa è in funzione di y.
        punti_x, punti_y = calcola_punti_grafico(expr_inversa, y)

        # Studio della funzione
        studio = studio_della_funzione(
            funzione_di_partenza=input.function,
            funzione_inversa=expr_inversa
        )
        
        return FunctionResult(
            funzione_di_partenza=latex(espressione),
            funzione_inversa=latex(expr_inversa),
            punti_x=punti_x,
            punti_y=punti_y,
            studio_della_funzione=studio
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))