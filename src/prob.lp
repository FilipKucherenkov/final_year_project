\ENCODING=ISO-8859-1
\Problem name: Capacity-Local-Search

Maximize
 obj1: source#j_0 + source#j_1 + source#j_2 + source#j_3
Subject To
 c0:  - t_0#sink + j_1#t_0 + j_2#t_0 + j_3#t_0  = 0
 c1:  - t_1#sink + j_1#t_1 + j_2#t_1 + j_3#t_1  = 0
 c2:  - t_2#sink + j_1#t_2 + j_2#t_2  = 0
 c3:  - t_3#sink + j_1#t_3 + j_2#t_3  = 0
 c4:  - t_4#sink + j_0#t_4  = 0
 c5:  - t_5#sink + j_0#t_5  = 0
 c6:  - t_6#sink  = 0
 c7:  source#j_0 - j_0#t_4 - j_0#t_5  = 0
 c8:  source#j_1 - j_1#t_0 - j_1#t_1 - j_1#t_2 - j_1#t_3  = 0
 c9:  source#j_2 - j_2#t_0 - j_2#t_1 - j_2#t_2 - j_2#t_3  = 0
 c10: source#j_3 - j_3#t_0 - j_3#t_1  = 0
Bounds
 0 <= source#j_0 <= 2
 0 <= source#j_1 <= 4
 0 <= source#j_2 <= 1
 0 <= source#j_3 <= 2
 0 <= t_0#sink <= 2
 0 <= t_1#sink <= 2
 0 <= t_2#sink <= 2
 0 <= t_3#sink <= 2
 0 <= t_4#sink <= 2
 0 <= t_5#sink <= 2
 0 <= t_6#sink <= 2
 0 <= j_0#t_4 <= 1
 0 <= j_0#t_5 <= 1
 0 <= j_1#t_0 <= 1
 0 <= j_1#t_1 <= 1
 0 <= j_1#t_2 <= 1
 0 <= j_1#t_3 <= 1
 0 <= j_2#t_0 <= 1
 0 <= j_2#t_1 <= 1
 0 <= j_2#t_2 <= 1
 0 <= j_2#t_3 <= 1
 0 <= j_3#t_0 <= 1
 0 <= j_3#t_1 <= 1
End
