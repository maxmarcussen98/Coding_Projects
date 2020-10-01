This is a simple trading algorithm that I built in my spare time during my junior year. 

From a pre-selected list of stocks, the algorithm buys stocks whose 3-day moving average is the furthest below their 45-day moving average.
It sells stocks whose 3-day moving average is the furthest above the 45-day.
The algorithm then analyzes 20,000 random allocations of stocks for total portfolio return, and uses the allocation with the highest portfolio
return relative to the standard deviation of that return -- buying a portfolio with the highest reward-to-risk ratio.
For actual buying and selling, the Python code makes calls to Alpaca's API. 
