#include <stdlib.h>
#include <stdio.h>

#define SIZE 128

void fill_tab(unsigned char *tab_a, unsigned char *tab_b){

  int a = 0 ;
  int b = 0 ;

  for (int i = 0 ; i < SIZE ; i++){

    a = rand() ;
    tab_a[i] = (unsigned char)a;

    b = rand() ;
    tab_b[i] = (unsigned char)b | 1;

  }

}


void affich_tab(unsigned char *tab_a, unsigned char *tab_b, int num_tab){

    printf("tab_%d = ", num_tab);
    for(int i = 0 ; i < SIZE ; i++)
        printf("%02x", tab_a[i]);
    printf("\n");

    printf("tab_%d = ", num_tab+1);
    for(int i = 0 ; i < SIZE ; i++)
        printf("%02x", tab_b[i]);
    printf("\n");

    printf("password_%d = ", num_tab);
    for(int i = 0 ; i < SIZE ; i++)
        printf("%02x", tab_a[i]^tab_b[i]);
    printf("\n");


    printf("\n");

}




int main(){

    unsigned char tab_1[SIZE] = {0} ;
    unsigned char tab_2[SIZE] = {0} ;

    unsigned char tab_3[SIZE] = {0} ;
    unsigned char tab_4[SIZE] = {0} ;

    unsigned char tab_5[SIZE] = {0} ;
    unsigned char tab_6[SIZE] = {0} ;

    unsigned char tab_7[SIZE] = {0} ;
    unsigned char tab_8[SIZE] = {0} ;


   fill_tab(tab_1, tab_2) ;
   fill_tab(tab_3, tab_4) ;
   fill_tab(tab_5, tab_6) ;
   fill_tab(tab_7, tab_8) ;

   affich_tab(tab_1, tab_2, 1) ;
   affich_tab(tab_3, tab_4, 3) ;
   affich_tab(tab_5, tab_6, 5) ;
   affich_tab(tab_7, tab_8, 7) ;





    return 0 ;
}
