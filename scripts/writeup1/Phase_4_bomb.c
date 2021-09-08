#include <libc.h>

int func4(int param_1)
{
  int iVar1;
  int iVar2;

  if (param_1 < 2) {
    iVar2 = 1;
  }
  else {
    iVar1 = func4(param_1 + -1);
    iVar2 = func4(param_1 + -2);
    iVar2 = iVar2 + iVar1;
  }
  return iVar2;
}

int main(){
    int test = 1;

    while(func4(test) != 55){
        test++;
    }
    printf("%d\n", test);

return (0);
}