import re

DEFAULT_MULTIPLE = 1
THOUSAND_FACTOR = 1000


class CurrencyConverter():

    def __init__(self):
        self._DOUBLE_CENTS = re.compile(r",\d\d,\d\d$")  # ,00,00
        self._DOT_DECIMAL_SEP = re.compile(r"\.\d\d$")  # .00
        self._THOUSAND_WITHOUT_COMMA = re.compile(r"\.\d{3}$")  # .000
        self._START_NOT_CURRENCY = re.compile(r"^([^0-9]*)")  # Iniciar com qualquer caractere que não seja número.
        self._END_NOT_CURRENCY = re.compile(r"([^0-9]*)$")  # Terminar com qualquer caractere que não seja número.
        self._VALUE_WITH_THOUSAND_MULTIPLY = re.compile(r"^R \$ .* mil$")  # 15 mil
        self._GENERIC_REPLACE_PATTERN = re.compile(r"^R4")
        self._FOREIGN_COIN = re.compile(r"(?i)^(Cr|cr|cz|Cz|US \$|USD \$|COL \$)")
        self._LIST_OF_VALUES = re.compile(r"^(R \$ )*\d{1,3}(\.\d{3})*,\d{2} \d{1,3}(\.\d{3})*,\d{2}")  # 10,00 20,00
        self._HIGHWAY_NUMBER = re.compile(r"^RS \d{1,3}$")
        self._DETACHED_NUMBER = re.compile(r"^\d{1,}$")
        self._CONCATENED_CENTS = re.compile(r"\.\d{5}$")  # XX.00000
        self._THOUSAND_4_DIGITS = re.compile(r"\.\d{4}$")  # .0000
        self._THOUSAND_4_DIGITS_WITH_DECIMAL = re.compile(r"\.\d{4},\d{2}$")  # XX.0000,00
        self._THOUSAND_REDUCED = re.compile(r"\.\d{2},\d{2}$")  # XX.00,00
        self._THOUSAND_BROKEN = re.compile(r"\.\d{1}\.\d{2},\d{2}$")  # XX.0.00,00
        self._NOT_CURRENCY = re.compile(r"^RT.*$")

    def fix_list(self, value: list, keep_null_values=False):
        if keep_null_values:
            return [self.fix(x) for x in value]
        else:
            return [converted_value for converted_value in [self.fix(x) for x in value] if converted_value is not None]

    def fix(self, value: str):
        multiply_factor = self._get_multiply_factor(value)
        decimal_value = 0.0

        if self._value_is_currency(value):
            value = self._GENERIC_REPLACE_PATTERN.sub("", value)
            value = self._START_NOT_CURRENCY.sub("", value)
            value = self._END_NOT_CURRENCY.sub("", value)

            if self._DETACHED_NUMBER.match(value) and multiply_factor == DEFAULT_MULTIPLE:
                value = ""

            # Se terminar com 5 dígitos, considerar 2 últimos dígitos.* Padrão identificado após analise manual.
            if len(self._CONCATENED_CENTS.findall(value)) > 0:
                value = value[0: -2] + "," + value[-2:]

            value = self._adjust_thousand_4digits(value)
            value = self._adjust_broken_resumed_thousand(value)

            if len(self._DOUBLE_CENTS.findall(value)) > 0:
                value = value[:-3]

            if len(self._DOT_DECIMAL_SEP.findall(value)) > 0:
                last_dot_index = str(value).rfind(".")
                value = value[: last_dot_index] + "," + value[last_dot_index + 1:]

            value = self._adjust_decimal(value)

            try:
                decimal_value = float(value.replace(".", "").replace(",", "."))
            except ValueError:
                pass

        decimal_value = decimal_value * multiply_factor

        if decimal_value > 0:
            return decimal_value
        else:
            return None

    def _get_multiply_factor(self, value):
        multiply_factor = DEFAULT_MULTIPLE

        if self._VALUE_WITH_THOUSAND_MULTIPLY.match(value):
            multiply_factor = THOUSAND_FACTOR

        return multiply_factor

    def _value_is_currency(self, value):
        return value and len(value) > 0 and \
               (not self._FOREIGN_COIN.match(value)) and \
               (not self._LIST_OF_VALUES.match(value)) and \
               (not self._HIGHWAY_NUMBER.match(value)) and \
               (not self._NOT_CURRENCY.match(value))

    def _adjust_thousand_4digits(self, value):
        # Se parte de milhar possuir 4 dígitos, considerar apenas 3 primeiros. *Padrão identificado após analise manual.

        if len(self._THOUSAND_4_DIGITS.findall(value)) > 0:
            valor_temp = value[0:len(value) - 1]
            value = value[:-1]
        if len(self._THOUSAND_4_DIGITS_WITH_DECIMAL.findall(value)) > 0:
            comma_index = value.rfind(",")
            valor_temp = value[0: comma_index - 1] + value[comma_index:]
            value = value[: comma_index - 1] + value[comma_index:]
        return value

    def _adjust_broken_resumed_thousand(self, value):
        if len(self._THOUSAND_BROKEN.findall(value)) > 0:
            last_dot_index = value.rfind(".")
            value = value[: last_dot_index] + value[last_dot_index + 1:]

        # Padrão "milhar resumido" deve ser aplicado apenas APÓS verificar "milhar quebrado", pois o regex é mais genérico;
        # *Padrão identificado após analise manual.
        if len(self._THOUSAND_REDUCED.findall(value)) > 0:
            last_dot_index = value.rfind(".")
            value = value[: last_dot_index + 1] + "0" + value[last_dot_index + 1:]
        return value

    def _adjust_decimal(self, value):
        last_comma_index = value.rfind(",")
        index_decimal_part = last_comma_index

        if last_comma_index < 0:
            if len(self._THOUSAND_WITHOUT_COMMA.findall(value)) > 0:
                index_decimal_part = len(value)
        if index_decimal_part > 0:
            number_part = value[:index_decimal_part].replace(",", "").replace(".", "").replace(" ", "").strip()
            decimal_part = value[index_decimal_part:].replace(" ", "")
            value = number_part + decimal_part

        return value
