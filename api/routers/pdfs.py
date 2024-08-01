from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from typing import Optional

router = APIRouter()

@router.get("/pdfs/")
async def mostrar_pdf(pdf_link: Optional[str] = Query(..., description="Enlace o path al documento PDF")):
    print (pdf_link)
    if not pdf_link:
        return {"error": "Por favor proporciona un enlace válido a un documento PDF."}
    
    # Validar si el enlace termina en .pdf
    if not pdf_link.endswith(".pdf"):
        return {"error": "El enlace proporcionado no parece ser un enlace válido a un documento PDF."}
    
    # Puedes implementar más validaciones según tus necesidades, como verificar si el enlace es accesible, etc.
    # pdf_link = "http://10.222.48.245:8000"+pdf_link
    # Simplemente devolver el archivo PDF como respuesta
    return FileResponse(pdf_link, media_type='application/pdf', filename='documento.pdf', content_disposition_type='inline')
