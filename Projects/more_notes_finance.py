'''
MORE NOTES

Weighted average cost of capital: rate that a company is expected to pay on average
to all its security holders to finance its assets.
WACC represents the minimum return a company needs to generate on its existing asset
base to justify owning that existing asset base so the investors don't
invest elsewhere.

If a company is only financed by debt and equity:
WACC = (D/(D+E))Cd + (E/(D+E))Ce
where D is debt, E is equity, Cd and Ce are costs of debt and equity


CAPITAL ASSET PRICING MODEL
investors are risk-averse, prefer higher returns, willing to buy optimal portfolio

Market portfolio: bundle of all possible investments in the world - it has the BEST
risk-return ratio since it's the most possibly diverse portfolio
    -it's the MOST efficient portfolio on the efficient frontier
HOWEVER: the CAPM also assumes the existence of a risk-free asset
    -there will be people so risk-averse ethey'll buy it even though it has crappy returns

we know the risk free return - that's the intercept on our y axis of return on the markowitz graph
we can therefore graph a line whose slope is the relation between how much more risk you take on
and how much more return you get (how much of the market portfolio
you invest in) - this line is called the CAPITAL MARKET LINE or capital allocation line

there will be a point where the CML and the efficient frontier are tangent

BETA - a pillar of the capital asset pricing model
	-helps us quantify relation between an asset and the market portfolio
	-measures a stock's risk vs. overall market

the market has a certain level of systematic volatility - some stocks are more volatile but earn more,
others are low risk low return investments

beta = covariance(asset, market)/variance(market)
if beta ==
	0: no relationship between stock and market
	<1: lower risk, lower return - defensive stock
	>1: higher risk, higher return - aggressive stock
	1: exactly the same as the market
	
CAPM formula:
	ri = rf + beta*(rm-rf)
	ri is expected return of stock
	rf is return of risk free thing
	rm is market return
	rm-rf is equity risk premium - return of investing in market
	over a risk free returner
What the CAPM formula tells you: ri is the amount of return you should be compensated for the risk
	you're taking
	
SHARPE RATIO
a rational investor considers both risk and return, right?
we can compute risk adjusted return
Sharpe Ratio = (ri-rf)/sigma i - ri and rf are once again expected return of a stock and fixed return
	of a risk-free asset, sigma i is standard deviation
The higher the Sharpe ratio, the more return per unit risk a stock has!

Alpha - a measure of how good or bad a fund is doing
Our standard CAPM setting assumes an alpha of zero - BUT
if we include alpha in our formula, it becomes
	ri = alpha + rf + beta*(rm-rf)
a good portfolio manager gets positive alpha, bad gets negative
alpha measures whether you outperform the market or not

'''
