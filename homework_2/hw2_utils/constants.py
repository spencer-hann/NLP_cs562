# Useful labels that we might need to re-use
import numpy as np

# label to use for offset/bias feature:
OFFSET = '**OFFSET**'
TTR_ZERO = '**TTR_0_1**'
TTR_ONE = '**TTR_1_2**'
TTR_TWO = '**TTR_2_3**'
TTR_THREE = '**TTR_3_4**'
TTR_FOUR = '**TTR_4_5**'
TTR_FIVE = '**TTR_5_6**'
TTR_SIX = '**TTR_6_INF**'

TTR_ARRAY = np.asarray(
            [TTR_ZERO,
            TTR_ONE,
            TTR_TWO,
            TTR_THREE,
            TTR_FOUR,
            TTR_FIVE,
            TTR_SIX]
            )
