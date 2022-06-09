#include <stdlib.h>
#include <stdio.h>


int main(){

    unsigned char tab_1[128] = {0} ;
    unsigned char tab_2[128] = {0} ;
    
    unsigned char tab_3[128] = {0} ;
    unsigned char tab_4[128] = {0} ;
    
    unsigned char tab_5[128] = {0} ;
    unsigned char tab_6[128] = {0} ;
    
    unsigned char tab_7[128] = {0} ;
    unsigned char tab_8[128] = {0} ;

    int a = 0 ;
    int b = 0 ;
    int c = 0 ;
    int d = 0 ;
    

    for (int i = 0 ; i < 128 ; i++){

        a = rand() ;
        tab_1[i] = (unsigned char)a;

        b = rand() ;
        tab_2[i] = (unsigned char)b | 1;

    }
    
    
    for (int i = 0 ; i < 128 ; i++){

        c = rand() ;
        tab_3[i] = (unsigned char)c;

        d = rand() ;
        tab_4[i] = (unsigned char)d | 1;

    }



    for (int i = 0 ; i < 128 ; i++){

        a = rand() ;
        tab_5[i] = (unsigned char)a;

        b = rand() ;
        tab_6[i] = (unsigned char)b | 1;

    }
    
    
    for (int i = 0 ; i < 128 ; i++){

        c = rand() ;
        tab_7[i] = (unsigned char)c;

        d = rand() ;
        tab_8[i] = (unsigned char)d | 1;

    }

    printf("tab_1 :\n") ;
    for (int i = 0 ; i < 128 ; i++ ){
        printf("%02x",tab_1[i]) ;
        if((i+1)%8==0)
            printf(" ");
        if((i+1)%16==0)
            printf("\n");
    }





    printf("tab_1 :\n") ;
    for (int i = 0 ; i < 128 ; i++ ){
        printf("%02x",tab_1[i]) ;
        if((i+1)%8==0)
            printf(" ");
        if((i+1)%16==0)
            printf("\n");
    }

 

    printf("\n");
    printf("tab_2 :\n");

    for (int i = 0 ; i < 128 ; i++){
        printf("%02x",tab_2[i]) ;
        if ((i+1)%8==0)
            printf(" ");
        if((i+1)%16==0)
            printf("\n");
    }

    printf("tab_1, tab_2, tab_1 xor tab_2\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_1[i]);
    printf("\n");
    
    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_2[i]);
    printf("\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_1[i]^tab_2[i]);
    printf("\n");


    printf("\n");

    printf("tab_3, tab_4, tab_3 xor tab_4\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_3[i]);
    printf("\n");
    
    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_4[i]);
    printf("\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_3[i]^tab_4[i]);
    printf("\n");



    printf("tab_5, tab_6, tab_5 xor tab_6\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_5[i]);
    printf("\n");
    
    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_6[i]);
    printf("\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_5[i]^tab_6[i]);
    printf("\n");

    printf("tab_7, tab_8, tab_7 xor tab_8\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_7[i]);
    printf("\n");
    
    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_8[i]);
    printf("\n");

    for(int i = 0 ; i < 128 ; i++)
        printf("%02x", tab_7[i]^tab_8[i]);
    printf("\n");

    return 0 ;
}
