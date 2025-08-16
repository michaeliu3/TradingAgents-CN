import pandas as pd
from datetime import datetime, timedelta
import json
import os
import time
from pathlib import Path # Import the Path object

# Import the necessary components from the TradingAgents framework
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# --- Part 1: Your Custom Configuration ---
def get_my_custom_config():
    """
    Creates and returns your specific custom configuration using Gemini models.
    """
    config = DEFAULT_CONFIG.copy()
    config.update({
        "llm_provider": "google",
        "deep_think_llm": "gemini-2.5-pro",
        "quick_think_llm": "gemini-2.0-flash",
        "max_debate_rounds": 5,
        "max_risk_discuss_rounds": 3,
        "online_tools": True,
    })
    selected_analysts = ["market", "fundamentals", "news"]
    print("✅ Custom configuration loaded with Gemini models.")
    return config, selected_analysts

# --- Part 2: Modified Batch Analysis Function ---
def batch_analysis(symbols, date, config, selected_analysts):
    """
    Performs batch analysis on a list of stocks using the provided configuration.
    """
    print("\n--- Starting Batch Analysis ---")
    ta = TradingAgentsGraph(
        debug=False,
        config=config,
        selected_analysts=selected_analysts
    )
    results = []
    for symbol in symbols:
        try:
            print(f"Analyzing {symbol}...")
            state, decision = ta.propagate(symbol, date)
            result = {
                "symbol": symbol,
                "action": decision.get("action", "hold"),
                "confidence": decision.get("confidence", 0.5),
                "risk_score": decision.get("risk_score", 0.5),
                "reasoning": decision.get("reasoning", "")
            }
            results.append(result)
            print(f"✅ {symbol}: {result['action']} (Confidence: {result['confidence']:.1%})")
        except Exception as e:
            print(f"❌ {symbol}: Analysis failed - {e}")
            results.append({
                "symbol": symbol, "action": "error", "confidence": 0.0,
                "risk_score": 1.0, "reasoning": f"Analysis failed: {e}"
            })
    print("--- Batch Analysis Complete ---")
    return pd.DataFrame(results)

# --- Part 3: Function to Save Results for Download (MODIFIED) ---
def save_dataframe_to_json(df, filename_prefix):
    """
    Saves a pandas DataFrame to the user's main Downloads folder.
    """
    # --- THIS IS THE MODIFIED SECTION ---
    # Find the user's Downloads folder dynamically
    results_dir = Path.home() / "Downloads"
    # Create it if it doesn't exist (unlikely, but safe)
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Use os.path.join to correctly create the full file path
    filepath = os.path.join(results_dir, f"{filename_prefix}_{timestamp}.json")
    
    df.to_json(filepath, orient='records', indent=2)
    
    print(f"✅ Results successfully saved to your Downloads folder: {filepath}")
    return filepath

# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Get your custom configuration
    my_config, my_analysts = get_my_custom_config()
    
    # 2. Define parameters for the batch analysis
    stocks_to_analyze = ["MARA","PFE"]
    analysis_date = "2025-08-01"
    
    # 3. Run the batch analysis
    batch_results_df = batch_analysis(stocks_to_analyze, analysis_date, my_config, my_analysts)
    print("\n=== Batch Analysis Results ===")
    
    # Set pandas display option to show full text in columns
    pd.set_option('display.max_colwidth', None)
    
    print(batch_results_df[["symbol", "action", "confidence", "risk_score", "reasoning"]])
    
    # 4. Save the batch analysis results
    save_dataframe_to_json(batch_results_df, "batch_analysis_results")

    print("\nAll tasks completed!")