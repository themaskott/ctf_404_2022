#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>


int main(){

    char buff[0x100] = {0} ;
    char input[0x50] ;

    printf("%d %d %d\n", O_RDONLY, O_WRONLY, O_RDWR);
    printf("%d\n", O_CREAT) ;

    printf("%d %d %d\n", S_IRWXU, S_IRUSR, S_IWUSR);

    int a = open("flag.txt",O_RDWR) ;

    printf("%d\n",a) ;
    read(a,buff,0x100) ;
    printf("%s\n",buff);

    
    read(0,input,0x25) ;


return 0;
}
