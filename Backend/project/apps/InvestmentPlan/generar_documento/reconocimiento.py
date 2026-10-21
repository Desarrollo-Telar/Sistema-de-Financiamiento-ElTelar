from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from .contrato_dinamico import texto

from apps.InvestmentPlan.models import InvestmentPlan

def generar_contrato(credito, garantias, ruta='contrato_dinamico.docx'):
    """Genera Word a partir del texto incorporado en este archivo."""

    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(11)
    for i, pagina in enumerate(texto(credito, garantias)):
        if i:
            doc.add_page_break()
        p = doc.add_paragraph(''.join(pagina))
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    doc.save(ruta)
    return ruta

if __name__ == "__main__":
    credito = InvestmentPlan.objects.get(id = 2)
    garantias = credito.garantias

    print("Documento creado:", generar_contrato(credito, garantias))