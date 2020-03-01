

from parser import XMLParser

parser = XMLParser()

for x in range(1, 7):
    print(f"Test case {x}: ", end = "")
    doc = str(open(f'sample{x}/ccd.xml').read()).strip()
    query = str(open(f'sample{x}/query.txt').read()).strip().replace('\n', ' ')
    output = str(open(f'sample{x}/output.txt').read()).strip()
    
    document = parser.parse(doc).find('ClinicalDocument')

    if document.execute_query(query) == output:
        print('Correct. Found', output)
    else:
        print("Incorrect. Did not find", output)