/*

functions.c

Quentin MARY - 12 novembre 2012

*/


#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include "functions.h"

//Creation d'un nouveau processus
pid_t create_process(void)
{
	pid_t pid;

	do {
		pid = fork();
	} while ((pid == -1) && (errno == EAGAIN));

	return pid;
}

// Calcul de l'index d'un caratere (wwww.developpez.com)
//+utilisee ici pour reperer le '@'
int str_istr (const char *cs, const char *ct)
{
	int index = -1;

	if (cs != NULL && ct != NULL)
	{ 
		char *ptr_pos = NULL;

		ptr_pos = strstr (cs, ct);
		if (ptr_pos != NULL)
		{ 
			// Modification de la fonction originale, on veut l'index du premier
			//+caractere apres le '@' d'ou l'ajout de '+1'
			index = ptr_pos - cs + 1;
		}
	}
	return index;
}

// Extraction d'une sous-chaine (www.developpez.com)
//+utilisee ici pour recuperer le nom du serveur (situe apres l'index calcule avant)
char *str_sub (const char *s, unsigned int start, unsigned int end)
{
	char *new_s = NULL;

	if (s != NULL && start < end)
	{
		new_s = malloc (sizeof (*new_s) * (end - start + 2));
		if (new_s != NULL)
		{
			int i;

			for (i = start; i <= end; i++)
			{
				new_s[i-start] = s[i];
			}
			new_s[i-start] = '\0';
		}
		else
		{
			fprintf (stderr, "Memoire insuffisante\n");
			exit (EXIT_FAILURE);
		}
	}
	return new_s;
}

// Ecriture de la connexion dans les logs
void write_log(char *server, int pid, int connect) {
	FILE* logfile = NULL;
	char tmp[256];
	char *home;
	char log[256];
	time_t timestamp = time(NULL);
	
	// Recuperation et formatage de la date systeme
	strftime(tmp, sizeof(tmp), "%A %d %B %Y - %X", localtime(&timestamp));
	
	// Le fichier doit se trouver dans le home de l'utilisateur
	home = getenv("HOME");
	if (home == NULL) {
		perror("home");
		exit (EXIT_FAILURE);
	}
	strcpy(log, home);
	strcat(log, "/ssh.log");
	
	// Ouverture du fichier de log (sera cree s'il n'esxiste pas)
	logfile = fopen(log, "a");
	
	if (logfile != NULL) {
		// Lors de l'ouverture de la connexion
		if (connect == 1) {
			fprintf(logfile, "Connect to %s on %s --- %d\n", server, tmp, pid);
		}
		// Et lors de la fermeture
		else if (connect == 0) {
			fprintf(logfile, "Disconnect from %s on %s --- %d\n", server, tmp, pid);
		}
		fclose(logfile);
	}
}

// Instructions du nouveau processus
void process(char *arg[], char *title)
{
	char *server = get_server(arg[7]);
	
	sprintf(title, "%s %d", server, (int) getpid() );
	write_log(server, (int) getpid(), 1);
	
	// On associe le titre aux arguments a passer
	arg[2] = title;
	
	// Execution de l'appel systeme ici une nouvelle instance xterm
	if (execv("/usr/bin/xterm", arg) == -1) {
		perror("execv");
		exit(EXIT_FAILURE);
	}
	
}

void father(char *connect, int pid_son) {
	char *server = get_server(connect);
	
	// On attend la fin du fils pour eviter les zombies et pouvoir logger la deco (sauf kill ou ^C)
	if (wait(NULL) == -1) {
		perror("wait :");
	}
	else {
		write_log(server, (int) pid_son, 0);
	}
}

char *get_server(char *tmp) {
	int index = str_istr(tmp, "@");
	int length = strlen(tmp);
	char *server = "";
	
	// On creer un string contenant le nom du serveur
	if (index > 0) {
		server = str_sub(tmp, index, length);
	}
	else {
		server = tmp;
	}
	
	return server;
}