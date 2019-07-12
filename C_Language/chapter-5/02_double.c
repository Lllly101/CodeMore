#include<stdio.h>

int main() {

    printf("%f\n", 12.0/0.0);
    printf("%f\n", -12.0/0.0);
    printf("%f\n", 0.0/0.0);

    printf("%d\n", 12/0); // warning

    return 0;
}
