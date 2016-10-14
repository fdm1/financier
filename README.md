requires Docker installed to work

```
bash budgetize.sh <config_file> \
    [-s <start_date> (YYYY-MM-DD) (default today)] \
    [-e <end_date> (YYYY-MM-DD) (default 1 year from now)] \
    [-b <start_balance> (default 0)] \
    [-f <output_file> (default <config>_YYYYMMDD_HHSS.csv) ] \
    [--no_csv=True (default False) ]
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

