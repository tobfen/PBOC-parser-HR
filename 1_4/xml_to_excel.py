import json
import os
import warnings
import uuid

import numpy as np
import pandas as pd
import xmltodict

import xml_function as xf

warnings.filterwarnings('ignore')

status_col_5year = {"SID",
"debit_credit_account_l5y_month1",
"debit_credit_account_l5y_month2",
"debit_credit_account_l5y_month3",
"debit_credit_account_l5y_month4",
"debit_credit_account_l5y_month5",
"debit_credit_account_l5y_month6",
"debit_credit_account_l5y_month7",
"debit_credit_account_l5y_month8",
"debit_credit_account_l5y_month9",
"debit_credit_account_l5y_month10",
"debit_credit_account_l5y_month11",
"debit_credit_account_l5y_month12",
"debit_credit_account_l5y_month13",
"debit_credit_account_l5y_month14",
"debit_credit_account_l5y_month15",
"debit_credit_account_l5y_month16",
"debit_credit_account_l5y_month17",
"debit_credit_account_l5y_month18",
"debit_credit_account_l5y_month19",
"debit_credit_account_l5y_month20",
"debit_credit_account_l5y_month21",
"debit_credit_account_l5y_month22",
"debit_credit_account_l5y_month23",
"debit_credit_account_l5y_month24",
"debit_credit_account_l5y_month25",
"debit_credit_account_l5y_month26",
"debit_credit_account_l5y_month27",
"debit_credit_account_l5y_month28",
"debit_credit_account_l5y_month29",
"debit_credit_account_l5y_month30",
"debit_credit_account_l5y_month31",
"debit_credit_account_l5y_month32",
"debit_credit_account_l5y_month33",
"debit_credit_account_l5y_month34",
"debit_credit_account_l5y_month35",
"debit_credit_account_l5y_month36",
"debit_credit_account_l5y_month37",
"debit_credit_account_l5y_month38",
"debit_credit_account_l5y_month39",
"debit_credit_account_l5y_month40",
"debit_credit_account_l5y_month41",
"debit_credit_account_l5y_month42",
"debit_credit_account_l5y_month43",
"debit_credit_account_l5y_month44",
"debit_credit_account_l5y_month45",
"debit_credit_account_l5y_month46",
"debit_credit_account_l5y_month47",
"debit_credit_account_l5y_month48",
"debit_credit_account_l5y_month49",
"debit_credit_account_l5y_month50",
"debit_credit_account_l5y_month51",
"debit_credit_account_l5y_month52",
"debit_credit_account_l5y_month53",
"debit_credit_account_l5y_month54",
"debit_credit_account_l5y_month55",
"debit_credit_account_l5y_month56",
"debit_credit_account_l5y_month57",
"debit_credit_account_l5y_month58",
"debit_credit_account_l5y_month59",
"debit_credit_account_l5y_month60",
"debit_credit_account_l5y_repay_status1",
"debit_credit_account_l5y_repay_status2",
"debit_credit_account_l5y_repay_status3",
"debit_credit_account_l5y_repay_status4",
"debit_credit_account_l5y_repay_status5",
"debit_credit_account_l5y_repay_status6",
"debit_credit_account_l5y_repay_status7",
"debit_credit_account_l5y_repay_status8",
"debit_credit_account_l5y_repay_status9",
"debit_credit_account_l5y_repay_status10",
"debit_credit_account_l5y_repay_status11",
"debit_credit_account_l5y_repay_status12",
"debit_credit_account_l5y_repay_status13",
"debit_credit_account_l5y_repay_status14",
"debit_credit_account_l5y_repay_status15",
"debit_credit_account_l5y_repay_status16",
"debit_credit_account_l5y_repay_status17",
"debit_credit_account_l5y_repay_status18",
"debit_credit_account_l5y_repay_status19",
"debit_credit_account_l5y_repay_status20",
"debit_credit_account_l5y_repay_status21",
"debit_credit_account_l5y_repay_status22",
"debit_credit_account_l5y_repay_status23",
"debit_credit_account_l5y_repay_status24",
"debit_credit_account_l5y_repay_status25",
"debit_credit_account_l5y_repay_status26",
"debit_credit_account_l5y_repay_status27",
"debit_credit_account_l5y_repay_status28",
"debit_credit_account_l5y_repay_status29",
"debit_credit_account_l5y_repay_status30",
"debit_credit_account_l5y_repay_status31",
"debit_credit_account_l5y_repay_status32",
"debit_credit_account_l5y_repay_status33",
"debit_credit_account_l5y_repay_status34",
"debit_credit_account_l5y_repay_status35",
"debit_credit_account_l5y_repay_status36",
"debit_credit_account_l5y_repay_status37",
"debit_credit_account_l5y_repay_status38",
"debit_credit_account_l5y_repay_status39",
"debit_credit_account_l5y_repay_status40",
"debit_credit_account_l5y_repay_status41",
"debit_credit_account_l5y_repay_status42",
"debit_credit_account_l5y_repay_status43",
"debit_credit_account_l5y_repay_status44",
"debit_credit_account_l5y_repay_status45",
"debit_credit_account_l5y_repay_status46",
"debit_credit_account_l5y_repay_status47",
"debit_credit_account_l5y_repay_status48",
"debit_credit_account_l5y_repay_status49",
"debit_credit_account_l5y_repay_status50",
"debit_credit_account_l5y_repay_status51",
"debit_credit_account_l5y_repay_status52",
"debit_credit_account_l5y_repay_status53",
"debit_credit_account_l5y_repay_status54",
"debit_credit_account_l5y_repay_status55",
"debit_credit_account_l5y_repay_status56",
"debit_credit_account_l5y_repay_status57",
"debit_credit_account_l5y_repay_status58",
"debit_credit_account_l5y_repay_status59",
"debit_credit_account_l5y_repay_status60",
}

overdue_amt_col_5year = {"SID",
"debit_credit_account_l5y_month1",
"debit_credit_account_l5y_month2",
"debit_credit_account_l5y_month3",
"debit_credit_account_l5y_month4",
"debit_credit_account_l5y_month5",
"debit_credit_account_l5y_month6",
"debit_credit_account_l5y_month7",
"debit_credit_account_l5y_month8",
"debit_credit_account_l5y_month9",
"debit_credit_account_l5y_month10",
"debit_credit_account_l5y_month11",
"debit_credit_account_l5y_month12",
"debit_credit_account_l5y_month13",
"debit_credit_account_l5y_month14",
"debit_credit_account_l5y_month15",
"debit_credit_account_l5y_month16",
"debit_credit_account_l5y_month17",
"debit_credit_account_l5y_month18",
"debit_credit_account_l5y_month19",
"debit_credit_account_l5y_month20",
"debit_credit_account_l5y_month21",
"debit_credit_account_l5y_month22",
"debit_credit_account_l5y_month23",
"debit_credit_account_l5y_month24",
"debit_credit_account_l5y_month25",
"debit_credit_account_l5y_month26",
"debit_credit_account_l5y_month27",
"debit_credit_account_l5y_month28",
"debit_credit_account_l5y_month29",
"debit_credit_account_l5y_month30",
"debit_credit_account_l5y_month31",
"debit_credit_account_l5y_month32",
"debit_credit_account_l5y_month33",
"debit_credit_account_l5y_month34",
"debit_credit_account_l5y_month35",
"debit_credit_account_l5y_month36",
"debit_credit_account_l5y_month37",
"debit_credit_account_l5y_month38",
"debit_credit_account_l5y_month39",
"debit_credit_account_l5y_month40",
"debit_credit_account_l5y_month41",
"debit_credit_account_l5y_month42",
"debit_credit_account_l5y_month43",
"debit_credit_account_l5y_month44",
"debit_credit_account_l5y_month45",
"debit_credit_account_l5y_month46",
"debit_credit_account_l5y_month47",
"debit_credit_account_l5y_month48",
"debit_credit_account_l5y_month49",
"debit_credit_account_l5y_month50",
"debit_credit_account_l5y_month51",
"debit_credit_account_l5y_month52",
"debit_credit_account_l5y_month53",
"debit_credit_account_l5y_month54",
"debit_credit_account_l5y_month55",
"debit_credit_account_l5y_month56",
"debit_credit_account_l5y_month57",
"debit_credit_account_l5y_month58",
"debit_credit_account_l5y_month59",
"debit_credit_account_l5y_month60",
"debit_credit_account_l5y_overdue_amt1",
"debit_credit_account_l5y_overdue_amt2",
"debit_credit_account_l5y_overdue_amt3",
"debit_credit_account_l5y_overdue_amt4",
"debit_credit_account_l5y_overdue_amt5",
"debit_credit_account_l5y_overdue_amt6",
"debit_credit_account_l5y_overdue_amt7",
"debit_credit_account_l5y_overdue_amt8",
"debit_credit_account_l5y_overdue_amt9",
"debit_credit_account_l5y_overdue_amt10",
"debit_credit_account_l5y_overdue_amt11",
"debit_credit_account_l5y_overdue_amt12",
"debit_credit_account_l5y_overdue_amt13",
"debit_credit_account_l5y_overdue_amt14",
"debit_credit_account_l5y_overdue_amt15",
"debit_credit_account_l5y_overdue_amt16",
"debit_credit_account_l5y_overdue_amt17",
"debit_credit_account_l5y_overdue_amt18",
"debit_credit_account_l5y_overdue_amt19",
"debit_credit_account_l5y_overdue_amt20",
"debit_credit_account_l5y_overdue_amt21",
"debit_credit_account_l5y_overdue_amt22",
"debit_credit_account_l5y_overdue_amt23",
"debit_credit_account_l5y_overdue_amt24",
"debit_credit_account_l5y_overdue_amt25",
"debit_credit_account_l5y_overdue_amt26",
"debit_credit_account_l5y_overdue_amt27",
"debit_credit_account_l5y_overdue_amt28",
"debit_credit_account_l5y_overdue_amt29",
"debit_credit_account_l5y_overdue_amt30",
"debit_credit_account_l5y_overdue_amt31",
"debit_credit_account_l5y_overdue_amt32",
"debit_credit_account_l5y_overdue_amt33",
"debit_credit_account_l5y_overdue_amt34",
"debit_credit_account_l5y_overdue_amt35",
"debit_credit_account_l5y_overdue_amt36",
"debit_credit_account_l5y_overdue_amt37",
"debit_credit_account_l5y_overdue_amt38",
"debit_credit_account_l5y_overdue_amt39",
"debit_credit_account_l5y_overdue_amt40",
"debit_credit_account_l5y_overdue_amt41",
"debit_credit_account_l5y_overdue_amt42",
"debit_credit_account_l5y_overdue_amt43",
"debit_credit_account_l5y_overdue_amt44",
"debit_credit_account_l5y_overdue_amt45",
"debit_credit_account_l5y_overdue_amt46",
"debit_credit_account_l5y_overdue_amt47",
"debit_credit_account_l5y_overdue_amt48",
"debit_credit_account_l5y_overdue_amt49",
"debit_credit_account_l5y_overdue_amt50",
"debit_credit_account_l5y_overdue_amt51",
"debit_credit_account_l5y_overdue_amt52",
"debit_credit_account_l5y_overdue_amt53",
"debit_credit_account_l5y_overdue_amt54",
"debit_credit_account_l5y_overdue_amt55",
"debit_credit_account_l5y_overdue_amt56",
"debit_credit_account_l5y_overdue_amt57",
"debit_credit_account_l5y_overdue_amt58",
"debit_credit_account_l5y_overdue_amt59",
"debit_credit_account_l5y_overdue_amt60",
}

rep_status_dic_col = {"debit_credit_account_l5y_month1":"debit_credit_account_l5y_repay_status1",
"debit_credit_account_l5y_month2":"debit_credit_account_l5y_repay_status2",
"debit_credit_account_l5y_month3":"debit_credit_account_l5y_repay_status3",
"debit_credit_account_l5y_month4":"debit_credit_account_l5y_repay_status4",
"debit_credit_account_l5y_month5":"debit_credit_account_l5y_repay_status5",
"debit_credit_account_l5y_month6":"debit_credit_account_l5y_repay_status6",
"debit_credit_account_l5y_month7":"debit_credit_account_l5y_repay_status7",
"debit_credit_account_l5y_month8":"debit_credit_account_l5y_repay_status8",
"debit_credit_account_l5y_month9":"debit_credit_account_l5y_repay_status9",
"debit_credit_account_l5y_month10":"debit_credit_account_l5y_repay_status10",
"debit_credit_account_l5y_month11":"debit_credit_account_l5y_repay_status11",
"debit_credit_account_l5y_month12":"debit_credit_account_l5y_repay_status12",
"debit_credit_account_l5y_month13":"debit_credit_account_l5y_repay_status13",
"debit_credit_account_l5y_month14":"debit_credit_account_l5y_repay_status14",
"debit_credit_account_l5y_month15":"debit_credit_account_l5y_repay_status15",
"debit_credit_account_l5y_month16":"debit_credit_account_l5y_repay_status16",
"debit_credit_account_l5y_month17":"debit_credit_account_l5y_repay_status17",
"debit_credit_account_l5y_month18":"debit_credit_account_l5y_repay_status18",
"debit_credit_account_l5y_month19":"debit_credit_account_l5y_repay_status19",
"debit_credit_account_l5y_month20":"debit_credit_account_l5y_repay_status20",
"debit_credit_account_l5y_month21":"debit_credit_account_l5y_repay_status21",
"debit_credit_account_l5y_month22":"debit_credit_account_l5y_repay_status22",
"debit_credit_account_l5y_month23":"debit_credit_account_l5y_repay_status23",
"debit_credit_account_l5y_month24":"debit_credit_account_l5y_repay_status24",
"debit_credit_account_l5y_month25":"debit_credit_account_l5y_repay_status25",
"debit_credit_account_l5y_month26":"debit_credit_account_l5y_repay_status26",
"debit_credit_account_l5y_month27":"debit_credit_account_l5y_repay_status27",
"debit_credit_account_l5y_month28":"debit_credit_account_l5y_repay_status28",
"debit_credit_account_l5y_month29":"debit_credit_account_l5y_repay_status29",
"debit_credit_account_l5y_month30":"debit_credit_account_l5y_repay_status30",
"debit_credit_account_l5y_month31":"debit_credit_account_l5y_repay_status31",
"debit_credit_account_l5y_month32":"debit_credit_account_l5y_repay_status32",
"debit_credit_account_l5y_month33":"debit_credit_account_l5y_repay_status33",
"debit_credit_account_l5y_month34":"debit_credit_account_l5y_repay_status34",
"debit_credit_account_l5y_month35":"debit_credit_account_l5y_repay_status35",
"debit_credit_account_l5y_month36":"debit_credit_account_l5y_repay_status36",
"debit_credit_account_l5y_month37":"debit_credit_account_l5y_repay_status37",
"debit_credit_account_l5y_month38":"debit_credit_account_l5y_repay_status38",
"debit_credit_account_l5y_month39":"debit_credit_account_l5y_repay_status39",
"debit_credit_account_l5y_month40":"debit_credit_account_l5y_repay_status40",
"debit_credit_account_l5y_month41":"debit_credit_account_l5y_repay_status41",
"debit_credit_account_l5y_month42":"debit_credit_account_l5y_repay_status42",
"debit_credit_account_l5y_month43":"debit_credit_account_l5y_repay_status43",
"debit_credit_account_l5y_month44":"debit_credit_account_l5y_repay_status44",
"debit_credit_account_l5y_month45":"debit_credit_account_l5y_repay_status45",
"debit_credit_account_l5y_month46":"debit_credit_account_l5y_repay_status46",
"debit_credit_account_l5y_month47":"debit_credit_account_l5y_repay_status47",
"debit_credit_account_l5y_month48":"debit_credit_account_l5y_repay_status48",
"debit_credit_account_l5y_month49":"debit_credit_account_l5y_repay_status49",
"debit_credit_account_l5y_month50":"debit_credit_account_l5y_repay_status50",
"debit_credit_account_l5y_month51":"debit_credit_account_l5y_repay_status51",
"debit_credit_account_l5y_month52":"debit_credit_account_l5y_repay_status52",
"debit_credit_account_l5y_month53":"debit_credit_account_l5y_repay_status53",
"debit_credit_account_l5y_month54":"debit_credit_account_l5y_repay_status54",
"debit_credit_account_l5y_month55":"debit_credit_account_l5y_repay_status55",
"debit_credit_account_l5y_month56":"debit_credit_account_l5y_repay_status56",
"debit_credit_account_l5y_month57":"debit_credit_account_l5y_repay_status57",
"debit_credit_account_l5y_month58":"debit_credit_account_l5y_repay_status58",
"debit_credit_account_l5y_month59":"debit_credit_account_l5y_repay_status59",
"debit_credit_account_l5y_month60":"debit_credit_account_l5y_repay_status60",}

overdue_amt_dic_col={
"debit_credit_account_l5y_month1":"debit_credit_account_l5y_overdue_amt1",
"debit_credit_account_l5y_month2":"debit_credit_account_l5y_overdue_amt2",
"debit_credit_account_l5y_month3":"debit_credit_account_l5y_overdue_amt3",
"debit_credit_account_l5y_month4":"debit_credit_account_l5y_overdue_amt4",
"debit_credit_account_l5y_month5":"debit_credit_account_l5y_overdue_amt5",
"debit_credit_account_l5y_month6":"debit_credit_account_l5y_overdue_amt6",
"debit_credit_account_l5y_month7":"debit_credit_account_l5y_overdue_amt7",
"debit_credit_account_l5y_month8":"debit_credit_account_l5y_overdue_amt8",
"debit_credit_account_l5y_month9":"debit_credit_account_l5y_overdue_amt9",
"debit_credit_account_l5y_month10":"debit_credit_account_l5y_overdue_amt10",
"debit_credit_account_l5y_month11":"debit_credit_account_l5y_overdue_amt11",
"debit_credit_account_l5y_month12":"debit_credit_account_l5y_overdue_amt12",
"debit_credit_account_l5y_month13":"debit_credit_account_l5y_overdue_amt13",
"debit_credit_account_l5y_month14":"debit_credit_account_l5y_overdue_amt14",
"debit_credit_account_l5y_month15":"debit_credit_account_l5y_overdue_amt15",
"debit_credit_account_l5y_month16":"debit_credit_account_l5y_overdue_amt16",
"debit_credit_account_l5y_month17":"debit_credit_account_l5y_overdue_amt17",
"debit_credit_account_l5y_month18":"debit_credit_account_l5y_overdue_amt18",
"debit_credit_account_l5y_month19":"debit_credit_account_l5y_overdue_amt19",
"debit_credit_account_l5y_month20":"debit_credit_account_l5y_overdue_amt20",
"debit_credit_account_l5y_month21":"debit_credit_account_l5y_overdue_amt21",
"debit_credit_account_l5y_month22":"debit_credit_account_l5y_overdue_amt22",
"debit_credit_account_l5y_month23":"debit_credit_account_l5y_overdue_amt23",
"debit_credit_account_l5y_month24":"debit_credit_account_l5y_overdue_amt24",
"debit_credit_account_l5y_month25":"debit_credit_account_l5y_overdue_amt25",
"debit_credit_account_l5y_month26":"debit_credit_account_l5y_overdue_amt26",
"debit_credit_account_l5y_month27":"debit_credit_account_l5y_overdue_amt27",
"debit_credit_account_l5y_month28":"debit_credit_account_l5y_overdue_amt28",
"debit_credit_account_l5y_month29":"debit_credit_account_l5y_overdue_amt29",
"debit_credit_account_l5y_month30":"debit_credit_account_l5y_overdue_amt30",
"debit_credit_account_l5y_month31":"debit_credit_account_l5y_overdue_amt31",
"debit_credit_account_l5y_month32":"debit_credit_account_l5y_overdue_amt32",
"debit_credit_account_l5y_month33":"debit_credit_account_l5y_overdue_amt33",
"debit_credit_account_l5y_month34":"debit_credit_account_l5y_overdue_amt34",
"debit_credit_account_l5y_month35":"debit_credit_account_l5y_overdue_amt35",
"debit_credit_account_l5y_month36":"debit_credit_account_l5y_overdue_amt36",
"debit_credit_account_l5y_month37":"debit_credit_account_l5y_overdue_amt37",
"debit_credit_account_l5y_month38":"debit_credit_account_l5y_overdue_amt38",
"debit_credit_account_l5y_month39":"debit_credit_account_l5y_overdue_amt39",
"debit_credit_account_l5y_month40":"debit_credit_account_l5y_overdue_amt40",
"debit_credit_account_l5y_month41":"debit_credit_account_l5y_overdue_amt41",
"debit_credit_account_l5y_month42":"debit_credit_account_l5y_overdue_amt42",
"debit_credit_account_l5y_month43":"debit_credit_account_l5y_overdue_amt43",
"debit_credit_account_l5y_month44":"debit_credit_account_l5y_overdue_amt44",
"debit_credit_account_l5y_month45":"debit_credit_account_l5y_overdue_amt45",
"debit_credit_account_l5y_month46":"debit_credit_account_l5y_overdue_amt46",
"debit_credit_account_l5y_month47":"debit_credit_account_l5y_overdue_amt47",
"debit_credit_account_l5y_month48":"debit_credit_account_l5y_overdue_amt48",
"debit_credit_account_l5y_month49":"debit_credit_account_l5y_overdue_amt49",
"debit_credit_account_l5y_month50":"debit_credit_account_l5y_overdue_amt50",
"debit_credit_account_l5y_month51":"debit_credit_account_l5y_overdue_amt51",
"debit_credit_account_l5y_month52":"debit_credit_account_l5y_overdue_amt52",
"debit_credit_account_l5y_month53":"debit_credit_account_l5y_overdue_amt53",
"debit_credit_account_l5y_month54":"debit_credit_account_l5y_overdue_amt54",
"debit_credit_account_l5y_month55":"debit_credit_account_l5y_overdue_amt55",
"debit_credit_account_l5y_month56":"debit_credit_account_l5y_overdue_amt56",
"debit_credit_account_l5y_month57":"debit_credit_account_l5y_overdue_amt57",
"debit_credit_account_l5y_month58":"debit_credit_account_l5y_overdue_amt58",
"debit_credit_account_l5y_month59":"debit_credit_account_l5y_overdue_amt59",
"debit_credit_account_l5y_month60":"debit_credit_account_l5y_overdue_amt60",
}

noncycle_col = ["info_summary_noncycle_manage_org_count","info_summary_noncycle_account_count","info_summary_noncycle_credit_amt_sum",
 "info_summary_noncycle_balance","info_summary_noncycle_l6m_avg_repayable"]
revolving_col = ["info_summary_revolving_manage_org_count","info_summary_revolving_account_count","info_summary_revolving_credit_amt_sum",
 "info_summary_revolving_balance","info_summary_revolving_l6m_avg_repayable"]
cycle_col = ["info_summary_cycle_manage_org_count","info_summary_cycle_account_count","info_summary_cycle_credit_amt_sum",
 "info_summary_cycle_balance","info_summary_cycle_l6m_avg_repayable"]
cc_col = [ "info_summary_cc_issuer_count","info_summary_cc_account_count","info_summary_cc_credit_amt_sum","info_summary_cc_single_max_credit_amt",
 "info_summary_cc_single_min_credit_amt","info_summary_cc_used_amt","info_summary_cc_l6m_avg_used_amt",]
qcc_col = [
 "info_summary_qcc_issuer_count","info_summary_qcc_account_count","info_summary_qcc_credit_amt_sum",
 "info_summary_qcc_single_max_credit_amt","info_summary_qcc_single_min_credit_amt","info_summary_qcc_overdraw_balance",
 "info_summary_qcc_l6m_avg_overdraw_bal"]
five_col = [noncycle_col,revolving_col,cycle_col]
seven_col = [cc_col,qcc_col]

creditTransactionExtra_col = {
"SID":"SID",
"CreditType":"CreditType",
"debit_credit_account_monpf_month":"Record1Description",
"debit_credit_account_monpf_account_status":"AccountState",
"debit_credit_account_monpf_five_level":"FiveLoanGradesOfRecord1",
"debit_credit_account_monpf_balance":"Record1Balance",
"debit_credit_account_monpf_remaining_repay_period":"RemainingTenor",
"debit_credit_account_monpf_repayable_amt":"PayableAmountOfThisMonth",
"debit_credit_account_monpf_repay_date":"DueDate",
"debit_credit_account_monpf_actually_repaid_amt":"PaymentAmountOfThisMonth",
"debit_credit_account_monpf_last_repay_date":"LastPaymentDate",
"debit_credit_account_monpf_used_amt":"UsedAmount",
"debit_credit_account_monpf_unissued_large_stage_bal":"SpecialInstalmentBalanceOfLargeUnbilled",
"debit_credit_account_monpf_current_overdue_periods":"CurrentDelinquencyTerm",
"debit_credit_account_monpf_l6m_avg_used_amt":"AverageUtilizationInLast6Month",
"debit_credit_account_monpf_max_use_amt":"MaxUtilization",
# "debit_credit_account_monpf_last_repay_date":"BillDate",
"debit_credit_account_monpf_current_overdue_sum":"CurrentArrearAmount",
"debit_credit_account_monpf_overdue_31_60_debit":"OverduePrincipal31To60Days",
"debit_credit_account_monpf_overdue_61_90_debit":"OverduePrincipal61To90Days",
"debit_credit_account_monpf_overdue_91_180_debit":"OverduePrincipal91To180Days",
"debit_credit_account_monpf_overdue_over_180_debit":"OverduePrincipalMoreThan180Days",
"debit_credit_account_latest_close_date":"AccountClosingDate",
"debit_credit_account_latest_transfer_out_month":"TransferringMonth",
"debit_credit_account_latest_five_level":"FiveLoanGradesOfRecord2",
"debit_credit_account_latest_balance":"Record2Balance",
"debit_credit_account_latest_repay_date":"Record2RepaymentDate",
"debit_credit_account_latest_repay_amt":"Record2RepaymentAmount",
"debit_credit_account_latest_repay_status":"Record2CurrentRepaymentState",
"debit_credit_account_monpf_overdraw_over_180_debit":"UnpaidAmountOfOverdueForMoreThan180days",
"debit_credit_account_latest_account_status":"AccountStateRecord2"}

def summary_Acc_Info(infoSummary_df):
    scai = infoSummary_df
    five_col_data = pd.DataFrame()

    for i in range(len(five_col)):
        df_tmp = scai[five_col[i]]
        df_tmp.columns = ['CountOfInstitutions','CountOfAccount','CreditTotalAmount','OutstandingBalance','AverageInstallmentOfRecent6Months']
        df_tmp.loc[:,'AccountType'] = i+1
        df_tmp.loc[:,'MaxCreditAmountOfSingleBank'] = np.nan
        df_tmp.loc[:,'MinCreditAmountOfSingleBank'] = np.nan
        df_tmp.loc[:,'OverdraftAmount'] = np.nan
        df_tmp.loc[:,'AverageOverdraftAmountInLast6Month'] = np.nan
        five_col_data = pd.concat([five_col_data,df_tmp],axis=0)
        
    seven_col_data = pd.DataFrame()

    for i in range(len(seven_col)):
        df_tmp = scai[seven_col[i]]
        df_tmp.columns = ['CountOfInstitutions','CountOfAccount','CreditTotalAmount','MaxCreditAmountOfSingleBank','MinCreditAmountOfSingleBank','OverdraftAmount','AverageOverdraftAmountInLast6Month']
        df_tmp.loc[:,'AccountType'] = i+4
        seven_col_data = pd.concat([seven_col_data,df_tmp],axis=0)
        
    summary_acc_info = pd.concat([five_col_data,seven_col_data],axis=0)
    return summary_acc_info

def CreditPaymentRecord(debitCreditAccount_df):
    info_5year_all = debitCreditAccount_df
    info_5year = info_5year_all[status_col_5year]
    repay_status = pd.DataFrame()
    for i in rep_status_dic_col:
        tmp1 = pd.DataFrame()
        tmp1 = info_5year[['SID',i,rep_status_dic_col[i]]]
        tmp1.columns = ['SID','yearMonth','value']
        repay_status = pd.concat([repay_status,tmp1],axis=0)
    repay_status['RepaymentYear'] = repay_status['yearMonth'].str.split('-',1).str[0]
    repay_status['RepaymentMonth'] = repay_status['yearMonth'].str.split('-',1).str[1]
    del repay_status['yearMonth']
    repay_status_notna = repay_status[~(repay_status.RepaymentYear.isna() & repay_status.RepaymentMonth.isna())].pivot(index=['SID','RepaymentYear'],columns='RepaymentMonth',values='value').reset_index()

    expected_original_cols = [f"{i:02d}" for i in range(1, 13)]
    # 添加缺失的原始列（自动填充NaN）
    for col in expected_original_cols:
        if col not in repay_status_notna:
            repay_status_notna[col] = np.nan

    repay_status_notna.columns.name = None
    repay_status_notna.rename(columns={'01':'Month1','02':'Month2','03':'Month3','04':'Month4','05':'Month5',
                       '06':'Month6','07':'Month7','08':'Month8','09':'Month9','10':'Month10',
                       '11':'Month11','12':'Month12'},inplace=True)
    repay_status_notna['PaymentRecordType'] = 1
    
    info_5year = info_5year_all[overdue_amt_col_5year]
    overdue_amt = pd.DataFrame()
    for i in overdue_amt_dic_col:
        tmp1 = pd.DataFrame()
        tmp1 = info_5year[['SID',i,overdue_amt_dic_col[i]]]
        tmp1.columns = ['SID','yearMonth','value']
        overdue_amt = pd.concat([overdue_amt,tmp1],axis=0)
    overdue_amt['RepaymentYear'] = overdue_amt['yearMonth'].str.split('-',1).str[0]
    overdue_amt['RepaymentMonth'] = overdue_amt['yearMonth'].str.split('-',1).str[1]
    
    del overdue_amt['yearMonth']
    overdue_amt_notna = overdue_amt[~(overdue_amt.RepaymentYear.isna() & overdue_amt.RepaymentMonth.isna())].pivot(index=['SID','RepaymentYear'],columns='RepaymentMonth',values='value').reset_index()

    # 添加缺失的原始列（自动填充NaN）
    for col in expected_original_cols:
        if col not in overdue_amt_notna:
            overdue_amt_notna[col] = np.nan

    overdue_amt_notna.columns.name = None
    overdue_amt_notna.rename(columns={'01':'Month1','02':'Month2','03':'Month3','04':'Month4','05':'Month5',
                       '06':'Month6','07':'Month7','08':'Month8','09':'Month9','10':'Month10',
                       '11':'Month11','12':'Month12'},inplace=True)
    overdue_amt_notna['PaymentRecordType'] = 2
    
    creditPaymentRecord = pd.concat([repay_status_notna,overdue_amt_notna],axis=0)
    if creditPaymentRecord.empty:
        # 获取所有可能的列名（合并两个源的列名）
        combined_columns = repay_status_notna.columns.union(overdue_amt_notna.columns)

        # 创建带有完整列结构的空DataFrame
        empty_template = pd.DataFrame(columns=combined_columns)

        # 添加一行全NaN数据
        creditPaymentRecord = empty_template.append(
            {col: None for col in combined_columns},
            ignore_index=True
        )
    creditPaymentRecord.rename(columns={"SID":"PSID"},inplace=True)

    return creditPaymentRecord

def xml_to_json(path,file_name):
    """以下为函数说明
    函数功能：将xml报文转为json格式并保存至当前路径下以该报文名称命名的文件夹中
    Arguments:
        path (str): xml报文所在文件夹.
        file_name (str): xml报文名称，不含文件格式.
    """
    os.chdir(path)
     
    #定义函数
    
    def pythonXmlToJson(path):
        with  open(path,'r',encoding='utf-8') as f:
            xmlStr = f.read()
     
        convertedDict = xmltodict.parse(xmlStr.replace(',',''));
        jsonStr = json.dumps(convertedDict, indent=1);
        return jsonStr;
    #执行函数
    
    json_str = pythonXmlToJson(file_name)    
    
    fileNames = open('sample.txt','w')
    fileNames.write(json_str)
    fileNames.close()
    
def add_key_and_save2csv(df,key,csv_name,mode,header):
    df1 = df.copy()
    try:
        df1.loc[:,'PCRID'] = key
        df1.to_csv(csv_name,index=False,mode=mode,header=header)  
    except:
        pass

def json_to_df(path,file_name,write_mode,header,column_type='ENG'):
    """以下为函数说明
    函数功能：将已转换为json格式的xml报文转化为数据表并存储
    Arguments:
        path (str): json文件所在目录，输出xlsx文件保存目录.
        file_name (str): json文件名称，不含文件格式.
    keyword Arguments:
        column_type (str): 返回数据表中column名称格式（'CNH'为中文，'ENG'为英文）Default：'CNH'
    """
    os.chdir(path)
    f = open(file_name, 'r',encoding="utf-8")
    temp1 = json.load(f)
    
    creditTransaction_col = ["CreditType","AccountNumber","ManagementInstituion","ManageOrgCode","AccountIdentity","CreditLine","ShareCreditLine","BusinessType","LoanIssuingDate","Currency",
                          "LoanAmount","MaturityDate","RepaymentMethod","RepaymentPeriod","Tenor","GuarantorType","CoBorrowingFlag","RepaymentStateWhenTransferingClaim",]
    
    summaryQueryInformation_col = ["LastQueryRecordDate","LastQueryRecordAgency","LastQueryRecordReason","CountOfCreditApprovalQueryInstitutionInLastMonth",                                       "CountOfCreditCardApprovalQueryInstitutionInLastMonth","QueryTimesOfCreditApprovalInLastMonth","QueryTimesOfCreditCardApprovalInLastMonth",
                                       "SelfQueryTimesInLastMonth","QueryTimesOfPostloanManagementInLastTwoMonth","QueryTimesOfGuaranteeQualificationAssessment",
                                       "QueryTimesOfMerchantsRealnameReview",]
    ### 主键
    pcrid,report_id,report_time,xm,zj_type = xf.pri_key(temp1)
        
    ###报告头模块
    header_dataf = xf.header_df(temp1,column_type = column_type)
    reportheaderAntiFraudWarning = ["WarningInformation","EffecgtiveDate","ExpirationDate","ReportHeaderWarningTel"]
    add_key_and_save2csv(header_dataf[reportheaderAntiFraudWarning],key=pcrid,csv_name='PCR2_ReportheaderAntiFraudWarning.csv',mode=write_mode,header=header)
    reportHeaderInfo = ["ReportNumber","ReportTime","CutomerName","CustomerIDType","CutomerIDNumber","QueryOrganization","QueryReason","DissentInformation",]
    add_key_and_save2csv(header_dataf[reportHeaderInfo],key=pcrid,csv_name='PCR2_ReportHeaderInformation.csv',mode=write_mode,header=header)
    
    ###基本信息段
    basicInfo_df = xf.basicInfo_df(temp1,column_type = column_type)
    basicInfo_df.loc[:,'IdentifyType'] = zj_type
    basicInfo_df.loc[:,'IdentifyNumber'] = pcrid
    basicInfo_df.loc[:,'CustomerName'] = xm
    basicInfo_df.loc[:,'QueryRecordId'] = report_id
    basicInfo_df.loc[:,'CreateTime'] = report_time
    add_key_and_save2csv(basicInfo_df,key=pcrid,csv_name='PCR2_IdentifiableInformation.csv',mode=write_mode,header=header)
    
    ###手机模块
    biMobile_df = xf.biMobile_df(temp1,column_type = column_type)
    add_key_and_save2csv(biMobile_df,key=pcrid,csv_name='PCR2_PhoneInformation.csv',mode=write_mode,header=header)
    
    ###居住情况
    biHouse_df = xf.biHouse_df(temp1,column_type = column_type)
    add_key_and_save2csv(biHouse_df,key=pcrid,csv_name='PCR2_LivingInformation.csv',mode=write_mode,header=header)
    
    ###工作模块
    biJob_df = xf.biJob_df(temp1,column_type = column_type)
    add_key_and_save2csv(biJob_df,key=pcrid,csv_name='PCR2_CareeInformation.csv',mode=write_mode,header=header)
    
    ###证件模块
    rhId_df = xf.rhId(temp1,column_type = column_type)
    add_key_and_save2csv(rhId_df,key=pcrid,csv_name='PCR2_ReportHeaderOtherID.csv',mode=write_mode,header=header)
    
    ###信息概要信息段
    infoSummary_df = xf.infoSummary_df(temp1,column_type = column_type)
    add_key_and_save2csv(infoSummary_df[['CountOfAccount','Balance']],key=pcrid,csv_name='PCR2_SummaryBadDebts.csv',mode=write_mode,header=header) #呆账信息汇总
    add_key_and_save2csv(infoSummary_df[['DigitalInterpretation','RelativePosition']],key=pcrid,csv_name='PCR2_SummaryDigitalInterpretation.csv',mode=write_mode,header=header) #个人信用报告数字解读

    add_key_and_save2csv(infoSummary_df[summaryQueryInformation_col],key=pcrid,csv_name='PCR2_SummaryQueryInformation.csv',mode=write_mode,header=header) #查询记录概要
    add_key_and_save2csv(infoSummary_df,key=pcrid,csv_name='信息概要.csv',mode=write_mode,header=header)
    summary_Acc_Info_df = summary_Acc_Info(infoSummary_df)
    add_key_and_save2csv(summary_Acc_Info_df,key=pcrid,csv_name='PCR2_SummaryCreditAcountInformation.csv',mode=write_mode,header=header)
    
    
    
    
    ###信贷交易提示信息段
    isCreditTransInfo_df = xf.isCreditTransInfo_df(temp1,column_type = column_type)
    add_key_and_save2csv(isCreditTransInfo_df,key=pcrid,csv_name='PCR2_SummaryCreditTips.csv',mode=write_mode,header=header)
    
    ###被追偿汇总信息
    isRecoveredSum_df = xf.isRecoveredSum_df(temp1,column_type = column_type)
    add_key_and_save2csv(isRecoveredSum_df,key=pcrid,csv_name='PCR2_SummaryDunningInformation.csv',mode=write_mode,header=header)
    
    ###逾期（透支）汇总信息段
    isOverdueSum_df = xf.isOverdueSum_df(temp1,column_type = column_type)
    add_key_and_save2csv(isOverdueSum_df,key=pcrid,csv_name='PCR2_SummaryOverdue.csv',mode=write_mode,header=header)
    
    ###相关还款责任汇总信息
    isRepayDutySum_df = xf.isRepayDutySum_df(temp1,column_type = column_type)
    add_key_and_save2csv(isRepayDutySum_df,key=pcrid,csv_name='PCR2_SummaryReleatedRepayment.csv',mode=write_mode,header=header)

    ###公共信息概要
    isPubInfoSum_df = xf.isPubInfoSum_df(temp1,column_type = column_type)
    add_key_and_save2csv(isPubInfoSum_df,key=pcrid,csv_name='PCR2_SummaryPublicInformation.csv',mode=write_mode,header=header)
    
    ###后付费业务欠费信息汇总
    isPostpaidSum_df = xf.isPostpaidSum_df(temp1,column_type = column_type)
    add_key_and_save2csv(isPostpaidSum_df,key=pcrid,csv_name='PCR2_SummaryOverduePostpayFee.csv',mode=write_mode,header=header)
    
    ###信贷交易明细-信贷账户交易信息
    debitCreditAccount_df = xf.debitCreditAccount_df(temp1,column_type = column_type)
    creditTransaction_df = debitCreditAccount_df[creditTransaction_col]
    #creditTransaction_df['SID'] = creditTransaction_df['AccountNumber']
    creditTransaction_df['SID'] = [str(uuid.uuid4()) for _ in range(len(creditTransaction_df))]
    debitCreditAccount_df['SID'] = creditTransaction_df['SID']

    add_key_and_save2csv(creditTransaction_df,key=pcrid,csv_name='PCR2_CreditTransaction.csv',mode=write_mode,header=header)
    # add_key_and_save2csv(debitCreditAccount_df,key=pcrid,csv_name='信贷交易明细.csv',mode=write_mode,header=header)
    creditPaymentRecord_df = CreditPaymentRecord(debitCreditAccount_df)
    add_key_and_save2csv(creditPaymentRecord_df,key=pcrid,csv_name='PCR2_CreditPaymentRecord.csv',mode=write_mode,header=header)
    need_col = list(creditTransactionExtra_col.keys())
    creditTransactionExtra = debitCreditAccount_df[need_col].rename(columns=creditTransactionExtra_col)
    creditTransactionExtra['BillDate'] = creditTransactionExtra['LastPaymentDate']

    # 使用 fillna 进行填充（只适用于 NaN 情况）
    creditTransactionExtra['AccountState'] = creditTransactionExtra['AccountState'].fillna(
        creditTransactionExtra['AccountStateRecord2']
    )

    add_key_and_save2csv(creditTransactionExtra,key=pcrid,csv_name='PCR2_CreditTransactionExtra.csv',mode=write_mode,header=header)
    
    ###特殊交易信息
    crSpecialTrans_df = xf.crSpecialTrans(temp1,column_type = column_type)
    add_key_and_save2csv(crSpecialTrans_df,key=pcrid,csv_name='PCR2_CreditSpecialTransaction.csv',mode=write_mode,header=header)
    
#     ###特殊事件信息
#     crSpecialEvent_df = xf.crSpecialEvent(temp1,column_type = column_type)
#     add_key_and_save2csv(crSpecialEvent_df,key=pcrid,csv_name='特殊事件信息.csv',mode=write_mode,header=header)
    
    ###大额专项分期信息
    largeSpecStage_df = xf.largeSpecStage(temp1,column_type = column_type)
    add_key_and_save2csv(largeSpecStage_df,key=pcrid,csv_name='PCR2_LargeAmountSpecialInstalment.csv',mode=write_mode,header=header)
    
    ###授信协议基本信息段
    crAgreement_df = xf.crAgreement(temp1,column_type = column_type)
    add_key_and_save2csv(crAgreement_df,key=pcrid,csv_name='PCR2_CreditAgreement.csv',mode=write_mode,header=header)
    
    ###相关还款责任信息
    crRelatedRepayDuty_df = xf.crRelatedRepayDuty(temp1,column_type = column_type)
    add_key_and_save2csv(crRelatedRepayDuty_df,key=pcrid,csv_name='PCR2_CreditRelatedRepayment.csv',mode=write_mode,header=header)
    
    ###后付费信息
    ncrTransDetail_df = xf.ncrTransDetail(temp1,column_type = column_type)
    add_key_and_save2csv(ncrTransDetail_df,key=pcrid,csv_name='PCR2_NonCreditTransaction.csv',mode=write_mode,header=header)
    
    ###税务信息
    pubTaxOwed_df = xf.pubTaxOwed(temp1,column_type = column_type)
    add_key_and_save2csv(pubTaxOwed_df,key=pcrid,csv_name='PCR2_OwingTaxInformation.csv',mode=write_mode,header=header)
    
    ###民事判决记录信息
    pubCivilJudgement_df = xf.pubCivilJudgement(temp1,column_type = column_type)
    add_key_and_save2csv(pubCivilJudgement_df,key=pcrid,csv_name='PCR2_CivilJudgmentRecords.csv',mode=write_mode,header=header)
    
    ###强制执行记录信息
    pubForceExecute_df = xf.pubForceExecute(temp1,column_type = column_type)
    add_key_and_save2csv(pubForceExecute_df,key=pcrid,csv_name='PCR2_EnforcementRecords.csv',mode=write_mode,header=header)
    
    ###行政处罚记录信息
    pubAdminPenalty_df = xf.pubAdminPenalty(temp1,column_type = column_type)
    add_key_and_save2csv(pubAdminPenalty_df,key=pcrid,csv_name='PCR2_PunishmentRecords.csv',mode=write_mode,header=header)
    
    ###住房公积金参缴记录信息
    pubHousingFund_df = xf.pubHousingFund(temp1,column_type = column_type)
    add_key_and_save2csv(pubHousingFund_df,key=pcrid,csv_name='PCR2_HousingProvidentFundRecords.csv',mode=write_mode,header=header)
    
    ###低保救助信息记录信息
    pubSubsistanceAllowance_df = xf.pubSubsistanceAllowance(temp1,column_type = column_type)
    add_key_and_save2csv(pubSubsistanceAllowance_df,key=pcrid,csv_name='PCR2_LowReliefRecords.csv',mode=write_mode,header=header)
    
    ###执业资格记录信息
    pubQualification_df = xf.pubQualification(temp1,column_type = column_type)
    add_key_and_save2csv(pubQualification_df,key=pcrid,csv_name='PCR2_QualificationRecords.csv',mode=write_mode,header=header)
    
    ###行政奖励记录信息
    pubAdminReward_df = xf.pubAdminReward(temp1,column_type = column_type)
    add_key_and_save2csv(pubAdminReward_df,key=pcrid,csv_name='PCR2_AwardRecords.csv',mode=write_mode,header=header)
    
    ###行政奖励记录信息-标注及声明信息段
    pubAdminRewardMark_df = xf.pubAdminRewardMark(temp1,column_type = column_type)
    add_key_and_save2csv(pubAdminRewardMark_df,key=pcrid,csv_name='PCR2_CalloutStatement.csv',mode=write_mode,header=header)
    
    
    ###查询记录
    inquiryRecord_df = xf.inquiryRecord(temp1,column_type = column_type)
    add_key_and_save2csv(inquiryRecord_df,key=pcrid,csv_name='PCR2_QueryRecord.csv',mode=write_mode,header=header)
    
#     ###标注及声明信息
#     otherMarkDeclaration_df = xf.otherMarkDeclaration(temp1,column_type = column_type)
#     add_key_and_save2csv(otherMarkDeclaration_df,key=pcrid,csv_name='标注及声明信息.csv',mode=write_mode,header=header)


