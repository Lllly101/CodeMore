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

b = 1;
while ( b > 0 ) {
    b++;
}
printf("sizeof float is %ld\n", sizeof(b));
printf("float最大值: %f\n", b);
printf("float最小值: %f\n", b-1);

return 0;
}
