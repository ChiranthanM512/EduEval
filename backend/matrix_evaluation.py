import os
import sys
from tabulate import tabulate
from services.scoring import semantic_score

def run_evaluation():
    print("\n" + "="*80)
    print("      EDU-EVALVE MODEL PREDICTION MATRIX EVALUATION")
    print("="*80 + "\n")

    # Define Test Cases: (Label, Model Answer, Student Answer)
    test_cases = [
        (
            "English: Exact Match",
            "Deadlock is a condition in an operating system where a group of processes are unable to proceed...",
            "Deadlock is a condition in an operating system where a group of processes are unable to proceed..."
        ),
        (
            "English: Severe OCR (Peacock)",
            "Deadlock is a condition in an operating system...",
            "peacock is a condition in an operating system..."
        ),
        (
            "Hindi: Poem - Near Match",
            "शिक्षक हुए ट्यूशन के, विद्या कहाँ है। प्रोग्राम हुए चैनल के, संस्कार कहाँ हैं।",
            "शिक्षा हुए ट्यूशन के, विद्यालय कहाँ है। प्रोग्राम हुए चैनल के, शंकरा कहाँ हैं।"
        ),
        (
            "Hindi: Exact Match",
            "शिक्षक हुए ट्यूशन के, विद्या कहाँ है।",
            "शिक्षक हुए ट्यूशन के, विद्या कहाँ है।"
        ),
        (
            "Hindi: Unrelated",
            "शिक्षक हुए ट्यूशन के, विद्या कहाँ है।",
            "There are several jobs, Admin, and IT, related which are since..."
        ),
        (
            "English: Correct Concept, Different Wording",
            "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize nutrients from carbon dioxide and water.",
            "Plants use sunlight to make food from CO2 and water. This is called photosynthesis."
        )
    ]

    results = []
    
    for label, model_ans, student_ans in test_cases:
        score_data = semantic_score(student_ans, model_ans)
        
        # Categorization logic for Confusion Matrix
        similarity = score_data['similarity']
        
        # We define a 'Acceptable' match as Similarity > 0.45 for educational contexts
        status = "✅ PASS" if similarity > 0.45 else "❌ FAIL"
        if similarity < 0.22: # NOT_RELATED_THRESHOLD
            status = "🚨 UNRELATED"

        results.append([
            label,
            f"{similarity:.4f}",
            f"{score_data['score']}%",
            status
        ])

    # Print Results Table
    headers = ["Test Case", "Similarity", "Grade Score", "Status"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
    
    print("\n" + "="*80)
    print("                     EVALUATION SUMMARY")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for r in results if "PASS" in r[3])
    unrelated = sum(1 for r in results if "UNRELATED" in r[3])
    
    print(f"Total Test Cases: {total}")
    print(f"Successful Matches (>0.45 sim): {passed} ({passed/total*100:.1f}%)")
    print(f"Failed Matches: {total - passed - unrelated}")
    print(f"Unrelated Detections: {unrelated}")
    print("="*80 + "\n")

if __name__ == "__main__":
    # Ensure backend root is in path for imports
    sys.path.append(os.getcwd())
    
    try:
        from services.scoring import embedder
        run_evaluation()
    except Exception as e:
        print(f"ERROR: Could not run evaluation: {e}")
