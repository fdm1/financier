requires Docker installed to work

```
bash budgetize.sh <config_file> \
    [-s <start_date> (YYYY-MM-DD) (default today)] \
    [-e <end_date> (YYYY-MM-DD) (default 1 year from now)] \
    [-b <start_balance> (default 0)] \
    [-f <output_file> (default <config>_YYYYMMDD_HHSS.csv) ] \
    [--to_csv=False (default True) ]
```

If `--no_csv`, it will print the budget to the screen.
Else, it will create a csv in the same directory as the config.


Config yaml format:

```
budget_events:
  <event_name>:
    amount: <amount>
    kind: <kind: [one_time | bimonthly | biweekly | monthly]
    start_date: <date (YYYY-MM-DD) default: today>
    day_of_month: <day>
    end_date: <date (YYYY-MM-DD>
  <event_name>:
    amount: <amount>
    kind: <kind: [one_time | bimonthly | biweekly | monthly]
    start_date: <date (YYYY-MM-DD) default: today>
    day_of_month: <day>
    end_date: <date (YYYY-MM-DD>
  (etc...as many events as you need)...
```

### `budget_event` kinds:

How different events work and what paramters do what.

If a parameter isn't listed below a `kind`, it has no effect.

`kind`:
  - `one_time`: a one time transaction
    - `start_date`: date money will take effect
    - `end_date`: money will not move after this date
  - `bimonthly`: money will take effect on 1st and 15th
    - `end_date`: money will not move after this date
  - `biweekly`: money takes effect every 14 days
    - `start_date`: used to calculate if date is multiple of 14 days before/after a given date
    - `end_date`: money will not move after this date
  - `monthly`:
    - `day_of_month`: what day of the month to move money (avoid after the 28th as end of month dates not fixed yet)
    - `end_date`: money will not move after this date


## Example:
```
$ bash budgetize.sh $(pwd)/sample_budget.yaml -b 100 -s 2016-10-01 -e 2016-11-30 --to_csv=False

          Date             Event   Amount  Balance
          0   2016-10-01  Starting Balance           $100.00
          1         ----              ----     ----     ----
          2   2016-10-01          mortgage   -$2.00   $98.00
          3   2016-10-14         frank_pay   $10.00  $108.00
          4   2016-10-15          mortgage   -$2.00  $106.00
          5   2016-10-20           daycare   -$4.50  $101.50
          6   2016-10-28         frank_pay   $10.00  $111.50
          7         ----              ----     ----     ----
          8   2016-10-31      End of Month           $111.50
          9
          10  2016-11-01          mortgage   -$2.00  $109.50
          11  2016-11-02          vacation  -$24.30   $85.20
          12  2016-11-11         frank_pay   $10.00   $95.20
          13  2016-11-15          mortgage   -$2.00   $93.20
          14  2016-11-20           daycare   -$4.50   $88.70
          15  2016-11-25         frank_pay   $10.00   $98.70
          16        ----              ----     ----     ----
          17  2016-11-30      End of Month            $98.70
          18
          19
          20        ----              ----     ----     ----
          21  2016-11-30    Ending Balance            $98.70


```
