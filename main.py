import psycopg2
import pandas as pd
from decimal import *
import numpy
import datetime
connection = psycopg2.connect("postgresql://observer:koh7theozoh8ohCh@5.79.73.74:5532/example")

def getInstalls():  # GET ALL INSTALLS PER DAY
    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT CAST(to_timestamp(player."createTime") as date) as DATE, COUNT(*)
                            FROM player
                            GROUP BY  CAST(to_timestamp(player."createTime") as date)
                            ORDER BY date;""")

        df = pd.DataFrame(cursor.fetchall())
        return df

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def getPayments(firstDay,lastDay):
    try:
        cursor = connection.cursor()
        data = inputs(firstDay,lastDay)
        cursor.execute("""select temp.dateLTV, temp.dattt, temp.suma/temp1.count as ltv from
                            (SELECT CAST(to_timestamp(payment."createTime") as date) as dateLTV,
                                  CAST(to_timestamp(player."createTime") as date) as dattt,
                                  SUM(("currencyAmount" * CAST("clientData"->>'payout_foreign_exchange_rate' as FLOAT))::NUMERIC)as suma,
                                  SUM(("currencyAmount" * CAST("clientData"->>'payout_foreign_exchange_rate' as FLOAT))::NUMERIC)
                            FROM payment
                            inner join player on payment."playerId" = player.id
                             WHERE (
                                   payment."createTime" >= extract(epoch from (%s) at time zone 'utc') and payment."createTime" <= extract(epoch from (%s) at time zone 'utc') )
                          
                             group by  dateLTV, CAST(to_timestamp(player."createTime") as date)
                            ORDER BY dateLTV)
                            as temp
                            inner join
                               (SELECT  CAST(to_timestamp(player."createTime") as date) as DATE, COUNT(*) as count
                            FROM player
                            GROUP BY  CAST(to_timestamp(player."createTime") as date)
                            ORDER BY date) as temp1 on temp.dattt=temp1.DATE
                            ORDER BY temp.dateLTV, temp.dattt;""", data)

        df = pd.DataFrame(cursor.fetchall())
        cursor.close()
        connection.close()
        return df

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def inputs(firstDay,lastDay):
    inputPaymentFirstDay = input('Enter first date of payment (or leave it empty to get from first record):')
    inputPaymentLastDay = input('Enter last date of payment (or leave it empty to get from last record):')

    if inputPaymentFirstDay == '':
        inputPaymentFirstDay = pd.to_datetime(firstDay).date()

    if inputPaymentLastDay == '':
        inputPaymentLastDay = pd.to_datetime(lastDay).date()

    return(inputPaymentFirstDay, inputPaymentLastDay)

if __name__ == "__main__":

    #create empty dataframe dataframe
    dateInstalls = getInstalls()

    # create list of all dates
    listOfDays = pd.to_datetime(dateInstalls[0]).unique()
    firstDay = listOfDays[0]
    lastDay = listOfDays[-1]

    dateInstalls.columns = ['Date','Installs']
    dateInstalls['LTV'] = 0
    dateInstalls['LTV'] = dateInstalls['LTV'].astype(float)

    dateInstalls.set_index('Date', inplace=True)
    dateInstalls.index = pd.to_datetime(dateInstalls.index)

    for i in range(1, dateInstalls.shape[0]):  # add LTV's columns
        dateInstalls['LTV' + str(i)] = None
        dateInstalls['LTV' + str(i)] = dateInstalls['LTV' + str(i)].astype(float)

    df = getPayments(firstDay,lastDay)

    # convert to datetime
    df[0] = pd.to_datetime(df[0])
    df[1] = pd.to_datetime(df[1])

    rangeOfAllDates = []
    ind = 0
    for date in listOfDays: # go from all days
        date = pd.Timestamp(date)
        rangeOfAllDates.append(date)  # expected range of dates
        listOfTransactions = df.loc[df[0] == date][1].tolist()

        if date != lastDay: # check if it's not last day
            for oneOfRangeDates in rangeOfAllDates:
                LTVind = (date - oneOfRangeDates).days + 1
                LTV = 'LTV' + str(LTVind)
                prevLTV = 'LTV' + str(LTVind - 1)

                if oneOfRangeDates not in listOfTransactions:  # check if no records for specific date
                    if int(LTVind) > 1:  # if it's not the first day
                        dateInstalls.set_value(oneOfRangeDates, LTV, Decimal(Decimal(dateInstalls.loc[oneOfRangeDates][prevLTV]) ))
                    else: # LTV1 CASE
                        dateInstalls.set_value(oneOfRangeDates, LTV, 0)

                else:  # if registered user
                    temp = df[1][ind]
                    val = df[2][ind]
                    if int(LTVind) > 1:  # if it's not the first day (when it's higher than LTV1)
                        dateInstalls.set_value(temp, LTV, Decimal(Decimal(dateInstalls.loc[temp][prevLTV]) + Decimal(val)))
                    else: # LTV1 Case
                        dateInstalls.set_value(temp, LTV, Decimal(val))

                    ind = ind + 1

        else: # if last date update LTV as well
            for oneOfRangeDates in rangeOfAllDates:  # DOESN't add if no record in specific date
                LTVind = (date - oneOfRangeDates).days + 1
                LTV = 'LTV' + str(LTVind)
                prevLTV = 'LTV' + str(LTVind - 1)

                if oneOfRangeDates not in listOfTransactions:  # when no records for specific date
                    if int(LTVind) > 1:  # if it's not the first day
                        dateInstalls.set_value(oneOfRangeDates, LTV, Decimal(Decimal(dateInstalls.loc[oneOfRangeDates][prevLTV])))
                        dateInstalls.set_value(oneOfRangeDates, 'LTV', Decimal(Decimal(dateInstalls.loc[oneOfRangeDates][prevLTV])))
                    else:  # LTV1 CASE
                        dateInstalls.set_value(oneOfRangeDates, LTV, 0)
                        dateInstalls.set_value(oneOfRangeDates, 'LTV', 0)

                else:  # if registered user
                    temp = df[1][ind]
                    val = df[2][ind]
                    if int(LTVind) > 1:  # if it's not the first day (when it's higher than LTV1)
                        dateInstalls.set_value(temp, LTV,Decimal(Decimal(dateInstalls.loc[temp][prevLTV]) + Decimal(val)))
                        dateInstalls.set_value(temp, 'LTV',Decimal(Decimal(dateInstalls.loc[temp][prevLTV]) + Decimal(val)))
                    else:  # LTV1 Case
                        dateInstalls.set_value(temp, LTV, Decimal(val))
                        dateInstalls.set_value(temp, 'LTV', Decimal(val))

                    ind = ind + 1

        dateInstalls.to_csv('result.csv') # build table