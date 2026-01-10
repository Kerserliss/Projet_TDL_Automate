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

%union {
	char* str;
}
%token <str> LETTRE 
%token PLUS POINT ETOILE PAR_O PAR_F LIGNE

%type <str> expression


%left PLUS
%left POINT
%right ETOILE

instruction : 
	expression {
		char buffer[100];
		sprintf(buffer, "resultat = %s\n", $1);
		Add_to_Prog(Programme_G, buffer)
	};

expression : 
	PAR_O expression PAR_F {
		$$ = $2;
	}
	|
	expression ETOILE {
		char nom[20];
		sprintf(nom, "a%d", numero);
		numero++;

		char buffer[200];
		sprintf(buffer, "%s = %s\n", nom, $1);
		Add_to_Prog(Programme_G, buffer);

		char etoile[20];
		sprintf(etoile, "a%d", numero);
		numero++;

		sprintf(buffer, "%s = etoile(%s)\n, etoile, nom);
		Add_to_Prog(Programme_G, buffer);

		$$ = strdup(etoile);
	}
	|
	expression POINT expression {
		char gauche[20];
		sprintf(gauche, "a%d", numero);
		numero++;

		char buffer[200];
		sprintf(buffer, "%s = %s\n", gauche, $1);
		Add_to_Prog(Programme_G, buffer);

		char droite[20];
		sprintf(droite, "a%d", numero);
		numero++;

		sprintf(buffer, "%s = %s\n", droite, $3);
		Add_to_Prog(Programme_G, buffer);

		char merge[20];
		sprintf(merge, "a%d", numero);
		numero++;

		spintf(buffer, "%s = concatenation(%s, %s)\n, merge, gauche, droite);
		Add_to_Prog(Programme_G, buffer);

		$$ = strdup(merge);
	}
	| 
	expression PLUS expression {
		char resultat[20];
		sprintf(resultat, "a%d", numero);
		numero++;

		char buffer[200];
		sprintf(buffer, "%s = %s\n", resultat, $1);
		Add_to_Prog(Programme_G, buffer);

		char expr[20];
		sprintf(expr, "a%d", numero);
		numero++;

		sprintf(buffer, "%s = %s\n", expr, $3);
		Add_to_Prog(Programme_G, buffer);

		char add[20];
		sprintf(add, "a%d", numero);
		numero++;

		sprintf(buffer, "%s = union(%s, %s)\n", add, resultat, expr);
		Add_to_Prog(Programme_G, buffer);
		$$ = strdup(add);
	}
	|
	LETTRE {
		char buffer[50];
		sprintf(buffer, "automate(\"%s\")", $1);
		$$ = strdup(buffer);
	}
	;

	


