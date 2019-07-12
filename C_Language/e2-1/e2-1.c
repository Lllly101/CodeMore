#include <stdio.h>

int main() {

int a;
float b;
double c;
char d;

long int e;
short int f;
signed long int g=0;

a = 1;
while ( a > 0) {
    a++;
    }

printf("sizeof int is: %ld\n", sizeof(a));
printf("int最小值: %d\n", a);
printf("int最大值： %d\n", a-1);

return 0;
}
