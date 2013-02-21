/*

functions.h

Quentin MARY - 12 novembre 2012

*/

// Les fonctions suivantes correspondent au traitement des processus
pid_t create_process(void);
void process(char *arg[], char *title);
void father(char *connect, int pid_son);

// Les fonctions suivantes ont ete honteusement plagiee sur www.developpez.com
int str_istr (const char *cs, const char *ct);
char *str_sub (const char *s, unsigned int start, unsigned int end);

// Diverses autres fonctions
void write_log(char *server, int pid, int connect);
char *get_server(char *tmp);
