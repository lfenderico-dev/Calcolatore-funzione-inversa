from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sympy import symbols, Eq, solve, parse_expr, latex, lambdify
import numpy as np
from typing import List, Optional
import traceback
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

@app.post("/calculate-inverse")
def calcola_funzione_inversa(input: FunctionInput):
    try:
        # definisci i simboli
        x, y = symbols('x y')
        
        # convertire la stringa in espressione matematica
        espressione = parse_expr(input.function)
        
        # creaiamo l'equazione y = f(x)
        funzione_originale = Eq(y, espressione)
        # troviamo la funzione inversa risolvendo l'equazione per x
        soluzioni = solve(funzione_originale, x)
        
        if not soluzioni:
            raise ValueError("Impossibile trovare l'inversa")
        expr_inversa = soluzioni[0]
        
        # --- CALCOLO DEI PUNTI PER IL GRAFICO ---
        # Usiamo la funzione helper. Passiamo 'y' perché l'inversa è in funzione di y.
        punti_x, punti_y = calcola_punti_grafico(expr_inversa, y)
        
        return FunctionResult(
            funzione_di_partenza=latex(espressione),
            funzione_inversa=latex(expr_inversa),
            punti_x=punti_x,
            punti_y=punti_y
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
