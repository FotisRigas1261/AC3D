# ###CREATE REPORT FOR VISUALISATION
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.platypus.tables import Table, TableStyle
# import re


# def createreport(UniprotID,FASTA):
#     pdf_doc = SimpleDocTemplate("my_report.pdf", pagesize=letter)
#     elements = []

#     styles = getSampleStyleSheet()
#     normal_style = styles['Normal']

#     #Title of report
#     title = Paragraph("Lysine Acetylation Analysis of "+UniprotID, styles['Title'])
#     elements.append(title)
#     elements.append(Spacer(1, 12))

#     #Take the species
#     match = re.search(r'OS=([^\s]+)', FASTA)

#     if match:
#         species = match.group(1)
#     else:
#         print("FASTA format error")

#     species = Paragraph("Species: "+species)
#     fasta = Paragraph(FASTA)

#     elements.append(species)
#     elements.append(fasta)
#     pdf_doc.build(elements)