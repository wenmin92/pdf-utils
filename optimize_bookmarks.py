import fitz
import re

file_path = r'D:\Downloads\test.pdf'

doc = fitz.open(file_path)
outline_xrefs = doc.get_outline_xrefs()
for xref in outline_xrefs:
    xref_obj = doc.xref_object(xref)
    print(f'origin xref: {xref_obj}')

    # remove font color
    new_xref_obj = re.sub(r'/C\s*\[.*?]\n\s*', '', xref_obj)

    # simplify dest
    new_xref_obj = re.sub(r'/A\s*<<.*?(\[.*?]).*?>>', r'/Dest \1', new_xref_obj, flags=re.S)

    # unify jump position
    dest_xref = re.search(r'/Dest\s+\[\s*(\d+)', new_xref_obj).group(1)
    dest_page_xref_obj = doc.xref_object(int(dest_xref))
    dest_page_media_box = doc.xref_get_key(int(dest_xref), 'MediaBox')
    page_height = re.search(r'\s([.\d]+)\s*]', dest_page_media_box[1]).group(1)
    new_xref_obj = re.sub(r'(/Dest\s+\[.*)(\s+[.\d]+){2}\s+null\s+]', f'\\1 0 {page_height} null ]', new_xref_obj)

    # update xref
    doc.update_object(xref, new_xref_obj)
    print(f'new xref: {new_xref_obj}')
    print('------------------\n')

new_file_path = re.sub(r'\\([^\\]+)\.pdf', r'\\\1_optimized.pdf', file_path)
doc.save(new_file_path, garbage=4, deflate=True, clean=True)