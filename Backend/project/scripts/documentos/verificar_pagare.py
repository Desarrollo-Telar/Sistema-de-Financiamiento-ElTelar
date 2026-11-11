import importlib.util, sys, types
from pathlib import Path
from docx import Document
package=types.ModuleType('documentos_prueba')
package.__path__=['D:/Sistema-de-Financiamiento-ElTelar/Backend/project/scripts/documentos']
sys.modules[package.__name__]=package
spec=importlib.util.spec_from_file_location('documentos_prueba.pagare', 'pagare.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for n in (0,1,3,8):
    avalistas=[{'nombre':f'Persona {i}', 'dpi':'2526220971601','domicilio':f'Direccion {i}'} for i in range(n)]
    doc=Document(m.generar_pagare_word({'avalistas':avalistas}))
    text='\n'.join(p.text for p in doc.paragraphs)
    assert text.count('FIRMA DEL AVALISTA:')==n
    for i in range(n):
        assert f'Nombre: Persona {i}' in text
        assert f'Domicilio: Direccion {i}' in text
    if n:
        assert f'firmante {n+1}:' in text
    print(f'OK: {n} avalistas')
for entrada, esperado in [({'incluir_aval':True,'avalista_nombre':'Anterior'},1),({'avalistas':[{'nombre':'Oculto'}],'incluir_aval':False},0),({'avalista_nombre':'Anterior'},1)]:
    text='\n'.join(p.text for p in Document(m.generar_pagare_word(entrada)).paragraphs)
    assert text.count('FIRMA DEL AVALISTA:')==esperado
print('OK: compatibilidad y desactivacion explicita')
compile(Path('pagare.py').read_text(encoding='utf-8'), 'pagare.py', 'exec')
