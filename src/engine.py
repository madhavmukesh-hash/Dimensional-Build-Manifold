import numpy as np
import pandas as pd

def get_manifold_metrics(ret_df, window=60):
    """
    Computes Dimensional Build metrics: Spectral Entropy, Effective Dimensions, 
    and Entropy Velocity (The Spike Detector).
    Takes a dataframe of log returns and a rolling window size.
    """
    results = pd.DataFrame(index=ret_df.index)
    entropies = []
    eff_dims = []

    for i in range(len(ret_df)):
        if i < window:
            entropies.append(np.nan)
            eff_dims.append(np.nan)
            continue
            
        # Extract the N-dimensional correlation slice
        c_mat = ret_df.iloc[i-window:i].corr().values
        evals = np.linalg.eigvalsh(c_mat)
        evals = np.clip(evals, 1e-10, None) 
        
        # 1. Spectral Entropy (H)
        p = evals / np.sum(evals)
        h = -np.sum(p * np.log(p))
        
        # 2. Effective Dimensions (Identity N_eff = e^H)
        # Replaced Participation Ratio with exponential to match bimodal physics
        n_eff = np.exp(h)
        
        entropies.append(h)
        eff_dims.append(n_eff)

    results['Entropy'] = entropies
    results['Eff_Dim'] = eff_dims
    
    # 3. Entropy Velocity (5-day Kinetic Acceleration)
    results['H_Velocity'] = results['Entropy'].diff(5).abs()
    
    return results

def prepare_ai_build_tensor(ret_df, target_date, window=60):
    """
    Extracts the un-collapsed Eigenvalue Spectrum for LLM Semantic Prompting.
    """
    idx = ret_df.index.get_loc(pd.to_datetime(target_date))
    c_mat = ret_df.iloc[idx-window:idx].corr().values
    
    # High to Low sorting
    evals = np.linalg.eigvalsh(c_mat)[::-1] 
    # Safeguard against negative eigenvalues from floating point math
    evals = np.clip(evals, 1e-10, None) 
    
    p = evals / np.sum(evals)
    h = -np.sum(p * np.log(p))
    
    return {
        "date": target_date,
        "spectral_entropy": round(h, 4),
        "eigenvalues": [round(e, 3) for e in evals],
        "dominant_collapse_pct": round(p[0] * 100, 2)
    }