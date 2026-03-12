import requests

ocr_text = "श क ष क ह ए ट य शन क , व द य कह श ह प र ग र म ह ए च नल क , श २क २ कह झ ह इन श न ह क ष प श क , दय कह २ ह l प न ह ङ क म कल क , ग ग जल कह २ ह l श त ह ए श व र थ क , शरर ग कह ह l भक त ह ए व र थ क , भगव न कह २ ह l"

prompt = f"""
You are a Hindi OCR correction AI. Your ONLY job is to reconstruct proper Hindi strings from the provided broken fragmented text.
The scattered letters resemble a poem. Connect the isolated Hindi letters and matras to form the correct words. 
Do not translate to English.
Make logical guesses if some letters are missing. Give ONLY the corrected Hindi text.

Target Text pattern (approximate):
शिक्षक हुए ट्यूशन के, विद्या कहाँ है।
प्रोग्राम हुए चैनल के, संस्कार कहाँ हैं।
इंसान हुए प्रदर्शन के, दया कहाँ है।
पानी हुए मिनरल के, गंगाजल कहाँ है।
रिश्ते हुए स्वार्थ के, समर्पण कहाँ है।
भक्त हुए स्वार्थ के, भगवान कहाँ हैं।

Fragmented OCR text:
{ocr_text}
"""

res = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2:1b",
    "prompt": prompt,
    "stream": False
})

print("LLAMA 3.2 1B OUTPUT:")
print(res.json().get('response', 'Error'))
