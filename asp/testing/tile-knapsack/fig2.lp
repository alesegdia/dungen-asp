
5 { figure(F),
	tile(F,X,Y),
	tile(F,X,Y+1),
	tile(F,X+1,Y),
	tile(F,X+1,Y+1)
	: dim(X) : dim(Y) : dim(X+1) : dim(Y+1) } 5 :- cuadrado(F,X,Y).

% number of cuadrados
exist_cuadrados(N-1) :- exist_cuadrados(N), N != 1.
1 { cuadrado(N,X,Y) : dim(X) : dim(Y) } 1 :- exist_cuadrados(N).

exist_cuadrados(4).
