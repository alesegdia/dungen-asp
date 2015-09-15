

tt(X,Y) :- tile(A,B,X,Y).

% two figures can't overlap
:- tile(FT,A,X,Y), tile(FT,B,X,Y), A != B.
:- tile(A,FI,X,Y), tile(B,FI,X,Y), A != B.
:- tile(A,C,X,Y), tile(B,D,X,Y), A != B.

adj(X1, Y1, X2, Y2) :-
	dim(X1;Y1;X2;Y2),
	tt(X1, Y1),
	tt(X2, Y2),
	#abs(X1-X2) + #abs(Y1-Y2) == 1.

connected(FT1, FN1, FT2, FN2) :-
	figure(FT1, FN1),
	tile(FT1, FN1, X1, Y1),
	tile(FT2, FN2, X2, Y2),
	FN1 != FN2,
	adj(X1, Y1, X2, Y2).

:- figure(F1, N1),
	figure(F2, N2),
	N1 != N2,
	not connected(F1, N1, F2, N2).


connected(FT1, FN1, FT2, FN2) :-
	figure(FT1, FN1),
	figure(FT2, FN2),
	figure(FT3, FN3),
	(FT1,FN1) != (FT2, FN2),
	(FT3,FN3) != (FT1, FN1),
	(FT3,FN3) != (FT2, FN2),
	connected(FT1, FN1, FT3, FN3),
	connected(FT2, FN2, FT3, FN3).



