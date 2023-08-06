from decimal import Decimal
from typing import List

TYPES = {
    'Numeric': Decimal,
    'Price': Decimal,
    'Real Quantity': Decimal,
    'Whole Quantity': Decimal,
    'Integer': int,
    # 'Unsigned': PositiveInt,
    'Boolean': bool,
    # 'Alphanumeric': constr(regex=r'^[a-zA-Z0-9]$'),
    'Text': str,
    # 'Date': constr(regex=r'^\d{8}$'),
    # 'Timestamp': constr(regex=r'^\d{8}[\s|T]\d{6}(.\d{3}(\d{6}){0,1}){0,1}$'),
    'Name/Value Pairs': dict,
    'Array': List,
    'Choice': str,
    'Symbol': str,
    'Message Type': str,
    'CAT Reporter IMID': str,
    'Exchange ID': str,
    'CAT Submitter ID': str,
    'Industry Memeber ID (IMID)': str,
    'Multi-Dimensional Array': List[List],
    'Trade Side Details': List[List],
    'Fulfillment Side Details': List[List],
    'Aggregated Orders': List[List],
}
