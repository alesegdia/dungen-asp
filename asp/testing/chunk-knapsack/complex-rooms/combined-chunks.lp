#const height = 20.
#const width = 20.

row(1..height).
column(1..width).

size(width, height).

% room definition
%2 {
%chunk(X,Y,3,3,ID),
%chunk(X+2,Y+2,3,3,ID) } 2
%	:- roomA(X,Y,ID).

% num rooms
%1 { roomA(X,Y,3) :
%	column(X) :
%	row(Y) } 1.

2 {
	chunk(X,Y,3,3,ID),
	chunk(X+2,Y+2,3,3,ID) } 2 :- roomA(ID, X, Y).

exist_roomAs(N-1) :- exist_roomAs(N), N != 1.
1 { roomA(N, X, Y) : column(X) : row(Y) } 1 :- exist_roomAs(N).

exist_roomAs(6).

% no out of bounds
:- 	chunk(X,Y,W,H,ID), 
	1{X + W > width, Y + H > height}.


:- 	chunk(X1,Y1,W1,H1,ID1), 
	chunk(X2,Y2,W2,H2,ID2),  
	ID1 != ID2,
	X1 <= X2, X2 < X1 + W1, 
	Y1 <= Y2, Y2 < Y1 + H1.


:-  chunk(X1,Y1,W1,H1,ID1), 
	chunk(X2,Y2,W2,H2,ID2),
	ID1 != ID2,
	X1 <= X2, X2 < X1 + W1, 
	Y2 <= Y1, Y1 < Y2 + H2.


