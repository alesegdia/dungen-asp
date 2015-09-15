
#const width = 10.
dim(1..width).

% define ELE figure type
5 { figure(l,F),
    tile(l,F,X,Y),
	tile(l,F,X+1,Y),
	tile(l,F,X,Y+1),
	tile(l,F,X,Y+2)
	: dim(X) : dim(Y) : dim(X+1) : dim(Y+1) : dim(Y+2) } 5 :- ele(F,X,Y).

tt(X,Y) :- tile(A,B,X,Y).

% define CUADRADO figure type
5 { figure(c,F),
	tile(c,F,X,Y),
	tile(c,F,X,Y+1),
	tile(c,F,X+1,Y),
	tile(c,F,X+1,Y+1)
	: dim(X) : dim(Y) : dim(X+1) : dim(Y+1) } 5 :- cuadrado(F,X,Y).

% two figures can't overlap
:- tile(FT,A,X,Y), tile(FT,B,X,Y), A != B.
:- tile(A,FI,X,Y), tile(B,FI,X,Y), A != B.
:- tile(A,C,X,Y), tile(B,D,X,Y), A != B.

% number of eles
exist_eles(N-1) :- exist_eles(N), N != 1.
1 { ele(N,X,Y) : dim(X) : dim(Y) } 1 :- exist_eles(N).

% number of cuadrados
exist_cuadrados(N-1) :- exist_cuadrados(N), N != 1.
1 { cuadrado(N,X,Y) : dim(X) : dim(Y) } 1 :- exist_cuadrados(N).

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


exist_eles(6).
exist_cuadrados(4).

