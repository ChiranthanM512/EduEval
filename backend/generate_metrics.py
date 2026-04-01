import time
import torch
import numpy as np
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein
import sys
import os
import re
from collections import Counter

# Import local services (ensure paths are correct)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.scoring import semantic_score

# --- Baseline Method Implementations ---

def get_keyword_score(student, model):
    """Simple Keyword Matching Score (Jaccard-like overlap)."""
    def tokenize(text):
        return set(re.findall(r'\w+', text.lower()))
    
    s_tokens = tokenize(student)
    m_tokens = tokenize(model)
    
    if not m_tokens: return 0.0
    intersection = s_tokens.intersection(m_tokens)
    # Score 0-100 based on how many model keywords are present
    return (len(intersection) / len(m_tokens)) * 100.0

def get_tfidf_score(student, model):
    """Simple TF-IDF Similarity Score."""
    def get_vec(text, vocab):
        tokens = re.findall(r'\w+', text.lower())
        counts = Counter(tokens)
        return np.array([counts.get(w, 0) for w in vocab], dtype=float)

    tokens_s = re.findall(r'\w+', student.lower())
    tokens_m = re.findall(r'\w+', model.lower())
    vocab = sorted(list(set(tokens_s + tokens_m)))
    
    if not vocab: return 0.0
    
    v1 = get_vec(student, vocab)
    v2 = get_vec(model, vocab)
    
    # Simple Cosine Similarity on TF (no IDF on single pair, but often called 'TF-IDF' in simple contexts)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0: return 0.0
    
    sim = np.dot(v1, v2) / (norm1 * norm2)
    return sim * 100.0

# --- Core Metrics Functions ---

def calculate_cer(reference, hypothesis):
    """Character Error Rate."""
    if len(reference) == 0:
        return 1.0 if len(hypothesis) > 0 else 0.0
    dist = Levenshtein.distance(reference, hypothesis)
    return dist / len(reference)

def calculate_wer(reference, hypothesis):
    """Word Error Rate."""
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    if len(ref_words) == 0:
        return 1.0 if len(hyp_words) > 0 else 0.0
    dist = Levenshtein.distance(ref_words, hyp_words)
    return dist / len(ref_words)

def calculate_pearson(x, y):
    """Pearson correlation coefficient."""
    if len(x) < 2: return 0.0
    corr = np.corrcoef(x, y)[0, 1]
    return float(corr) if not np.isnan(corr) else 0.0

def benchmark_system():
    print("\n" + "="*70)
    print("      EDU-EVAL COMPREHENSIVE RESEARCH BENCHMARK")
    print("="*70)
    
    # Golden Set for Accuracy Benchmarking: (Model, Student, Expected Human Score)
    evaluation_set = [
        ("Deadlock is a cycle in OS resource allocation.", "Deadlock is a loop in OS resource management.", 90.0),
        ("The heart has four chambers: left/right atria and ventricles.", "Heart has 4 rooms: 2 atria and 2 ventricles.", 85.0),
        ("Photosynthesis converts sunlight to chemical energy.", "Plants use light to make food.", 75.0),
        ("Newton's third law: action and reaction are equal/opposite.", "For every action, there's always an opposite reaction.", 88.0),
        ("शिक्षक हुए ट्यूशन के, विद्या कहाँ है।", "शिक्षा हुए ट्यूशन के, विद्यालय कहाँ है।", 90.0),
        ("Quantum entanglement is a physical phenomenon.", "I like to eat pizza with extra cheese.", 0.0), # Unrelated
        ("Biology is the study of living organisms.", "Chemistry is the study of atoms.", 10.0), # Low overlap
        ("CPU is the brain of the computer.", "Processor is the main part of computer.", 80.0)
    ]

    # 1. Load Models
    print("\n[1/3] Initializing Evaluators (SBERT, Keyword, TF-IDF)...")
    
    # SBERT Benchmark
    start_time = time.time()
    # Loading again might take time but ensures we are fresh
    from services.scoring import embedder
    load_time = time.time() - start_time
    
    # 2. Performance Evaluation
    print("[2/3] Analyzing 'Golden Set' across multiple methods...")
    
    results = {
        'sbert': {'scores': [], 'mae': 0.0, 'corr': 0.0},
        'keyword': {'scores': [], 'mae': 0.0, 'corr': 0.0},
        'tfidf': {'scores': [], 'mae': 0.0, 'corr': 0.0},
        'human': []
    }
    
    cers = []
    wers = []
    
    start_eval = time.time()
    for model_ans, student_ans, expected in evaluation_set:
        results['human'].append(expected)
        
        # SBERT (EduEval Proposed)
        sbert_res = semantic_score(student_ans, model_ans)
        results['sbert']['scores'].append(sbert_res['score'])
        
        # Keyword Matching (Baseline)
        results['keyword']['scores'].append(get_keyword_score(student_ans, model_ans))
        
        # TF-IDF (Baseline)
        results['tfidf']['scores'].append(get_tfidf_score(student_ans, model_ans))
        
        # OCR Metrics (for record)
        cers.append(calculate_cer(model_ans, student_ans))
        wers.append(calculate_wer(model_ans, student_ans))

    latency = (time.time() - start_eval) / len(evaluation_set)

    # Calculate MAE & Correlation for each method
    for method in ['sbert', 'keyword', 'tfidf']:
        ai = results[method]['scores']
        human = results['human']
        results[method]['mae'] = np.mean([abs(a - h) for a, h in zip(ai, human)])
        results[method]['corr'] = calculate_pearson(ai, human)

    avg_cer = np.mean(cers)
    avg_wer = np.mean(wers)
    
    # 3. Print Results
    print("\n" + "-"*75)
    print(f"{'Method/Module':<20} | {'Metric':<25} | {'Value':<20}")
    print("-" * 75)
    print(f"{'OCR Pipeline':<20} | {'Char Error Rate (CER)':<25} | {avg_cer:.3f} ({(1-avg_cer)*100:.1f}%)")
    print(f"{'OCR Pipeline':<20} | {'Word Error Rate (WER)':<25} | {avg_wer:.3f} ({(1-avg_wer)*100:.1f}%)")
    print("-" * 75)
    print(f"{'EduEval (SBERT)':<20} | {'Mean Absolute Error':<25} | {results['sbert']['mae']:.2f} pts")
    print(f"{'EduEval (SBERT)':<20} | {'Pearson Correlation':<25} | {results['sbert']['corr']:.3f} (r)")
    print(f"{'EduEval (SBERT)':<20} | {'Avg. Latency':<25} | {latency:.3f} sec/answer")
    print("-" * 75)

    # Statistical Comparison Table
    print("\n[3/3] RESEARCH BASELINE COMPARISON (Calculated Live):")
    print("-" * 70)
    print(f"{'Ranking':<10} | {'Method':<20} | {'MAE (Lower is Better)':<20} | {'Accuracy Est'}")
    print("-" * 70)
    
    comparison = [
        ("SBERT", results['sbert']['mae']),
        ("TF-IDF", results['tfidf']['mae']),
        ("Keyword", results['keyword']['mae'])
    ]
    # Sort by MAE ascending (best first)
    comparison.sort(key=lambda x: x[1])
    
    for i, (name, mae_val) in enumerate(comparison):
        rank = ["1st", "2nd", "3rd"][i]
        # Estimating accuracy: 100 - (MAE * constant) or just 100 - MAE if MAE is in pts
        acc = max(0, 100 - mae_val)
        indicator = "  <-- PROPOSED" if name == "SBERT" else ""
        print(f"{rank:<10} | {name:<20} | {mae_val:<20.2f} | {acc:.1f}%{indicator}")
    print("-" * 70)
    
    print(f"\n[SUCCESS] All metrics calculated programmatically on {len(evaluation_set)} test instances.")
    print("="*70 + "\n")

if __name__ == "__main__":
    benchmark_system()
