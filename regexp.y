%{
#include <stdio.h>
#include <stdlib.h>
#if YYBISON
int yylex();
int yyerror(const char *s);
#endif

int numero = 0;

typedef struct Programme {
	char* code;
	int taille;
	int position;
};

int yyerror(const char *s)
{
    fprintf(stderr, "Erreur syntaxique: %s\n", s);
    return 0;
}

Programme* Initprogramme() {
	Programme prog = { .code = (char*)malloc(64 * sizeof(char)), .taille = 64, .position = 0 };  // Initialisation du programme
	if (prog.code == NULL) exit(1); 
	return &prog; // On retourne un pointeur
}

void Freeprogramme(programme* p){
	free(p->code); // Liberation du malloc
	free(p);
}

Programme* Add_to_Prog(Programme* p, char* add){
	if (p->position+ strlen(add) >= p->taille){
		realloc(p->code, p->taille*2);
	}
	sprintf(p->code + strlen(add),"%s", add);
	return p;
	
}

Programme* Programme_G = Initprogramme();

%}


//Grammaire 
%token LETTRE LIGNE
%token PLUS POINT ETOILE PAR_O PAR_F


%left PLUS
%left POINT
%right ETOILE

//Déclarations 
%%
ligne : 
	S LIGNE {
		res_final = $1 ;
	}

expr :
	PAR_O expr PAR_F {
		$$ = parenth($2);
		free($2);
	}
	|
	expr ETOILE {
		char * chaine = malloc(strlen($1) + 2);
		sprintf(chaine, "%s", $1);
		free($1);
		$$ = chaine; 
	}
	|

	expr PLUS expr {
		char * chaine = malloc(strlen($1) + strlen($3) + 2);
		sprintf(chaine, "%s+%s, $1, $3);
		free($1); free($3);
		$$ = chaine;
	}
	|
	expr POINT expr {
		char * chaine = malloc(strlen($1) + strlen($3) +2);
		sprintf(chaine, "%s.s%", $1, $3);
		$$ = chaine;
	}
	|
	LETTRE {
		$$ = yylval("a", "b", "c");
	}
%%




