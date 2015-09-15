
5 { figure(l,F),
    tile(l,F,X,Y),
	tile(l,F,X+1,Y),
	tile(l,F,X,Y+1),
	tile(l,F,X,Y+2)
	: dim(X) : dim(Y) : dim(X+1) : dim(Y+1) : dim(Y+2) } 5 :- ele(F,X,Y).

% number of eles
exist_eles(N-1) :- exist_eles(N), N != 1.
1 { ele(N,X,Y) : dim(X) : dim(Y) } 1 :- exist_eles(N).

exist_eles(6).
