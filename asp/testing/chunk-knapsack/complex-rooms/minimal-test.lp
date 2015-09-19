#const height = 60.
#const width = 60.

row(1..height).
column(1..width).

size(width, height).


12 { chunk(X,Y,11,11) : column(X) : row(Y) } 12.

% no out of bounds
:- 	chunk(X,Y,W,H), 
	1{X + W > width, Y + H > height}.


:- 	chunk(X1,Y1,W1,H1), 
	chunk(X2,Y2,W2,H2),  
	1 {X1 != X2,Y1 != Y2}, 
	X1 <= X2, X2 < X1 + W1, 
	Y1 <= Y2, Y2 < Y1 + H1.


:-  chunk(X1,Y1,W1,H1), 
	chunk(X2,Y2,W2,H2),
	1 {X1 != X2,Y1 != Y2}, 
	X1 <= X2, X2 < X1 + W1, 
	Y2 <= Y1, Y1 < Y2 + H2.


