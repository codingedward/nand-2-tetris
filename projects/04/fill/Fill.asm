// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(CHECK_KEY)
    @i
    M=0
    @KBD
    D=M
    @BLACKEN
    D;JGT       // jump to blacken if kbd > 0
(WHITEN)
    @i
    D=M
    @8192
    D=D-A
    @CHECK_KEY
    D;JEQ       // (i-8192) == 0 done whitening!
    @i
    D=M
    @SCREEN
    A=A+D
    M=0
    @i
    M=M+1
    @WHITEN
    0;JMP
(BLACKEN)
    @i
    D=M
    @8192
    D=D-A
    @CHECK_KEY
    D;JEQ       // (i-8192) == 0 done blackening
    @i
    D=M
    @SCREEN
    A=A+D
    M=-1
    @i
    M=M+1
    @BLACKEN
    0;JMP


