from django.utils.html import escape, format_html

def higlight(text, term):
    if not term:
        return escape(text)
    
    text_l = text.lower()
    term_l = term.lower()
    start = text_l.find(term_l)
    if start == -1:
        return escape(text)
    
    end = start + len(term)

    return format_html(
        "{}<span>{}</span>{}",
        escape(text[:start]),
        escape(text[start:end]),
        escape(text[end:])
    )