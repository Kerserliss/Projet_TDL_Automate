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