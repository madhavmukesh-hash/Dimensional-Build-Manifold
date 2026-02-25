import numpy as np

def print_regime_comparison(metrics_df, regimes_dict):
    """
    Prints a formatted, crisp comparison table of structural regimes 
    (Tear, Collapse, and Grounded) based on Spectral Entropy.
    """
    print(f"\n{'Regime Window':<25} | {'Spectral Entropy':<18} | {'Eff_Dim (N_eff)':<16} | {'Structural State'}")
    print("-" * 85)

    for name, date_str in regimes_dict.items():
        try:
            row = metrics_df.loc[date_str]
            h_val = row['Entropy']
            
            # Handle Eff_Dim whether it's pre-calculated in the df or needs calculating
            eff_dim = row['Eff_Dim'] if 'Eff_Dim' in metrics_df.columns else np.exp(h_val)
            
            # Determine the bimodal state dynamically
            if h_val > 1.85:
                state = "TEAR (Fragmented)"
            elif h_val < 1.45:
                state = "COLLAPSE (Singularity)"
            else:
                state = "GROUNDED (Stable)"
                
            print(f"{name:<25} | {h_val:<18.4f} | {eff_dim:<16.2f} | {state}")
            
        except KeyError:
            print(f"{name:<25} | Data for {date_str} unavailable.")
            
    print("\n" + "="*85)
    print("[THEORY VALIDATION: THE BIMODAL MANIFOLD]")
    print("TEAR REGIMES:     Expect Entropy > 1.85 (Manifold fragmenting; exit to Cash)")
    print("COLLAPSE REGIMES: Expect Entropy < 1.45 (Systemic singularity; rotate to GLD/TLT)")
    print("GROUNDED REGIMES: Expect Entropy 1.45 - 1.85 (Healthy structure; maintain Equities)")
    print("="*85)