import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def str_to_date(x):
  dt = datetime.strptime(x, "%m/%d/%Y")
  # formatted_date = dt.strftime("m/%d/%Y")
  return dt

def is_last_year(date):
    now = datetime.now()
    this_year_start = datetime(now.year, 1, 1, 0, 0)
    last_year_start = this_year_start - relativedelta(years=1)
    return last_year_start <= date < this_year_start

def get_last_year_gifts(df, date_as_string_col="giftDateFormatted"):
    #assumes df has column with date as string "%m/%d/%y"
    df["date"] = df[date_as_string_col].apply(str_to_date)
    is_last_year_gift = df["date"].apply(is_last_year)
    return df[is_last_year_gift]

def is_last_year_to_date(date):
    now = datetime.now()
    last_year_to_date = now - relativedelta(years=1)
    last_year_start = datetime(last_year_to_date.year, 1, 1, 0, 0)
    return last_year_start <= date <= last_year_to_date

def get_lytd_gifts(df, date_as_string_col="giftDateFormatted"):
    #assumes df has column with date as string "%m/%d/%y"
    df["date"] = df[date_as_string_col].apply(str_to_date)
    is_last_year_to_date_gift = df["date"].apply(is_last_year_to_date)
    return df[is_last_year_to_date_gift]

def is_this_year(date):
    now = datetime.now()
    this_year_start = datetime(now.year, 1, 1, 0, 0)
    return this_year_start <= date

def get_ytd_gifts(df, date_as_string_col="giftDateFormatted"):
    #assumes df has column with date as string "%m/%d/%y"
    df["date"] = df[date_as_string_col].apply(str_to_date)
    is_year_to_date_gift = df["date"].apply(is_this_year)
    return df[is_year_to_date_gift]

def get_lytd_gifts_by_contact(df, date_as_string_col="giftDateFormatted"):
    lytd_gifts = get_lytd_gifts(df, date_as_string_col)
    lytd_gift_amounts = lytd_gifts[["contactPassthroughId", "amount"]]
    return lytd_gift_amounts.groupby(["contactPassthroughId"]).sum()

def main():
    pass

if __name__ == '__main__':
    main()
