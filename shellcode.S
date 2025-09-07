#include <sys/syscall.h>

.globl main
    .type   main, @function

 main:
    xorq  %rax, %rax
    pushq %rax
    movq  $0x7478742e73656461, %rax 
    pushq %rax
    movq  $0x72672f746e656475, %rax 
    pushq %rax
    movq  $0x74732f656d6f682f, %rax 
    pushq %rax

    pushq %rsp
    popq  %rdi
    movq  $87, %rax
    syscall

   
    xorq  %rdi, %rdi
    movq  $60, %rax
    syscall
	