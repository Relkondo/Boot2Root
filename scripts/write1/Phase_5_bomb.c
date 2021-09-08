#include <libc.h>

int main(int ac, char **av) {
  char encoder[] = "isrveawhobpnutfg";
  char tmp = 'a';

  while (tmp <= 'z') {
    printf("%c -> %c\n", tmp, encoder[tmp & 0xf]);
    tmp++;
  }

  return 0;
}
/*
Rendu =
a -> s
b -> r
c -> v
d -> e
e -> a
f -> w
g -> h
h -> o
i -> b
j -> p
k -> n
l -> u
m -> t
n -> f
o -> g
p -> i
q -> s
r -> r
s -> v
t -> e
u -> a
v -> w
w -> h
x -> o
y -> b
z -> p

*/