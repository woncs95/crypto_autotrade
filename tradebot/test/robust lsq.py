from scipy.optimize import least_squares
from dev import main
import matplotlib.pyplot as plt

candle= main.get_candlestick("BTC_USDT", "1D")
x=candle["t"]
##local maximum
y=list(map(float,candle["h"]))

#Run robust least squares with loss='soft_l1', set f_scale to 0.1 which means that inlier residuals are approximately lower than 0.1.

res_robust = least_squares(loss='soft_l1', f_scale=0.1, args=(x, y))


#y_robust = generate_data(x, *res_robust.x)

plt.plot(x, res_robust, label='robust lsq')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.show()