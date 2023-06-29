# sketch a dataframe (using excel/spreadsheets)

If you want to explore spark or SQL or write tests, IMHO its cumbersome to write a dataframe definition in a text editor.
A table calculation tool provides a better user experience for that.
This tool is meant to bridge the gap and allow you to generate dataframe or SQL VALUES statements from a copy/paste of such a tool.

## usage

1. draw some dataframe in excel ([excel.new](http://excel.new)) or spreadsheets ([spreadsheet.new](http://spreadsheet.new))
  * should look like [this](https://docs.google.com/spreadsheets/d/1RMAZ3To3dgCO1S0I_P6-8VE70tXBoQekfJq47vF1Fws/edit?usp=sharing) one
  * has a header line containing the column names (line one)
  * has data rows/lines (starting from line 2)
  * can have empty values
  * example:
    ```tsv
        date	name	debt	remark
        2022-02-01	max	1	
        2022-02-02	max	2	
        2022-02-03	max	3	
        2022-02-04	max	4	
        2022-02-01	john	3	
    ```
2. copy the range, including the header
3. paste the range into the `input.tsv` file
4. run the script via `make generate` or `python main.py` **OR via running it on [repl.it](https://replit.com/@duke8585/sketchadataframe#input.tsv)**
5. get your code pieces from either of the `output.*` files

## features

* will detect constants - à la `colnames.date` - and not string-quote them in the statements
* will replace empty string values with `null` or `None`
* smart enough to figure out end of data values
* additional comments for creating a spark context

## limitations

* if fields have non.scalar types, the script will still string-quote them

## resources

the repository on [github](https://github.com/duke8585/sketch_some_dataframe)

