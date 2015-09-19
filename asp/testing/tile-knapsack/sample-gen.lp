

solid(X,Y) :- tile(B,X,Y).

% two figures can't overlap
:- tile(A,X,Y), tile(B,X,Y), A != B.

adj(X1, Y1, X2, Y2) :-
	dim(X1;Y1;X2;Y2),
	solid(X1, Y1),
	solid(X2, Y2),
	|X1-X2| + |Y1-Y2| == 1.

connected(FN1, FN2) :-
	tile(FN1, X1, Y1),
	tile(FN2, X2, Y2),
	FN1 != FN2,
	adj(X1, Y1, X2, Y2).

:- figure(N1),
	figure(N2),
	N1 != N2,
	not connected(N1, N2).


connected(FN1, FN2) :-
	FN1 != FN2,
	FN3 != FN1,
	FN3 != FN2,
	connected(FN1, FN3),
	connected(FN2, FN3).



