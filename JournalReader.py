from cryptography.fernet import Fernet

class JournalReader(object):
    def __init__(self):
        self.filepath = "JournalsConsolidated"
        self.secret_key = "better_make_it_secret"
        self.dict_dates = {}
        self.prev_mon, self.prev_day, self.prev_year = None, None, None
        # Some strange character fractions can occur
        self.fix_dates = {'⅓' : "1/3", "¼": "1/4", "⅕": "1/5", "⅙": "1/6", "¾": "3/4", "½": "1/2",
             "⅘": "4/5", "⅛": "1/8", "⅗":"3/5", "⅚":"5/6", "⅝": "5/8", "⅞":"7/8",
            "⅔":"2/3", "⅖":"2/5", "⅜":"3/8"}
        # Process the file at init time
        self.process_file()
        
    def bogus_char_checker(self, st):
        """
        Some strange characters can exist. so remove them if necessary
        """
        _st = st.strip().replace('/', '')
        for char in _st:
            if char in 'abcdefghijklmnopqrstquvwrxyz':
                return False
        return True


    def insert_into_dict(self,mon,day,year,line):
        """
        For a given mon,day,year (all ints) and a line,
        insert this line into our date dictionary
        """
        if self.dict_dates.get(mon, None):
            if self.dict_dates[mon].get(day, None):
                # If we find a new line, just add to the line
                if self.dict_dates[mon][day].get(year, None):
                    self.dict_dates[mon][day][year] += line
                else:
                    self.dict_dates[mon][day][year] = line
            else:
                self.dict_dates[mon][day]={}
                self.dict_dates[mon][day][year] = line
        else:
            self.dict_dates[mon]={}
            self.dict_dates[mon][day]={}
            self.dict_dates[mon][day][year] = line

    def process_file(self):
        """
        Process input file, line by line, parsing through dates and entries.
        """
        for line in open(self.filepath, encoding='utf-8'):

            # Split on if the first number is 1-9
            line = line.strip()
            if line and ord(line[0]) >= 49 and ord(line[0]) <= 57 and "/" in line and self.bogus_char_checker(line):
                #print(line)
                if self.fix_dates.get(line, None):
                    print("Found a bad date after ",  self.prev_mon, self.prev_day, self.prev_year)
                    line = self.fix_dates.get(line, None)
                if line.strip()!='' and len(line) < 12:

                    split_date = line.strip().split("/")
                    if len(split_date) == 2:
                        mon, day = split_date
                    elif len(split_date) == 3:
                        mon, day, year = split_date

                    if "" in split_date: # bug in parsing the date
                        print("Bad Date! ", split_date)
                        day = self.prev_day + 1
                        try:
                            self.insert_into_dict(mon,day,year,line)
                        except Exception as e:
                            print(e, "failed to insert as a date")

                    else:
                        #print("New date found: ", mon, day, year )
                        mon, day, year = int(mon), int(day), int(year)
                    if len(str(year)) == 2:
                        year = int("20"+str(year))
                    self.prev_mon, self.prev_day, self.prev_year = int(mon), int(day), int(year)
            elif line:
                self.insert_into_dict(mon,day,year,line)
                
    def get_entries(self, mn, d):
        """
        Prints out the entries found for all years
        mn: month in integer format
        d: day in integer format
        TODO: have a lookback parameter for `n` years
        """
        _entries = self.dict_dates.get(mn, None)
        if _entries:
            _entries = _entries.get(d, None)
            if _entries:
                years = _entries.keys()
                #print(years)
                for year in sorted(years):
                    print(year)
                    print(_entries[year])
                    print("\n")

    
