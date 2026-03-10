# autopoiesis.py
from memory import Procedural
import importlib, types, time, uuid

def propose_skill(task_signature:str, examples:list[str], constraints:str)->str:
    """
    Use your LLM to emit Python function code implementing a tool or macro.
    Return code as string (validated by Gatekeeper).
    """
    ...

def load_skill(runtime_code:str):
    mod = types.ModuleType(f"skill_{uuid.uuid4().hex}")
    exec(runtime_code, mod.__dict__)
    # Expect function named 'run(payload: dict) -> dict'
    return mod.run

def evaluate_skill(run_fn, testset):
    wins=0; total=len(testset)
    for t in testset:
        try:
            out=run_fn(t["input"])
            wins += 1 if t["metric"](out) else 0
        except: pass
    return wins/total if total else 0.0

def autopoiesis_loop(proc: Procedural, failing_signature, testset):
    code = propose_skill(failing_signature, [t["input"] for t in testset], constraints="no external net; timeouts; logs")
    run_fn = load_skill(code)
    score = evaluate_skill(run_fn, testset)
    if score >= 0.6:  # retention threshold
        proc.register(failing_signature, run_fn, {"score": score, "created_at": time.time()})
        return True, score
    return False, score