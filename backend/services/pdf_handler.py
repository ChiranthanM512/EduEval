# import os
# import fitz  # PyMuPDF
# import uuid


# def pdf_to_images(pdf_path: str, out_dir="uploads/pdf_pages", dpi=250) -> list:
#     """
#     Converts PDF pages into PNG images using PyMuPDF (fast).

#     Returns:
#         List of image paths (one per page)
#     """

#     os.makedirs(out_dir, exist_ok=True)

#     doc = fitz.open(pdf_path)
#     image_paths = []

#     # unique id per pdf (avoids overwriting)
#     pdf_id = uuid.uuid4().hex[:8]
#     base_name = os.path.splitext(os.path.basename(pdf_path))[0]

#     zoom = dpi / 72  # 72 is default PDF DPI
#     mat = fitz.Matrix(zoom, zoom)

#     for page_num in range(len(doc)):
#         page = doc[page_num]

#         pix = page.get_pixmap(matrix=mat, alpha=False)

#         img_path = os.path.join(
#             out_dir,
#             f"{base_name}_{pdf_id}_page_{page_num+1}.png"
#         )

#         pix.save(img_path)
#         image_paths.append(img_path)

#     doc.close()
#     return image_paths
