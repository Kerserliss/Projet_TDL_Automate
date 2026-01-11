%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#if YYBISON
int yylex();
int yyerror(const char *s);
#endif

int numero = 0;

typedef struct Programme {
	char* code;
	int taille;
	int position;
} Programme;

int yyerror(const char *s)
{
    fprintf(stderr, "Erreur syntaxique: %s\n", s);
    return 0;
}

Programme* Initprogramme() {
	Programme* prog = (Programme*)malloc(sizeof(Programme));
	if (prog == NULL) exit(1);

	prog->code = (char*)malloc(64 * sizeof(char));
	prog->taille = 64;
	prog ->position = 0;  // Initialisation du programme

	if (prog->code == NULL) exit(1); 
	return prog; // On retourne un pointeur
}

void Freeprogramme(Programme* p){
	free(p->code); // Liberation du malloc
	free(p);
}

Programme* Add_to_Prog(Programme* p, char* add){
	if (p->position+ strlen(add) >= p->taille){
		p->code = realloc(p->code, p->taille*2);
		p->taille *= 2;
		if (p->code == NULL) exit(1);
	}
	sprintf(p->code + p->position,"%s", add);
	p->position += strlen(add);
	return p;
	
}

Programme* Programme_G;

%}


//Grammaire 

%token <str> LETTRE 
%token PLUS POINT ETOILE PAR_O PAR_F LIGNE
%union {int n; 
		char* str;}


%type <n> instruction expression

%left PLUS
%left POINT 
%right ETOILE

%start instruction

%%

instruction : 
	expression LIGNE expression {
		FILE *fpython;
		fpython = fopen("main.1.py","w");

		fprintf(fpython, "from automate import *\n \n");
		char terminator[] = "\0";
		Add_to_Prog(Programme_G, "\0");
		fputs(Programme_G->code, fpython);
		fprintf(fpython, "\n\n");

		fprintf(fpython, "a%d = tout_faire(a%d) \na%d = tout_faire(a%d) \n\n", numero, $1, numero+1, $3);

		fprintf(fpython, "if egal(a%d, a%d) : \n\tprint(\" EGAL \")\nelse: \n\tprint(\"NON EGAL \")", numero, numero +1);
		fclose(fpython);
		Freeprogramme(Programme_G);

	};

expression : 
	PAR_O expression PAR_F {
		$$ = $2;
	}
	|
	expression ETOILE {

		// Creation du nom de l automate
		char etoile[8];
		sprintf(etoile, "a%d", numero);
		numero++;

		// Creation de la ligne correspondante
		char buffer[64];
		sprintf(buffer, "%s = etoile(a%d)\n", etoile,$1 );
		Add_to_Prog(Programme_G, buffer);

		$$ = numero-1;
	}
	|
	expression POINT expression {

		// Creation du nom de l automate
		char merge[8];
		sprintf(merge, "a%d", numero);
		numero++;

		// Creation de la ligne correspondante
		char buffer[64];
		sprintf(buffer, "%s = concatenation(a%d, a%d)\n", merge, $1, $3);
		Add_to_Prog(Programme_G, buffer);

		$$ = numero -1;
	}
	| 
	expression PLUS expression {

		// Creation du nom de l'automate
		char add[8];
		sprintf(add, "a%d", numero);
		numero++;

		// Creation de la ligne correspondante
		char buffer[64];
		sprintf(buffer, "%s = union(a%d, a%d)\n", add,$1, $3);
		Add_to_Prog(Programme_G, buffer);
		$$ = numero-1;
	}
	|
	LETTRE {

		// Creation de l'automate simple
		char buffer[64];
		sprintf(buffer, "a%d = automate(\"%s\") \n",numero, $1);
		Add_to_Prog(Programme_G, buffer);
		numero++;
		$$ = numero - 1;  // On renvoie le numero precedent
	}
	;

%%

Programme* Programme_G;

int main(void) {
    Programme_G = Initprogramme();
    yyparse();
    return 0;
}