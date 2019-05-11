// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Assume x = *R0, y = *R1, product = *R2

    @R2
    M=0         // product = 0
(LOOP)
    @R0
    M=M-1
    D=M
    @END      
    D;JLT       // goto END if x <= 0
    @R1
    D=M         // D = y
    @R2
    M=M+D       // product += y
    @LOOP
    0;JMP
(END)
    @END
    0;JMP