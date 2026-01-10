%{

#include "operateur_bison.tab.h"
// Fichier qui genere et stock les tokens

%}

%% 
// Lettre
[a-c] { return LETTRE;}
[ \t] {;} // ignore les espaces 
[\n] { return LIGNE;}
// Opérateur 
"+"    { return PLUS ;}
"."    { return POINT ; }
"*"    { return ETOILE ; }
"("    {return PAR_O ;}
")"    {return PAR_F;}

%%
// Juste pour tester avant.
int main() {
	yylex();
	return 0;
}