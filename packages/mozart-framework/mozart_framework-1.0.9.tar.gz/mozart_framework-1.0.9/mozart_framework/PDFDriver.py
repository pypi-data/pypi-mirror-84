# =============================================================
# =================     Library Import    =====================
# =============================================================

from tika import parser


# =============================================================
# =================        class          =====================
# =============================================================

# Classe PDF Responsável pela automatização do processo usando o PDF
class PDFAutomator:
    pdfFile = None

    def __init__(self):
        nothing = None


    def read_pdf(self, filePath):
        self.pdfFile = parser.from_file(filePath)