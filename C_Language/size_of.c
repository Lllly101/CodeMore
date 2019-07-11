#include <stdio.h>

int main( ) {

int a;
char b;

/*abbrev of long int c*/ 
long c; 

printf("int size: %d\n", sizeof(int));
printf("short size: %d\n", sizeof(short));
printf("long size: %d\n", sizeof(long));
printf("char size: %d\n", sizeof(char));
printf("float size: %d\n", sizeof(float));
printf("double size: %d\n", sizeof(double));

return 0;
}
