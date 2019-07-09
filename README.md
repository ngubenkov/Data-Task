# volka
Task
You need to prepare a report showing the growth of daily cohort LTV of players (Report description).
You should use PostgreSQL database, tables:
player  - players’ data
payment – payments’ data
Access to test database:
postgresql://observer:koh7theozoh8ohCh@5.79.73.74:5532/example 
You need to create a script on R or Python which connects to the database, executes the SQL-query and then completes processing of received data. Final table is saved in a file.
Do not download the database. Initial filtering and grouping should be done in SQL.
Optionally complete additional tasks.
We are waiting for the result in archive (script and instruction to launch it) on jobs@volkagames.com

Report description
A game designer needs to understand what is the value of the users who started to play on certain dates. 
He wants to insert a range of registration dates in the query to get a table like this:
Date
Installs
LTV
LTV-1
LTV-2
LTV-3
LTV-4
1 of May
1000
0.4$
0.1$
0.2$
0.3$
0.4$
2 of May
1200
0.02$
0.01$
0.01$
0.02$


3 of May
800
1.0$
0.8$
1.0$




(Imagine today is a 5th of May)

The table shows the growth of LTV (LifeTime Value) of players who registered on a particular day - that is, how much the game has earned on average from each install on that day, and how this value changes over time. This allows to evaluate how successfully players convert into paying users - for example, in this case, on May 2, something obviously went wrong (small and slowly growing LTV), but on May 3 there was some successful solution (high and growing rapidly LTV).
Date – Registration date of the cohort of users;
Installs – The amount of game installations on a particular day;
LTV – Total cohort LTV;
LTV-1, 2, 3... – LTV of the first and subsequent days of life.
How to calculate the LTV
LTV of the cohort is a sum of all cohort payments for all time divided by Installs.
LTV of the life day is a sum of payments during current and all previous days, divided by Installs. It is an accumulative metric. It always only grows with time (or doesn’t change if there were no purchases).


Additional details
The game designer will insert the date range in the query, according to your instructions;
The tables contain data for 3 months, but the report should allow the Game Designer to set any range of dates (including half a year or a year).
The dates are calendar. That is, it doesn’t matter at what time of the day the player is registered. He could start playing at 00:01 or at 23:59 on the 1st of May - in both cases he is in the cohort of the 1st of May. His 1st day of life will be the 1st of May (even if it was just a minute), and the 2nd day of life will come on the 2nd of May;
Today's date is not included in the report, as the day is not yet finished
Note that we calculate the LTV of the entire cohort. That is, the sum of purchases must be divided by all installats, and not only by those players who paid.
Additional tasks
The main difficulty of the report is to correctly receive and count LTV growth data, and to display the table in the correct form.
However, the report can be made more accurate by using additional information from the database. 
Report options:
Payments can be made in different currencies. Convert all amounts to US dollars (exchange rates are in clientData);
Prepare two tables: with platform commission and without platform commission;
Take into account that some payments could be canceled and the amount of these payment is refunded to the player;
Take into account that the new gaming day comes at 00:00 AM GMT-1. It is desirable to calculate the statistics in this time zone.
Take into account that the payment can be a test.

Requirements
The results of the script must match our results;
SQL query must be optimized for execution speed;
We will also consider code organization, explanations and comments.

