import fitz  # PyMuPDF
import re

file_path = r'D:\Downloads\test.pdf'
pattern = b'q\\n/\\w+ gs\\n1 0 0 1 210 \\d\\.\\d{,2} cm\\n0 0 1 rg\\nBT\\n/QQAPF5cabeeee 10 Tf\\n1 0 0 1 0 0 Tm\\n\\(www\\.it-ebooks\\.info\\) Tj\\nET\\nQ\\n'

doc = fitz.open(file_path)
for page in doc:
    # remove watermarks
    page.clean_contents()
    xref = page.get_contents()[0]
    cont = doc.xref_stream(xref)
    if b'www.it-ebooks.info' in cont:
        print(f'Found watermark on page {page.number}')
        new_cont = re.sub(pattern, b'', cont, flags=re.S)
        new_cont = re.sub(b'q\\nQ\\n', b'', new_cont, flags=re.S)
        doc.update_stream(xref, new_cont)

    # remove links
    for link in page.links():
        if link.get('uri') == 'http://www.it-ebooks.info':
            print(f'Found link on page {page.number}')
            page.delete_link(link)
    print('---')

new_file_path = re.sub(r'\\([^\\]+)\.pdf', r'\\\1_optimized.pdf', file_path)
doc.save(new_file_path, garbage=4, deflate=True, clean=True)