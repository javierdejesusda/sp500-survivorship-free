import pandas as pd
import re

def categorize_change(reason):
    """
    Categoriza el motivo de un cambio en el S&P 500 basado en el texto de la razón.
    """
    if pd.isna(reason):
        return "Desconocido"
    
    reason_lower = str(reason).lower()
    
    if "merger" in reason_lower or "acquired" in reason_lower or \
       "acquisition" in reason_lower or re.search(r"\bacq\b", reason_lower) or \
       "bought" in reason_lower:
        return "Fusión/Adquisición"
    
    if "spin-off" in reason_lower or "spun off" in reason_lower:
        return "Spin-off"
    
    if "market cap" in reason_lower or "market capitalization" in reason_lower:
        return "Sustitución (Mercado)"
    
    if "reorganization" in reason_lower or "bankruptcy" in reason_lower:
        return "Reorganización"
    
    return "Otros"