#const height = 10.
#const width = 10.
#const chunk_types = 3.

row(1..height).
column(1..width).

chunk_width(1,3).
chunk_height(1,3).
% just in case we want a shorter form
chunk_size(1,3,3).

% only one chunk type for now
{ chunk(X,Y,1) : row(Y) : column(X) }.
#maximize [ chunk(X,Y,T) ].

% no out of bounds
:- 	chunk(X,Y,T), 
	chunk_height(T,H), 
	chunk_width(T,W), 
	1{X + W > width, Y + H > height}.

% no overlapping
:- 	chunk(X1,Y1,T1), 
	chunk(X2,Y2,T2),  
	1 {X1 != X2,Y1 != Y2}, 
	chunk_width(T1,W1),
	chunk_height(T1,H1),
	X1 <= X2, X2 < X1 + W1, 
	Y1 <= Y2, Y2 < Y1 + H1.

:-    	chunk(X1,Y1,T1), 
	chunk(X2,Y2,T2), 
	1 {X1 != X2,Y1 != Y2}, 
	chunk_width(T1,W1),
	chunk_height(T2,H2),
	X1 <= X2, X2 < X1 + W1, 
	Y2 <= Y1, Y1 < Y2 + H2.

% visualization helper
size(width,height).

