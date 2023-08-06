EQUITY_EVENT_TITLES = {
    'MENO': 'New Order Event',
    'MENOS': 'Order Modified Supplement Event',
    'MEOR': 'Order Route Event',
    'MEMR': 'Route Modified',
    'MECR': 'Route Cancelled',
    'MEOA': 'Order Accepted',
    'MEIR': 'Order Internal Route Accepted',
    'MEIM': 'Order Internal Route Modified',
    'MEIC': 'Order Internal Route Cancelled',
    'MECO': 'Child Order',
    'MECOM': 'Child Order Modified',
    'MECOC': 'Child Order Cancelled',
    'MEOM': 'Order Modified',
    'MEOMS': 'Order Modified Supplement Event',
    'MEOJ': 'Order Adjusted',
    'MEOC': 'Order Cancelled',
    'MENQ': 'New Quote',
    'MEQR': 'Quote Received',
    'MEQC': 'Quote Cancelled',
    'MEOT': 'Trade Event',
    'MEOTS': 'Trade Supplement Event',
    'MEOF': 'Order Fulfillment',
    'MEFA': 'Order Fulfillment Amendment',
    'MEPA': 'Post Trade Allocation',
    'MEAA': 'Amended Allocation',
}
COMMON_FULFILLMENT_COLUMNS = (
   'actionType', 'errorROEID', 'firmROEID', 'type', 'CATReporterIMID', 'fillKeyDate', 'fulfillmentID', 'symbol'
)
COMMON_ORDER_COLUMNS = (
   'actionType', 'errorROEID', 'firmROEID', 'type', 'CATReporterIMID', 'orderKeyDate', 'orderID', 'symbol'
)
COMMON_QUOTE_COLUMNS = (
   'actionType', 'errorROEID', 'firmROEID', 'type', 'CATReporterIMID', 'quoteKeyDate', 'quoteID', 'symbol'
)
COMMON_TRADE_COLUMNS = (
   'actionType', 'errorROEID', 'firmROEID', 'type', 'CATReporterIMID', 'tradeKeyDate', 'tradeID', 'symbol'
)
EQUITY_EVENT_COLUMNS = {
    'MENO': (
        *COMMON_ORDER_COLUMNS,
        'eventTimestamp', 'manualFlag', 'electronicDupFlag', 'electronicTimestamp', 'manualOrderKeyDate',
        'manualOrderID', 'deptType', 'reservedForFutureUse', 'reservedForFutureUse', 'side', 'price', 'quantity',
        'minQty', 'orderType', 'timeInForce', 'tradingSession', 'handlingInstructions', 'custDspIntrFlag',
        'firmDesignatedID', 'accountHolderType', 'affiliateFlag', 'infoBarrierID', 'aggregatedOrders',
        'negotiatedTradeFlag', 'representativeInd', 'seqNum', 'atsDisplayInd', 'displayPrice', 'workingPrice',
        'displayQty', 'atsOrderType', 'nbbPrice', 'nbbQty', 'nboPrice', 'nboQty', 'nbboSource', 'nbboTimestamp',
    ),
    'MENOS': (
        *COMMON_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'aggregatedOrders', 'firmDesignatedID',
    ),
    'MEOR': (
        *COMMON_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'manualFlag', 'electronicDupFlag', 'electronicTimestamp', 'senderIMID',
        'destination', 'destinationType', 'routedOrderID', 'session', 'side', 'price', 'quantity', 'minQty',
        'orderType', 'timeInForce', 'tradingSession', 'affiliateFlag', 'isoInd', 'handlingInstructions',
        'routeRejectedFlag', 'dupROIDCond', 'seqNum',
    ),
    'MEOA': (
        *COMMON_ORDER_COLUMNS,
        'eventTimestamp', 'manualFlag', 'electronicDupFlag', 'electronicTimestamp', 'receiverIMID', 'senderIMID',
        'senderType', 'routedOrderID', 'manualOrderKeyDate', 'manualOrderID', 'affiliateFlag', 'deptType', 'side',
        'price', 'quantity', 'minQty', 'orderType', 'timeInForce', 'tradingSession', 'isoInd', 'handlingInstructions',
        'custDspIntrFlag', 'infoBarrierID', 'seqNum', 'atsDisplayInd', 'displayPrice', 'workingPrice', 'displayQty',
        'atsOrderType', 'nbbPrice', 'nbbQty', 'nboPrice', 'nboQty', 'nbboSource', 'nbboTimestamp',
    ),
    'MEIR': (
        *COMMON_ORDER_COLUMNS,
        'parentOrderKeyDate', 'parentOrderID', 'originatingIMID', 'eventTimestamp', 'manualFlag', 'electronicTimestamp',
        'deptType', 'receivingDeskType', 'infoBarrierID', 'side', 'price', 'quantity', 'minQty', 'orderType',
        'handlingInstructions', 'timeInForce', 'tradingSession',
    ),
    'MECO': (
        *COMMON_ORDER_COLUMNS,
        'parentOrderKeyDate', 'parentOrderID', 'originatingIMID', 'eventTimestamp', 'side', 'price', 'quantity',
        'minQty', 'orderType', 'timeInForce', 'tradingSession', 'handlingInstructions', 'seqNum', 'atsDisplayInd',
        'displayPrice', 'workingPrice', 'displayQty', 'nbbPrice', 'nbbQty', 'nboPrice', 'nboQty', 'nbboSource',
        'nbboTimestamp',
    ),
    'MECOM': (
        *COMMON_ORDER_COLUMNS,
        'priorOrderKeyDate', 'priorOrderID', 'originatingIMID', 'eventTimestamp', 'side', 'price', 'quantity',
        'minQty', 'leavesQty', 'orderType', 'timeInForce', 'tradingSession', 'handlingInstructions', 'seqNum',
        'atsDisplayInd', 'displayPrice', 'workingPrice', 'displayQty', 'nbbPrice', 'nbbQty', 'nboPrice', 'nboQty',
        'nbboSource', 'nbboTimestamp',
    ),
    'MECOC': (
        *COMMON_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'side', 'cancelQty', 'leavesQty', 'reservedForFutureUse', 'seqNum',
    ),
    'MEOM': (
        *COMMON_ORDER_COLUMNS,
        'priorOrderKeyDate', 'priorOrderID', 'originatingIMID', 'eventTimestamp', 'manualFlag', 'manualOrderKeyDate',
        'manualOrderID', 'electronicDupFlag', 'electronicTimestamp', 'receiverIMID', 'senderIMID', 'senderType',
        'routedOrderID', '_reservedForFutureUse', '_reservedForFutureUse2', '_reservedForFutureUse3',
        'reservedForFutureUse4', 'initiator', 'side', 'price', 'quantity', 'minQty', 'leavesQty', 'orderType',
        'timeInForce', 'tradingSession', 'isoInd', 'handlingInstructions', 'custDspIntrFlag', 'infoBarrierID',
        'aggregatedOrders', 'representativeInd', 'seqNum', 'atsDisplayInd', 'displayPrice', 'workingPrice',
        'displayQty', 'atsOrderType', 'nbbPrice', 'nbbQty', 'nboPrice', 'nboQty', 'nbboSource', 'nbboTimestamp',
    ),
    'MEOMS': (
        *COMMON_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'aggregatedOrders',
    ),
    'MEOJ': (
        *COMMON_ORDER_COLUMNS,
        'priorOrderKeyDate', 'priorOrderID', 'originatingIMID', 'eventTimestamp', 'manualFlag', 'electronicTimestamp',
        'initiator', 'price', 'quantity', 'minQty', 'leavesQty', 'seqNum', 'atsDisplayInd', 'displayPrice',
        'workingPrice', 'displayQty', 'nbbPrice', 'nbbQty', 'nboPrice', 'nboQty', 'nbboSource', 'nbboTimestamp',
    ),
    'MEOC': (
        *COMMON_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'manualFlag', 'electronicTimestamp', 'cancelQty', 'leavesQty', 'initiator',
        'seqNum',
    ),
    'MENQ': (
        *COMMON_QUOTE_COLUMNS,
        'priorQuoteKeyDate', 'priorQuoteID', 'eventTimestamp', 'seqNum', 'senderIMID', 'destination', 'routedQuoteID',
        'onlyOneQuoteFlag', 'bidPrice', 'bidQty', 'askPrice', 'askQty', 'firmDesignatedID', 'accountHolderType',
        'unsolicitedInd', 'mpStatusCode', 'quoteRejectedFlag',
    ),
    'MEQR': (
        *COMMON_QUOTE_COLUMNS,
        'receivedQuoteID', 'eventTimestamp', 'seqNum', 'receiverIMID', 'senderIMID', 'onlyOneQuoteFlag',
        'priorQuoteKeyDate', 'priorQuoteID', 'bidPrice', 'bidQty', 'askPrice', 'askQty', 'mpStatusCode',
        'unsolicitedInd', 'quoteWantedInd',
    ),
    'MEQC': (
        *COMMON_QUOTE_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'seqNum', '_reservedForFutureUse', 'initiator', 'mpStatusCode',
    ),
    'MEOT': (
        *COMMON_TRADE_COLUMNS,
        'eventTimestamp', 'manualFlag', 'electronicTimestamp', 'cancelFlag', 'cancelTimestamp', 'quoteKeyDate',
        'quoteID', 'quantity', 'price', 'capacity', 'tapeTradeID', 'marketCenterID', 'sideDetailsInd', 'buyDetails',
        'sellDetails', 'reportingExceptionCode', 'seqNum', 'nbbPrice', 'nbbQty', 'nboPrice', 'nboQty', 'nbboSource',
        'nbboTimestamp',
    ),
    'MEOTS': (
        *COMMON_TRADE_COLUMNS,
        'eventTimestamp', 'buyDetails', 'sellDetails',
    ),
    'MEOF': (
        *COMMON_FULFILLMENT_COLUMNS,
        'eventTimestamp', 'manualFlag', 'electronicTimestamp', 'fulfillmentLinkType', 'cancelFlag', 'cancelTimestamp',
        'quantity', 'price', 'capacity', 'clientDetails', 'firmDetails',
    ),
    'MEFA': (
        'actionType', 'errorROEID', 'firmROEID', 'type', 'CATReporterIMID', 'fillKeyDate', 'fulfillmentID',
        'priorFillKeyDate', 'priorFulfillmentID', 'symbol', 'originatingIMID', 'eventTimestamp', 'manualFlag',
        'electronicTimestamp', 'quantity', 'capacity', 'price', 'fulfillmentLinkType', 'clientDetails', 'firmDetails',
    ),
}

OPTION_EVENT_TITLES = {
    'MONO': 'New Option Event',
    'MONOS': 'Option Order Supplement',
    'MONP': 'Paired Option Order',
    'MOOR': 'Option Order Route',
    'MOMR': 'Option Route Modified',
    'MOCR': 'Option Route Cancelled',
    'MOOA': 'Option Order Accepted',
    'MOIR': 'Option Order Internal Route Accepted',
    'MOIM': 'Option Order Internal Route Modified',
    'MOIC': 'Option Order Internal Route Cancelled',
    'MOCO': 'Child Option Order',
    'MOCOM': 'Child Option Order Modified',
    'MOCOC': 'Child Option Order Cancelled',
    'MOOM': 'Option Order Modified',
    'MOOMS': 'Option Order Modified Supplement',
    'MOOJ': 'Option Order Adjusted',
    'MOOC': 'Option Order Cancelled',
    'MOOF': 'Option Order Fulfillment',
    'MOFA': 'Option Order Fulfillment Amendment',
    'MOPA': 'Option Post-Trade Allocation',
    'MOAA': 'Option Post-Trade Amended Allocation',
}
COMMON_OPTION_ORDER_COLUMNS = (
   'actionType', 'errorROEID', 'firmROEID', 'type', 'CATReporterIMID', 'orderKeyDate', 'orderID', 'optionID'
)
COMMON_OPTION_FULFILLMENT_COLUMNS = (
   'actionType', 'errorROEID', 'firmROEID', 'type', 'CATReporterIMID', 'fillKeyDate', 'fulfillmentID', 'optionID'
)
OPTION_EVENT_COLUMNS = {
    'MONO': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'eventTimestamp', 'manualFlag', 'manualOrderKeyDate', 'manualOrderID', 'electronicDupFlag',
        'electronicTimestamp', 'deptType', 'side', 'price', 'quantity', 'minQty', 'orderType', 'timeInForce',
        'tradingSession', 'handlingInstructions', 'firmDesignatedID', 'accountHolderType', 'affiliateFlag',
        'aggregatedOrders', '_reservedForFutureUse', 'openCloseIndicator', 'representativeInd', 'nextUnlinked',
    ),
    'MONOS': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'aggregatedOrders', 'priorUnlinked', 'nextUnlinked', 'firmDesignatedID',
    ),
    'MOOR': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'manualFlag', 'electronicDupFlag', 'electronicTimestamp', 'senderIMID',
        'destination', 'destinationType', 'routedOrderID', 'session', 'side', 'price', 'quantity', 'minQty',
        'orderType', 'timeInForce', 'tradingSession', 'handlingInstructions', 'routeRejectedFlag', 'exchOriginCode',
        'affiliateFlag', '_reservedForFutureUse', 'openCloseIndicator', 'priorUnlinked', 'nextUnlinked',
    ),
    'MOOA': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'eventTimestamp', 'manualOrderKeyDate', 'manualOrderID', 'manualFlag', 'electronicDupFlag',
        'electronicTimestamp', 'receiverIMID', 'senderIMID', 'senderType', 'routedOrderID', 'deptType', 'side',
        'price', 'quantity', 'minQty', 'orderType', 'timeInForce', 'tradingSession', 'handlingInstructions',
        'affiliateFlag', '_reservedForFutureUse', '_reservedForFutureUse2', 'openCloseIndicator', 'priorUnlinked',
        'nextUnlinked',
    ),
    'MOIR': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'parentOrderKeyDate', 'parentOrderID', 'originatingIMID', 'eventTimestamp', 'manualFlag',
        'electronicTimestamp', 'deptType', 'receivingDeskType', 'side', 'price', 'quantity', 'minQty',
        'orderType', 'handlingInstructions', 'openCloseIndicator', 'priorUnlinked', 'nextUnlinked', 'timeInForce',
        'tradingSession',
    ),
    'MOCO': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'parentOrderKeyDate', 'parentOrderID', 'originatingIMID', 'eventTimestamp', 'side', 'price', 'quantity',
        'minQty', 'orderType', 'timeInForce', 'tradingSession', 'handlingInstructions', 'openCloseIndicator',
        'priorUnlinked', 'nextUnlinked',
    ),
    'MOCOM': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'priorOrderKeyDate', 'priorOrderID', 'originatingIMID', 'eventTimestamp', 'side', 'price', 'quantity',
        'minQty', 'leavesQty', 'orderType', 'timeInForce', 'tradingSession', 'handlingInstructions',
        'openCloseIndicator', 'priorUnlinked', 'nextUnlinked',
    ),
    'MOCOC': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'side', 'cancelQty', 'leavesQty', '_reservedForFutureUse', 'priorUnlinked',
    ),
    'MOOM': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'priorOrderKeyDate', 'priorOrderID', 'originatingIMID', 'eventTimestamp', 'manualOrderKeyDate', 'manualOrderID',
        'manualFlag', 'electronicDupFlag', 'electronicTimestamp', 'receiverIMID', 'senderIMID', 'senderType',
        'routedOrderID', 'initiator', 'side', 'price', 'quantity', 'minQty', 'leavesQty', 'orderType', 'timeInForce',
        'tradingSession', 'handlingInstructions', 'openCloseIndicator', '_reservedForFutureUse',
        '_reservedForFutureUse2', 'aggregatedOrders', 'representativeInd', 'priorUnlinked', 'nextUnlinked',
    ),
    'MOOJ': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'priorOrderKeyDate', 'priorOrderID', 'originatingIMID', 'eventTimestamp', 'manualFlag', 'electronicTimestamp',
        'initiator', 'price', 'quantity', 'minQty', 'leavesQty', 'priorUnlinked', 'nextUnlinked',
    ),
    'MOOC': (
        *COMMON_OPTION_ORDER_COLUMNS,
        'originatingIMID', 'eventTimestamp', 'manualFlag', 'electronicTimestamp', 'cancelQty', 'leavesQty', 'initiator',
        'priorUnlinked',
    ),
    'MOOF': (
        *COMMON_OPTION_FULFILLMENT_COLUMNS,
        'eventTimestamp', 'manualFlag', 'electronicTimestamp', 'quantity', 'price', 'fulfillmentLinkType',
        'clientDetails', 'firmDetails', 'priorUnlinked', 'cancelFlag', 'cancelTimestamp',
    ),
    'MOFA': (
        *COMMON_OPTION_FULFILLMENT_COLUMNS,
        'priorFillKeyDate', 'priorFulfillmentID', 'originatingIMID', 'eventTimestamp', 'manualFlag',
        'electronicTimestamp', 'fulfillmentLinkType', 'quantity', 'price', 'clientDetails', 'firmDetails',
        'priorUnlinked',
    ),
}

ALL_EVENT_TITLES = {
    **EQUITY_EVENT_TITLES,
    **OPTION_EVENT_TITLES,
}
ALL_EVENT_COLUMNS = {
    **EQUITY_EVENT_COLUMNS,
    **OPTION_EVENT_COLUMNS,
}
