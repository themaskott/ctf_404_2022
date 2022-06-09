#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int main(){

    char buff[0x100] = {0} ;


    printf("%d %d %d\n", O_RDONLY, O_WRONLY, O_RDWR);
    printf("%d\n", O_CREAT) ;
    printf("%d\n", O_EXCL) ;

    printf("%d %d %d\n", EACCES, S_IRUSR, S_IWUSR);

    int a = open("flag.txt",O_RDONLY) ;

    printf("%d\n",a) ;
    read(a,buff,0x100) ;
    printf("%s\n",buff);


return 0;
}
