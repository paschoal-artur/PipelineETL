import scrapy
import re

class SmartphoneSpider(scrapy.Spider):
    name = "smartphone"
    allowed_domains = ["mercadolivre.com.br"]
    start_urls = [
        "https://lista.mercadolivre.com.br/celulares-telefones/celulares-smartphones/smartphone_NoIndex_True"
    ]

    start_page = 1
    max_page = 20

    def parse(self, response):
        products = response.css('li.ui-search-layout__item')

        for product in products:
            # 1) pega as frações como texto bruto
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            old_text = prices[0] if len(prices) > 0 else None
            new_text = prices[1] if len(prices) > 1 else None

            # 2) função para limpar separador de milhar e converter decimal
            def clean_price(txt):
                if not txt:
                    return None
                # remove pontos de milhar, troca vírgula decimal por ponto
                normalized = txt.replace('.', '').replace(',', '.')
                try:
                    return float(normalized)
                except ValueError:
                    return None

            old_price = clean_price(old_text)
            new_price = clean_price(new_text)

            installments_raw = " ".join(
                product.css('span.poly-price__installments *::text').getall()
            )

            # 1) número de parcelas
            installments = None
            m1 = re.search(r'(\d+)\s*x', installments_raw)
            if m1:
                installments = int(m1.group(1))

            # 2) valor da parcela (novo)
            valores = re.findall(r'R\$[\s]?([\d\.,]+)', installments_raw)
            if valores:
                per_installment = valores[1] if len(valores) > 1 else valores[0]
                credit_price = float(per_installment.replace('.', '').replace(',', '.'))
            else:
                credit_price = None


            yield {
                'brand': product.css('span.poly-component__brand::text').get(),
                'name': product.css('a.poly-component__title::text').get(),
                'seller': product.css('span.poly-component__seller::text').get(),
                'reviews_rating_number': product.css('span.poly-reviews__rating::text').get(),
                'reviews_amount': product.css('span.poly-reviews__total::text').get(),
                'old_price': old_price,
                'new_price': new_price,
                'credit_price': credit_price,
                'installments': installments,
            }

        # paginação
        if self.start_page < self.max_page:
            next_page = response.css(
                'li.andes-pagination__button.andes-pagination__button--next '
                'a::attr(href)'
            ).get()


            self.logger.debug(f"PÁGINA {self.start_page} -> {next_page}")

            if next_page:
                self.start_page += 1
                yield response.follow(next_page, callback=self.parse)