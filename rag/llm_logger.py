import os
import time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase_client  = create_client( 
                        os.getenv("SUPABASE_URL"),
                        os.getenv("SUPABASE_KEY")
                        )

COST_PER_1k_PROMPT_TOKENS = 0.00006
COST_PER_1k_COMPLETION_TOKENS = 0.00006

def calculate_cost(prompt_tokens: int, completion_tokens:int)->float:
    prompt_cost = (prompt_tokens / 1000) * COST_PER_1k_PROMPT_TOKENS
    completion_cost = (completion_tokens / 1000) * COST_PER_1k_COMPLETION_TOKENS
    return round(prompt_cost + completion_cost, 6)

def logged_llm_call(client,model:str,messages:list,note_id:str=None, **kwargs):
    start_time = time.time()
    success = True
    error = None
    response = None
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
    
    except Exception as e:
        
        success = False
        error = str(e)
        raise
    finally:
        latency_ms = int((time.time() - start_time) * 1000)
        
        if response and response.usage:
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
        else:
            prompt_tokens = completion_tokens = total_tokens = 0
        
        cost = calculate_cost(prompt_tokens, completion_tokens)
        
        try:
            supabase_client.table("llm_logs").insert({
                "note_id": note_id,
                "model": model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "cost_eur": cost,
                "latency_ms": latency_ms,
                "success": success,
                "error": error
            }).execute()
        except Exception as log_error:
            print(f"Warning: failed to write LLM log: {log_error}")
    
    return response