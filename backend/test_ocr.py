from services.hybrid_ocr import hybrid_ocr

print("Starting OCR extraction...")
res = hybrid_ocr.extract_text('uploads/f504bcfdeddb4cd5931370172abff20a.jpeg', hint_text='deadlock condition operating system processes proceed resource')
print('OCR RESULT:')
print(repr(res))
