from longclaw.configuration.models import Configuration

def currency(request):
    config = Configuration.for_site(request.site)
    return {
        'currency_html_code': config.currency_html_code,
        'currency': config.currency
    }
