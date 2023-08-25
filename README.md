# weewxx-xtype-wet-bulb-temperature

Extend [weewx](https://www.weewx.com) with the wet bulb temperature data type.

## Calculating The Wet Bulb Temperature

The [perryweather web site provides us with a formula for calculating the wet bulb temperature](https://perryweather.com/resources/what-is-wbgt-and-how-do-you-calculate-it/):

    Tw = T * arctan[0.151977 * (rh% + 8.313659)^(1/2)] + arctan(T + rh%) – arctan(rh% – 1.676331) + 0.00391838 *(rh%)^(3/2) * arctan(0.023101 * rh%) – 4.686035


