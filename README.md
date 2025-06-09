
### Intro 
This project supports extracting a zip file of csv price data
and calculating correlations across a universe of stocks. The project uses Python (pandas, numpy) as its main backend tools
and streamlit for the application GUI.

### Data Loading
The zipped data file should be placed in the `/data` directory and named `stock_data.zip`. From there, you can simply call `make unzip` from the project root.
This will create two sub-directories, one called `stock_data` and one called `parquet` these store the unzipped csv files, and the
csv's converted into `.parquet` files, respectively.
This is a one-step process (takes less than a couple of seconds on my machine) which not only unzips the file, but also converts
the csv data into parquet for fast downstream reading.

### Instructions to Run
If you haven't yet, please read the loading data step, as this is a prerequisite for launching this app
successfully.

Once the relevant data has been extracted into the relevant files under the /data directory, all that's needed
to run the project is to enter ```make run``` in a terminal, from project root, which should spin up a streamlit
GUI in your browser.

Please make sure to have the requirements from ```requirements.txt``` installed in your virtual environment (recommended) or
python management tool.

To run the provided test suite, simply run `make run_tests` from the project root.

### Data exploration / Cleaning
 - Missing values / errors / data inconsistencies:
    - One thing that came up from visualizations and testing is that the data in `20220216.csv` - representing daily prices for
16-Feb-2022 had corrupted price data of all 1's. This file was not included in the analysis. 
    - Also, any NaN stock tickers or prices were dropped. The assumption for us is that correlation information can be actionable, so I wanted to make sure
that the values seen are accurate, with the risk that less values will be present (less false positives but risking less data). 
    - We also saw that for most of the years, there were significant gaps between the months of September and December.
    - Two of the files had different data formats to the rest, but it seems like csv date parsing handled those.
 - Window handling:
   - Our window handling reflects the same objective / priority as above. We only include valid windows. These are defined as at least
   twenty trading days preceding target date, and no more than 5 days between consecutive dates.
   - Other approaches could be argued here, but again, we take the perspective of these correlations potentially being signals,
   so the higher the statistical significance of these measures, the better, under this assumption.
   
     

### Approach
The general approach for this project is:
1. extracting the zip files
2. converting the resulting csv files to parquet (more in the Optimization section)
3. aggregate data into a master (long) dataframe
4. pivot data into (wide) dataframe, where each column represents the time-price series per ticker
5. For each target date, a lookback window is generated iff there are 20 available trading days preceding it,
and no gap larger than 5 days amongst those.
6. For each window, we generate a correlation matrix across the full universe, and extract descriptive statistics (e.g. top N)
to aid visualization of the data.
7. Plot relevant data in line charts, heatmaps and bar charts.

Tools used: Python (mostly Pandas with numpy), parquet file representation for raw data, Streamlit for GUI


### Optimizations
- Caching:
  - The decoding of the parquet files and aggregation into the master pivot dataframe (wide) is only done once at launch time and is \
  cached across all subpages of the streamlit app. 
  - Because our universe size (N=5000) is also quite large, pre-computing correlation matrices (each on the order of O(N^2)) 
  for all lookback windows (~900) turned out to be prohibitive, both from a memory and a user-experience latency perspective. Therefore,
  we have instead decided to calculate each window's correlation matrix on the fly, and cache the results after calculation. We set
  a max number of items on the cache to restrict memory from scaling uncontrollably. Overall, the latency is small here.
  - At some point, I tried experimenting with compressing the correlation matrices before caching (my primary concern was memory overhead)
  but I wasn't able to get this to a satisfactory latency so far, so I chose to stick with a limit on the cache items as described above.
- Parquet vs CSV:
   - During testing, the slowest aspect of the app always seemed to be loading the data into the (wide) pivot dataframe. This makes
  sense. I ran a profiler over the various steps of that process (retrieving filepaths, reading_csv's into dataframes, concatenating into long dataframe,
  and pivoting the DataFrame). It seemed that reading the csv's into dataframes were the costliest aspect, so I experimented with converting the files
  into parquet during the unzip phase, and that gave a 2x improvement at read-time, for a trade-off of minimal one-time conversion overhead.
   
   ```
  csv read time:

   File list time: 0.0011188983917236328
   CSV read time: 1.2151949405670166
   Concat time: 0.027607202529907227
   Drop + pivot time: 0.6258032321929932
    
   parquet read times:
    
   File list time: 0.0012552738189697266
   CSV read time: 0.5872199535369873
   Concat time: 0.026544809341430664
   Drop + pivot time: 0.662041187286377
  ```
- Vectorization:
  - Wherever possible, native numpy or pandas code was used for operations, and a best effort to research
  the faster options when multiple choices were available e.g. np.corrcoeff() vs df.corr()
   