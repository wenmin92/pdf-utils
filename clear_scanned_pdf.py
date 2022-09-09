import fitz
import re

file_path = r'D:\Downloads\test.pdf'

doc = fitz.open(file_path)
for page in doc:
    page.clean_contents()
    xref = page.get_contents()[0]
    cont = doc.xref_stream(xref)
    new_cont = re.search(b'q\\n.*Do\\nQ\\n', cont, flags=re.S)[0]
    doc.update_stream(xref, new_cont)
    print(new_cont)

new_file_path = re.sub(r'\\([^\\]+)\.pdf', r'\\\1_optimized.pdf', file_path)
doc.save(new_file_path, garbage=4, deflate=True, clean=True)
