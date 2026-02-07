import logging
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)

def render_to_pdf(template_src, context):
    """Render HTML template to PDF and return HTTP response."""
    logger.info(f"[PDF-UTILS] Starting PDF generation with context keys: {list(context.keys())}")
    
    try:
        template = get_template(template_src)
        logger.info(f"[PDF-UTILS] Template loaded successfully: {template_src}")
    except Exception as e:
        logger.error(f"[PDF-UTILS] Template loading failed: {e}")
        raise
    
    try:
        html = template.render(context)
        logger.info(f"[PDF-UTILS] Template rendered successfully, HTML length: {len(html)}")
    except Exception as e:
        logger.error(f"[PDF-UTILS] Template rendering failed: {e}")
        raise
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{context.get("donation_id", "unknown")}.pdf"'
    
    try:
        pisa_status = pisa.CreatePDF(html, dest=response)
        logger.info(f"[PDF-UTILS] PDF generation status: {pisa_status.err}")
        if pisa_status.err:
            logger.error("[PDF-UTILS] PDF generation had errors")
    except Exception as e:
        logger.error(f"[PDF-UTILS] PDF creation failed: {e}")
        raise
    
    logger.info(f"[PDF-UTILS] PDF generated successfully")
    return response
