%{

#include "operateur_bison.tab.h"
// Fichier qui genere et stock les tokens

%}

%% 
// Lettre
[a-c] { return LETTRE;}
[ \t] {;} // ignore les espaces 
[\n] { return LIGNE;}

%%
// Juste pour tester avant.
int main() {
	yylex();
	return 0;
}