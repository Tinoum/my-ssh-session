/*

functions.c

Quentin MARY - 12 novembre 2012

*/

#include <stdlib.h>
#include <stdio.h>
#include "functions.c"

int main(int argc, char *argv[])
{
	if (argc != 2) {
		return -1;
	}
	
	pid_t pid = create_process();
	char title[6] = "";
	// Arguments qui seront passes a l'appel systeme
	char *arg[250] = { "xterm", "-title", "Xterm", "-name" , "ssh", "-e", "ssh", argv[1], NULL };

	switch (pid) {
	case -1:
		perror("fork");
		return EXIT_FAILURE;
		break;
	case 0:
		process(arg, title);
		break;
	default:
		father(arg[7], pid);
		break;
	}
	return EXIT_SUCCESS;
}
