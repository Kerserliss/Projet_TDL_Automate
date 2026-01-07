%{

#include "operateur_bison.tab.h"
// Fichier qui genere et stock les tokens

%}

%% 
// Ordre de priorite - Operateur
[(] { return PO;}
[)] { return PF;}
[*] { return ETOILE; }
[.] { return CONCATENATION;}
[+] { return OU; }
[ \t] {;} // ignore les espaces 
[\n] { return LIGNE;}

%%
// Juste pour tester avant.
int main() {
	yylex();
	return 0;
}