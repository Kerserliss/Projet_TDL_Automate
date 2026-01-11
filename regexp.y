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

%token <str> LETTRE 
%token PLUS POINT ETOILE PAR_O PAR_F LIGNE


%left PLUS
%left POINT
%right ETOILE

instruction : 
	expression LIGNE expression {
		FILE *fpython;
		fpython = fopen("main.1.py","w");

		fprintf(fpython, "from automate import *\n \n");
		char* terminator[2] = "\0"
		Add_to_Prog(Programme_G, terminator)
		fputs(Programme_G->code, fpython);
		fprintf(fpython, "\n\n");

		fprintf(fpython, "a%d = tout_faire(a%d) \na%d = tout_faire(a%d) \n\n", numero, $1, numero+1, $3);

		fprintf(fpython, "if egal(a%d, a%d) : \n\tprint(\" EGAL \")\nelse: \n\tprint(\"NON EGAL \"));
		close(fpython);
		Freeprogramme(Programme_G);

	};

expression : 
	PAR_O expression PAR_F {
		$$ = $2;
	}
	|
	expression ETOILE {

		\\ Creation du nom de l'automate
		char etoile[20];
		sprintf(etoile, "a%d", numero);
		numero++;

		\\ Creation de la ligne correspondante
		sprintf(buffer, "%s = etoile(a%d)\n", etoile,$1 );
		Add_to_Prog(Programme_G, buffer);

		$$ = numero-1;
	}
	|
	expression POINT expression {

		\\ Creation du nom de l'automate
		char merge[20];
		sprintf(merge, "a%d", numero);
		numero++;

		\\ Creation de la ligne correspondante
		spintf(buffer, "%s = concatenation(%s, %s)\n, merge, $1, $2);
		Add_to_Prog(Programme_G, buffer);

		$$ = numero -1;
	}
	| 
	expression PLUS expression {

		\\ Creation du nom de l'automate
		char add[20];
		sprintf(add, "a%d", numero);
		numero++;

		\\ Creation de la ligne correspondante
		sprintf(buffer, "%s = union(%s, %s)\n", add,$1, $2);
		Add_to_Prog(Programme_G, buffer);
		$$ = numero-1;
	}
	|
	LETTRE {

		\\ Creation de l'automate simple
		char buffer[50];
		sprintf(buffer, "a%d = automate(\"%s\")",numero, $1);
		Add_to_Prog(Programme_G, buffer);
		numero++;
		$$ = numero - 1;  // On renvoie le numero precedent
	}
	;

	


