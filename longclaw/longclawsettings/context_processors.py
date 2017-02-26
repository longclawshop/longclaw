from longclaw.longclawsettings.models import LongclawSettings

def currency(request):
    settings = LongclawSettings.for_site(request.site)
    return {
        'currency_html_code': settings.currency_html_code,
        'currency': settings.currency
    }
