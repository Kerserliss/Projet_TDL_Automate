%{

#include "regexp.tab.h"
// Fichier qui genere et stock les tokens

%}

%% 
[a-c] { yylval.str = strdup(yytext); return LETTRE;}
[ \t\r] {;} // ignore les espaces et retours chariot
[\n] { return LIGNE;}


"+"    { return PLUS ;}
"."    { return POINT ; }
"*"    { return ETOILE ; }
"("    {return PAR_O ;}
")"    {return PAR_F;}

%%