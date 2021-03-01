from wagtail.core import blocks

class DiscountPercentageBlock(blocks.StructBlock):
    discount_type_name = 'Percentage'
    percentage = blocks.IntegerBlock(
        min_value=0,
        max_value=100,
        help_text='A value between 0 and 100 which represents the percentage discount',
    )

class DiscountDollarBlock(blocks.StructBlock):
    discount_type_name = 'Dollar'
    dollar = blocks.DecimalBlock(
        min_value=0,
        decimal_places=2,
        help_text='A value with a minimum of 0 which represents a flat dollar discount amount',
    )
