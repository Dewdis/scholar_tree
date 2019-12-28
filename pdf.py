import sys
import re
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text(file_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


def extract_references_list(text):
    matching_result = re.search('REFERENCES', text)
    references_text = text[matching_result.span()[0]:]
    print(references_text)
    # WARNING: not more than 999 references!
    index_re = re.compile('\[[0-9]([0-9]|)([0-9]|)\]')
    for reference in index_re.finditer(references_text):
        print(references_text[reference.span()[0]:reference.span()[1]])


if __name__ == '__main__':
    text = extract_text(sys.argv[1])
    #print(text)
    extract_references_list(text)
